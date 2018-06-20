from abjadext.nauert.Heuristic import Heuristic


class DistanceHeuristic(Heuristic):
    r'''Distance heuristic.

    Considers only the computed distance of each ``QGrid`` and the number of
    leaves of that ``QGrid`` when choosing the optimal ``QGrid`` for a given
    ``QTargetBeat``.

    The ``QGrid`` with the smallest distance and fewest number of
    leaves will be selected.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _process(self, q_target_beats):
        import abjadext.nauert
        for q_target_beat in q_target_beats:
            q_grids = q_target_beat.q_grids
            if q_grids:
                sorted_q_grids = sorted(
                    q_grids, key=lambda x: (x.distance, len(x.leaves)))
                q_target_beat._q_grid = sorted_q_grids[0]
            else:
                q_target_beat._q_grid = abjadext.nauert.QGrid()
        return q_target_beats