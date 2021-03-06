import abc

import abjad

from .SearchTree import SearchTree


class QSchemaItem:
    """
    Abstract q-schema item.

    Represents a change of state in the timeline of a quantization process.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_search_tree", "_tempo")

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, search_tree=None, tempo=None):
        if search_tree is not None:
            assert isinstance(search_tree, SearchTree)
        self._search_tree = search_tree
        if tempo is not None:
            if isinstance(tempo, tuple):
                tempo = abjad.MetronomeMark(*tempo)
            assert not tempo.is_imprecise
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=""):
        """
        Formats q schema item.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        """
        if format_specification in ("", "storage"):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def search_tree(self):
        """
        The optionally defined search tree.

        Returns search tree or none.
        """
        return self._search_tree

    @property
    def tempo(self):
        """
        The optionally defined tempo.

        Returns tempo or none.
        """
        return self._tempo
