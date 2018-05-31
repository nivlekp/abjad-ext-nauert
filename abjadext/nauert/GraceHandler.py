import abc
import abjad


class GraceHandler(abjad.AbjadObject):
    r'''Abstract grace-handler.

    Determines what pitch, if any, will be selected from a list of
    ``QEvents`` to be applied to an attack-point generated by a ``QGrid``,
    and whether there should be a ``GraceContainer`` attached to th
    at attack-point.

    When called on a sequence of ``QEvents``, ``GraceHandler``
    subclasses should return a pair, where the first item of the pair
    is a sequence of pitch tokens or ``None``, and where the
    second item of the pair is a ``GraceContainer`` instance or None.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, q_events):
        r'''Calls grace handler.
        '''
        raise NotImplementedError
