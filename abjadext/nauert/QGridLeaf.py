import uqbar.containers
import uqbar.graphs

import abjad

from .QEventProxy import QEventProxy


class QGridLeaf(abjad.rhythmtrees.RhythmTreeMixin, uqbar.containers.UniqueTreeNode):
    """
    Q-grid leaf.

    ..  container:: example

        >>> leaf = abjadext.nauert.QGridLeaf()
        >>> leaf
        QGridLeaf(
            preprolated_duration=Duration(1, 1),
            is_divisible=True
            )

    Used internally by ``QGrid``.
    """

    ### INITIALIZER ###

    def __init__(self, preprolated_duration=1, q_event_proxies=None, is_divisible=True):
        uqbar.containers.UniqueTreeNode.__init__(self)
        abjad.rhythmtrees.RhythmTreeMixin.__init__(self, preprolated_duration)
        if q_event_proxies is None:
            self._q_event_proxies = []
        else:
            assert all(isinstance(x, QEventProxy) for x in q_event_proxies)
            self._q_event_proxies = list(q_event_proxies)
        self._is_divisible = bool(is_divisible)

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        """
        Calls q-grid leaf.

        Returns selection of notes.
        """
        pulse_duration = abjad.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        maker = abjad.NoteMaker()
        return maker(0, total_duration)

    def __graph__(self, **keywords):
        """
        Graphviz graph of q-grid leaf.

        Returns Graphviz graph.
        """
        graph = uqbar.graphs.Graph(name="G")
        node = uqbar.graphs.Node(
            attributes={"label": str(self.preprolated_duration), "shape": "box"}
        )
        graph.append(node)
        return graph

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = abjad.StorageFormatManager(self)
        names = agent.signature_names
        template_names = names[:]
        if "q_event_proxies" in names and not self.q_event_proxies:
            names.remove("q_event_proxies")
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_keyword_names=names,
            template_names=template_names,
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.preprolated_duration)]

    ### PUBLIC PROPERTIES ###

    @property
    def is_divisible(self):
        """
        Flag for whether the node may be further divided
        under some search tree.
        """
        return self._is_divisible

    @is_divisible.setter
    def is_divisible(self, argument):
        self._is_divisible = bool(argument)

    @property
    def preceding_q_event_proxies(self):
        """
        Preceding q-event proxies of q-grid leaf.

        Returns list.
        """
        return [x for x in self._q_event_proxies if x.offset < self.start_offset]

    @property
    def q_event_proxies(self):
        """
        Q-event proxies of q-grid leaf.
        """
        return self._q_event_proxies

    @property
    def rtm_format(self):
        """
        RTM format of q-grid leaf.
        """
        return str(self.preprolated_duration)

    @property
    def succeeding_q_event_proxies(self):
        """
        Succeeding q-event proxies of q-grid leaf.

        Returns list.
        """
        return [x for x in self._q_event_proxies if self.start_offset <= x.offset]
