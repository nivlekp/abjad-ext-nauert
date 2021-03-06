import abjad

from .AttackPointOptimizer import AttackPointOptimizer


class NaiveAttackPointOptimizer(AttackPointOptimizer):
    """
    Naive attack-point optimizer.

    Optimizes attack points by fusing tie leaves within logical ties with leaf
    durations decreasing monotonically.

    Logical ties will be partitioned into sub-logical-ties if leaves are found
    with metronome marks attached.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls naive attack-point optimizer.

        Returns none.
        """
        for logical_tie in abjad.iterate(argument).logical_ties(
            grace=False, reverse=True
        ):
            sub_logical_ties = []
            current_sub_logical_tie = []
            for leaf in logical_tie:
                tempos = leaf._get_indicators(abjad.MetronomeMark)
                if tempos:
                    if current_sub_logical_tie:
                        current_sub_logical_tie = abjad.LogicalTie(
                            current_sub_logical_tie
                        )
                        sub_logical_ties.append(current_sub_logical_tie)
                    current_sub_logical_tie = []
                current_sub_logical_tie.append(leaf)
            if current_sub_logical_tie:
                current_sub_logical_tie = abjad.LogicalTie(current_sub_logical_tie)
                sub_logical_ties.append(current_sub_logical_tie)
            for sub_logical_tie in sub_logical_ties:
                abjad.mutate._fuse_leaves_by_immediate_parent(sub_logical_tie)
