import abc
import copy

import abjad

from .QGrid import QGrid


class SearchTree:
    r"""Abstract search tree.

    ``SearchTrees`` encapsulate strategies for generating collections of
    ``QGrids``, given a set of ``QEventProxy`` instances as input.

    They allow composers to define the degree and quality of nested rhythmic
    subdivisions in the quantization output.  That is to say, they allow
    composers to specify what sorts of tuplets and ratios of pulses may be
    contained within other tuplets, to arbitrary levels of nesting.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_definition",)

    ### INITIALIZER ###

    def __init__(self, definition=None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self._is_valid_definition(definition)
        self._definition = definition

    ### SPECIAL METHODS ###

    def __call__(self, q_grid):
        r"""Calls search tree."""
        assert isinstance(q_grid, QGrid)
        new_q_grids = []
        commands = self._generate_all_subdivision_commands(q_grid)
        for command in commands:
            new_q_grid = copy.deepcopy(q_grid)
            q_events = new_q_grid.subdivide_leaves(command)
            new_q_grid.fit_q_events(q_events)
            new_q_grids.append(new_q_grid)
        return new_q_grids

    def __eq__(self, argument):
        r"""Is true when `argument` is a search tree with definition equal to that of
        this search tree. Otherwise false.

        Returns true or false.
        """
        if type(self) == type(argument):
            if self.definition == argument.definition:
                return True
        return False

    def __format__(self, format_specification="") -> str:
        """
        Formats object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self):
        r"""Hashes search tree.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super(SearchTree, self).__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _find_divisible_leaf_indices_and_subdivisions(self, q_grid):
        # TODO: This should actually check for all QEvents which fall
        # within the leaf's duration,
        # including QEvents attached to the next leaf
        # It may be prudent to actually store QEvents in two lists:
        # before_offset and after_offset
        indices, subdivisions = [], []
        leaves = list(q_grid.leaves)
        i = 0
        for leaf_one, leaf_two in abjad.sequence(leaves).nwise():
            if leaf_one.is_divisible:
                succeeding_proxies = leaf_one.succeeding_q_event_proxies
                preceding_proxies = leaf_two.preceding_q_event_proxies
                if not preceding_proxies and all(
                    proxy.offset == leaf_one.start_offset
                    for proxy in succeeding_proxies
                ):
                    pass  # proxies align perfectly with this leaf

                elif preceding_proxies or succeeding_proxies:
                    parentage_ratios = leaf_one.parentage_ratios
                    leaf_subdivisions = self._find_leaf_subdivisions(parentage_ratios)
                    if leaf_subdivisions:
                        indices.append(i)
                        subdivisions.append(tuple(leaf_subdivisions))
            i += 1
        return indices, subdivisions

    @abc.abstractmethod
    def _find_leaf_subdivisions(self, leaf):
        raise NotImplementedError

    def _generate_all_subdivision_commands(self, q_grid):
        indices, subdivisions = self._find_divisible_leaf_indices_and_subdivisions(
            q_grid
        )
        if not indices:
            return ()
        combinations = abjad.enumeratex.yield_outer_product(subdivisions)
        combinations = [tuple(_) for _ in combinations]
        return tuple(tuple(zip(indices, combo)) for combo in combinations)

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    @abc.abstractmethod
    def _is_valid_definition(self, definition):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def default_definition(self):
        r"""The default search tree definition.

        Returns dictionary.
        """
        raise NotImplementedError

    @property
    def definition(self):
        r"""The search tree definition.

        Returns dictionary.
        """
        return self._definition
