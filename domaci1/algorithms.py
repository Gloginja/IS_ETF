import random
import time
import bisect
from functools import cmp_to_key
import config


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions


class BreadthFirstSearch(Algorithm):

    def get_steps(self, initial_state, goal_state):
        fifo = [initial_state]
        actions_dict = {initial_state: []}
        while len(fifo) != 0:
            state = fifo.pop(0)
            if state == goal_state:
                break
            legal_actions = self.get_legal_actions(state)
            for action in legal_actions:
                new_state = self.apply_action(state, action)
                if new_state not in actions_dict.keys():
                    fifo.append(new_state)
                    actions_dict[new_state] = actions_dict[state] + [action]
        try:
            return actions_dict[goal_state]
        except KeyError:
            return None


class BestFirstSearch(Algorithm):
    def custom_sort_for_best(self, a, b):
        heuristic_a = self.heuristic.get_evaluation(a)
        heuristic_b = self.heuristic.get_evaluation(b)
        if heuristic_a > heuristic_b:
            return 1
        elif heuristic_a == heuristic_b:
            for i, j in zip(a, b):
                if i > j:
                    return 1
            return 0
        else:
            return -1

    def get_steps(self, initial_state, goal_state):
        heuristic_list = [initial_state]
        actions_dict = {initial_state: []}
        custom_sort_py3 = cmp_to_key(self.custom_sort_for_best)
        while len(heuristic_list) != 0:
            state = heuristic_list.pop(0)
            if state == goal_state:
                break
            legal_actions = self.get_legal_actions(state)
            for action in legal_actions:
                new_state = self.apply_action(state, action)
                if new_state not in actions_dict.keys():
                    bisect.insort(heuristic_list, new_state,
                                  key=custom_sort_py3)  # lambda x: self.heuristic.get_evaluation(x))
                    # heuristic_list.append(new_state)
                    # heuristic_list.sort(key=custom_sort_py3)
                    actions_dict[new_state] = actions_dict[state] + [action]
        try:
            return actions_dict[goal_state]
        except KeyError:
            return None


class Astar(Algorithm):

    def __init__(self,heuristic):
        super().__init__(heuristic)
        self.actions_dict = {}

    def custom_sort_for_astar(self, a, b):
        heuristic_a = self.heuristic.get_evaluation(a) + len(self.actions_dict[a])
        heuristic_b = self.heuristic.get_evaluation(b) + len(self.actions_dict[b])
        if heuristic_a > heuristic_b:
            return 1
        elif heuristic_a == heuristic_b:
            for i, j in zip(a, b):
                if i > j:
                    return 1
            return 0
        else:
            return -1

    def get_steps(self, initial_state, goal_state):
        heuristic_list = [initial_state]
        custom_sort_py3 = cmp_to_key(self.custom_sort_for_astar)
        self.actions_dict = {initial_state: []}
        while len(heuristic_list) != 0:
            state = heuristic_list.pop(0)
            if state == goal_state:
                break
            legal_actions = self.get_legal_actions(state)
            for action in legal_actions:
                new_state = self.apply_action(state, action)
                if new_state not in self.actions_dict.keys():
                    self.actions_dict[new_state] = self.actions_dict[state] + [action]
                    bisect.insort(heuristic_list, new_state,
                                  key=custom_sort_py3)  # lambda x: self.heuristic.get_evaluation(x))
                    # heuristic_list.append(new_state)
                    # heuristic_list.sort(key=custom_sort_py3)

        try:
            return self.actions_dict[goal_state]
        except KeyError:
            return None
