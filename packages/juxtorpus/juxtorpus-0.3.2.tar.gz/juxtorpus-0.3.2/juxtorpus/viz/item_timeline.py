""" Item Timeline

Plot a number of items and their chosen metric across a shared timeline.
"""
import pandas as pd

"""
NOTES:
Trace:
Inputs: list of timestamps, list of counts/metric
Output: a Trace


Timeline:
Factory Methods:
1. from_freqtables
2. from_corpus_groups ---> defaults to using the standard dtm

Features:
1. Mode: Highlight Peaks, Highlight Cumulative
2.


Properties:
1. expose terms
2. expose terms and their colours
"""
from pandas.api.types import is_datetime64_dtype
from typing import Union, Optional
import plotly.graph_objs as go
from collections import namedtuple
from functools import partial
import random
import ipywidgets as widgets
from IPython.display import display
import pandas as pd
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS

from juxtorpus.viz import Widget
from juxtorpus.corpus import Corpus
from juxtorpus.corpus.freqtable import FreqTable
from juxtorpus.corpus.meta import SeriesMeta
from juxtorpus.utils.utils_ipywidgets import debounce

TNUMERIC = Union[int, float]
TPLOTLY_RGB_COLOUR = str


class ItemTimeline(Widget):
    """ ItemTimeline
    This visualisation class plots a number of items and their associated metric across a timeline.
    The two modes for the metrics are:
        1. Peak
        2. Cumulative

    The top items have maximum opacity 1.0 and then opacity drops.

    Factory Methods:
    from_freqtables - uses term as items, frequencies as metric.
    from_corpus_groups - uses datetime groupings
    from_corpus - tries to find a datetime meta and group it (default freq = 1 week)
    """
    TRACE_DATUM = namedtuple('TRACE_DATUM', ['item', 'datetimes', 'metrics', 'colour', 'texts'])

    @classmethod
    def from_corpus(cls, corpus: Corpus, datetime_meta_key: str = None, freq: str = '1w', use_custom_dtm: bool = False):
        keys = {'datetime': datetime_meta_key}
        if datetime_meta_key is None:
            for k, meta in corpus.meta.items():
                if type(meta) != SeriesMeta: continue
                if pd.api.types.is_datetime64_any_dtype(meta.series):
                    keys['datetime'] = k
                    break
            if not keys.get('datetime'): raise LookupError(f"No meta found with datetime dtype. {corpus.meta.keys()}")
        datetime_meta_key = keys.get('datetime')
        return cls.from_corpus_groups(corpus.slicer.group_by(datetime_meta_key, pd.Grouper(freq=freq)), use_custom_dtm)

    @classmethod
    def from_corpus_groups(cls, groups, use_custom_dtm: bool = False):
        """ Constructss ItemTimeline from corpus groups.
        :arg use_custom_dtm - use the cached custom dtm instead of default.
        """
        groups = list(groups)
        datetimes = []
        for dt, _ in groups:
            if type(dt) != pd.Timestamp: raise TypeError("Did you groupby a meta that is of type datetime?")
            datetimes.append(dt)

        if not use_custom_dtm:
            fts = [c.dtm.freq_table() for _, c in groups]
        else:
            fts = [c.custom_dtm.freq_table() for _, c in groups]
        return cls.from_freqtables(datetimes, fts)

    @classmethod
    def from_freqtables(cls, datetimes: Union[pd.Series, list], freqtables: list[FreqTable]):
        """ Constructs ItemTimeline using the specified freqtables.
        :arg datetimes - list of datetimes for each freqtable (converted using pd.to_datetime)
        """
        if len(datetimes) != len(freqtables):
            raise ValueError(f"Mismatched length of datetimes and freqtables. {len(datetimes)} and {len(freqtables)}.")
        fts_df = pd.concat([ft.series for ft in freqtables], axis=1).fillna(0).T
        datetimes = pd.to_datetime(pd.Series(datetimes))
        fts_df.reset_index(drop=True)
        fts_df.set_index(datetimes, inplace=True)
        return cls(df=fts_df)

    def __init__(self, df: pd.DataFrame):
        """ Initialise with a dataframe with a datetime index, item columns and values as metrics. """
        self._df: pd.DataFrame = df
        assert is_datetime64_dtype(self._df.index), "DataFrame Index must be datetime."
        self.datetimes = self._df.index.to_list()

        self.SORT_BY_PEAK = 'PEAK'
        self.SORT_BY_TOTAL = 'TOTAL'
        self.sort_bys = {
            self.SORT_BY_PEAK: partial(pd.DataFrame.max, axis=0),  # across datetime
            self.SORT_BY_TOTAL: partial(pd.DataFrame.sum, axis=0)
        }
        self.DEFAULT_SORT_BY = self.SORT_BY_TOTAL
        self.sort_by = self.DEFAULT_SORT_BY
        self._metric_series = None
        self.items = None

        # top items
        self.DEFAULT_NUM_TRACES = 30
        self.num_traces = self.DEFAULT_NUM_TRACES

        self.MAX_NUM_TRACES = 100

        # stop words
        self.no_stopwords = False

        # search bar states
        self.__first_search = True

        self._update_metrics(self.sort_by, self.num_traces, self.no_stopwords)

        # opacity
        self.FULL_OPACITY_TOP = 3  # top number of items with full opacity

        self.seed(42)
        self._rint = random.randint

    @staticmethod
    def seed(seed: int):
        """ Set the seed across all item timeline objects. """
        random.seed(seed)

    def set_sort_by(self, sort_by: Optional[str]):
        """ Sets the mode of the timeline as 'Peak' or 'Cumulative'. """
        # updates the items to display.
        if sort_by is None:
            self.sort_by = None
            self.items = self._df.columns.to_list()
        else:
            sort_by = sort_by.upper()
            if sort_by not in self.sort_bys.keys(): raise ValueError(
                f"{sort_by} not in {', '.join(self.sort_bys.keys())}")
            self.sort_by = sort_by
            self._update_metrics(self.sort_by, self.num_traces, self.no_stopwords)

    def set_top(self, top: int):
        if top < 1: raise ValueError(f"Must be > 1.")
        self.num_traces = top
        self._update_metrics(self.sort_by, self.num_traces, self.no_stopwords)

    def set_no_stopwords(self, no_stopwords: bool):
        if not isinstance(no_stopwords, bool): raise TypeError("no_stopwords must be a boolean.")
        self.no_stopwords = no_stopwords
        self._update_metrics(self.sort_by, self.num_traces, no_stopwords=self.no_stopwords)

    def _update_metrics(self, sort_by: str, top: int, no_stopwords: bool):
        metric_series = self.sort_bys.get(sort_by)(self._df)
        if no_stopwords:
            sw_in_metric_series = [item for item in metric_series.index.tolist() if item in ENGLISH_STOP_WORDS]
            metric_series = metric_series.drop(sw_in_metric_series, axis=0)
        metric_series.sort_values(ascending=False, inplace=True)
        metric_series = metric_series.iloc[:top]
        self._metric_series = metric_series
        self.items = self._metric_series.index.to_list()

    def widget(self):
        fig = self._build_main_figure()
        display(self._build_widgets(fig))
        return fig

    def _build_main_figure(self):
        fig = go.FigureWidget()
        fig.layout.showlegend = True  # even for single traces
        for tdatum in self._generate_trace_data():
            fig.add_trace(self._create_trace(tdatum))

        self._add_toggle_all_selection_layer(fig)
        # self._add_top_items_slider_layer(fig)
        return fig

    def _build_widgets(self, fig):
        trace_slider = self._create_num_traces_slider(fig)
        trace_slider.layout.width = '35%'
        sw_checkbox = self._create_stopwords_checkbox(fig)
        sw_checkbox.layout.width = '150px'
        sw_checkbox.style = {'description_width': '0px'}
        pad_box = widgets.Box(layout=widgets.Layout(width='5%'))
        sort_by_dropdown = self._create_dropdown_widget(fig)
        item_search = self._create_search_bar(fig)
        return widgets.HBox([trace_slider, sw_checkbox, pad_box, sort_by_dropdown, item_search],
                            layout=widgets.Layout(width='100%', height='40px'))

    @staticmethod
    def _create_trace(tdatum: TRACE_DATUM):
        return go.Scatter(
            x=tdatum.datetimes, y=tdatum.metrics,
            mode='lines+markers+text', marker_color=tdatum.colour,
            text=tdatum.texts, textposition='bottom center', textfont={'color': 'crimson'},
            name=tdatum.item,
        )

    def _generate_trace_data(self):
        """ Generates the trace content data from the current state (mode, top)"""
        trace_data = []
        for i, item in enumerate(self.items):
            tdatum = ItemTimeline.TRACE_DATUM(item=item, datetimes=self.datetimes, metrics=self._df.loc[:, item],
                                              colour=self._get_colour(item), texts=self._get_texts(item, i))
            trace_data.append(tdatum)
        return trace_data

    def _update_traces(self, fig):
        trace_data = self._generate_trace_data()

        if len(trace_data) > len(fig.data):
            start_idx = len(fig.data)
            for tdatum in trace_data[start_idx:]:
                fig.add_trace(self._create_trace(tdatum))
        with fig.batch_update():
            for i, trace in enumerate(fig.data):
                tdatum = trace_data[i]
                trace.name = f'{tdatum.item}'
                trace.y = tdatum.metrics
                trace.text = tdatum.texts

    def _create_dropdown_widget(self, fig):
        dropdown = widgets.Dropdown(
            options=[mode.capitalize() for mode in sorted(list(self.sort_bys.keys()))],
            value=self.sort_by.capitalize(),
            description='Sort by: ',
            disabled=False,
        )

        def observe_dropdown(event):
            self.set_sort_by(dropdown.value.upper())
            self._update_traces(fig)

        dropdown.observe(observe_dropdown)
        return dropdown

    def _create_search_bar(self, fig):
        """ Create the search bar to filter for items. """
        search_bar = widgets.Text(description='Search: ')

        @debounce(0.1)
        def observe_search(event):
            query = event.get('new')
            if self.__first_search:
                # deselect all -- this is needed for intuitive search. i.e. when searching for multiple items.
                self.__first_search = False
                with fig.batch_update():
                    for trace in fig.data: trace.visible = 'legendonly'
            with fig.batch_update():
                for trace in fig.data:
                    if query.upper() == trace.name.upper():
                        trace.visible = True
                    elif query.upper() in trace.name.upper():
                        trace.visible = 'legendonly' if trace.visible is not True else True
                    else:
                        trace.visible = False if trace.visible is not True else True

        search_bar.observe(observe_search, names='value')
        return search_bar

    def _create_num_traces_slider(self, fig):
        """ Create a slider to control the number of traces on the plot. """
        slider = widgets.IntSlider(value=self.DEFAULT_NUM_TRACES, min=self.DEFAULT_NUM_TRACES, max=self.MAX_NUM_TRACES,
                                   description="More data: ")

        @debounce(0.5)
        def observe_slider(event):
            num_traces = event.get('new')
            self.set_top(num_traces)
            self._update_traces(fig)

        slider.observe(observe_slider, names='value')
        return slider

    def _create_stopwords_checkbox(self, fig):
        sw_checkbox = widgets.Checkbox(description='Remove stopwords')
        sw_checkbox.value = self.no_stopwords

        def observe_checkbox(event):
            self.set_no_stopwords(event.get('new'))
            self._update_traces(fig)

        sw_checkbox.observe(observe_checkbox, names='value')
        return sw_checkbox

    @staticmethod
    def _add_toggle_all_selection_layer(fig):
        """ Adds a layer to select/deselect all the traces of the timeline. """
        fig.update_layout(dict(updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=["visible", True],
                        label="Select All",
                        method="restyle",
                    ),
                    dict(
                        args=[{"visible": ['legendonly'] * len(fig.data)}],
                        label="Deselect All",
                        method="restyle",
                    ),
                ]),
                pad={"r": 1, "t": 1},
                showactive=False,
                x=1,
                xanchor="right",
                y=1.1,
                yanchor="top",
                font=dict(size=12)
            ),
        ]
        ))

    def _add_top_items_slider_layer(self, fig):
        steps = []
        for i in reversed(range(len(fig.data))):
            step = dict(
                method='update',
                args=[{'visible': [True if j <= i else 'legendonly' for j in range(len(fig.data))]}, ],
                # {'title': self._get_title(i + 1)}],
                label=f'{i + 1}',
            )
            steps.append(step)

        sliders = [dict(
            active=self.num_traces,
            currentvalue={'prefix': 'Top: '},
            pad={'t': 25},
            steps=steps
        )]
        # pad = {'t': 20}
        fig.update_layout(sliders=sliders)
        return fig

    def _get_colour(self, item) -> TPLOTLY_RGB_COLOUR:
        r, g, b = self._get_rgb(item)
        opacity = self._get_opacity(item)
        return f'rgba({r},{g},{b},{opacity})'

    def _get_rgb(self, item: str):
        rint = self._rint
        h = hash(item)
        return (h * rint(0, 10)) % 256, (h * rint(0, 10)) % 256, (h * rint(0, 10)) % 256

    def _get_opacity(self, item):
        # no modes selected
        if self.sort_by is None: return 1.0
        else:
            # top
            idx = self._metric_series.index.get_loc(item)
            if idx < self.FULL_OPACITY_TOP: return 1.0

            # gradient
            metric = self._metric_series.loc[item]
            if metric > self._metric_series.quantile(0.5): return 0.4
            return 0.1

    def _get_title(self, idx):
        return f'Top {idx} {self.sort_by.capitalize()} items'

    def _get_texts(self, item: str, idx: int):
        """ Return the annotation when mouse is hovered over the series."""
        number = self._metric_series.loc[item]
        if idx >= self.FULL_OPACITY_TOP:
            idx = -1  # i.e. no text annotation for this trace.
        elif self.sort_by == self.SORT_BY_PEAK:
            idx = self._df.loc[:, item].argmax()
        elif self.sort_by == self.SORT_BY_TOTAL:
            idx = len(self.datetimes) - 1
        else:
            raise RuntimeError(
                f"Unsupported Mode. {self.sort_by} not in {self.sort_bys.keys()}. This should not happen.")
        return ['' if i != idx else str(number) for i in range(len(self.datetimes))]
