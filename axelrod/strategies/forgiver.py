from axelrod import Player


class Forgiver(Player):
    """
    A player starts by cooperating however will defect if at any point
    the opponent has defected more than 10 percent of the time
    """

    name = 'Forgiver'
    memory_depth = float('inf')  # Long memory

    @staticmethod
    def strategy(opponent):
        """
        Begins by playing C, then plays D if the opponent has defected more than 10 percent of the time
        """
        try:
            if opponent.history.count('D') > len(opponent.history) / 10.:
                return 'D'
            return 'C'
        except IndexError:
            return 'C'


class ForgivingTitForTat(Player):
    """
    A player starts by cooperating however will defect if at any point,
    the opponent has defected more than 10 percent of the time,
    and their most recent decision was defect.
    """

    name = 'Forgiving Tit For Tat'
    memory_depth = float('inf')  # Long memory

    @staticmethod
    def strategy(opponent):
        """
        Begins by playing C, then plays D if,
        the opponent has defected more than 10 percent of the time,
        and their most recent decision was defect.
        """
        try:
            if opponent.history.count('D') > len(opponent.history) / 10.:
                return opponent.history[-1]
            return 'C'
        except IndexError:
            return 'C'