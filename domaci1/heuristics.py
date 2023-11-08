class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0


class HammingHeuristic(Heuristic):
    def get_evaluation(self, state):
        n = len(state)
        heuristic = 0
        num = 1
        for i in range(n - 1):
            if state[i] != 0 and state[i] != num:
                heuristic += 1
            num += 1
        return heuristic


class ManhattanHeuristic(Heuristic):
    def get_evaluation(self, state):
        n = len(state)
        distance_sum = 0
        for i in range(n - 1):
            if state[i] != 0:
                distance_sum += abs(i - state[i] + 1)
        return distance_sum
