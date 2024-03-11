import re
import copy
import networkx as nx
import matplotlib.pyplot as plt

class GrammarConverter:

    non_terminals = []
    terminals = []
    productions = []

    def __init__(self):
        pass


class Automaton:

    states = []
    alphabet = []
    initial_state = []
    final_states = []
    transitions = {}

    def __init__(self):
        self.states = ["q0", "q1", "q2", "q3"]
        self.alphabet = ["a", "b", "c"]
        self.initial_state = "q0"
        self.final_states = "q3"
        self.transitions = {
            "q0": ["a q0", "a q1"],
            "q1": ["b q1", "a q2"],
            "q2": ["b q3", "a q0"],
            "q3": []
        }

    def is_det(self) -> bool:
        for state, transitions in self.transitions.items():
            symbols = []

            for transition in transitions:
                symbols.append(transition[0])
            if len(symbols) != len(set(symbols)):
                return False

        return True

    def to_grammar(self) -> GrammarConverter:
        grammar = GrammarConverter()

        grammar.non_terminals = self.states
        grammar.terminals = self.alphabet
        grammar.productions = self.transitions

        return grammar

    def nfa_to_dfa(self):
        if self.is_det():
            return
        dfa = Automaton()

        chars_pattern = re.compile(r'^(.*?)\s')
        states_pattern = re.compile(r'\s(.*)$')

        transitions = {self.initial_state: self.group_states(self.transitions[self.initial_state])}

        finished_states = []
        last_state = ""

        while not (self.has_all_states(transitions)):

            transitions_copy = copy.deepcopy(transitions)
            for value in finished_states:
                del transitions_copy[value]

            for key, values in transitions_copy.items():
                symbols = []
                states = []
                for value in values:
                    symbols.append(chars_pattern.search(value).group(1))
                    states.append(states_pattern.search(value).group(1))

                if not (len(symbols) == len(set(symbols))):
                    unique_symbols = set(symbols)
                    for element in unique_symbols:
                        positions = [i for i, value in enumerate(symbols) if value == element]
                        if len(positions) > 1:
                            new_state = ""
                            new_state_trans = []
                            for position in positions:
                                if states[position] not in new_state:
                                    new_state += states[position]
                                for state1 in self.degroup_states(states[position]):
                                    for elem in self.transitions[state1]:
                                        if elem not in new_state_trans:
                                            new_state_trans.append(elem)

                            if new_state in transitions:
                                break

                            transitions[new_state] = self.group_states(new_state_trans)
                            last_state = new_state

                for state in states:
                    if state not in transitions:
                        new_state_trans = []
                        new_states = self.degroup_states(state)
                        for new_state in new_states:
                            for trans in self.transitions[new_state]:
                                if trans not in new_state_trans:
                                    new_state_trans.append(trans)
                        new_state_trans = self.group_states(new_state_trans)
                        transitions[state] = new_state_trans
                        last_state = state

                finished_states.append(key)

        finished_states.append(last_state)
        dfa.states = finished_states
        dfa.final_states = []
        for state in dfa.states:
            if self.final_states in state:
                dfa.final_states.append(state)
        dfa.transitions = transitions

        return dfa

    def group_states(self, states_arr) -> []:
        chars_pattern = re.compile(r'^(.*?)\s')
        states_pattern = re.compile(r'\s(.*)$')
        states_arr.sort()
        for i in range(len(states_arr) - 1, 0, -1):
            if chars_pattern.search(states_arr[i]).group(
                    1) == chars_pattern.search(states_arr[i - 1]).group(1):
                temp = states_pattern.search(states_arr[i]).group(1) + \
                       states_pattern.search(states_arr[i - 1]).group(1)
                states_arr[i - 1] = chars_pattern.search(states_arr[i - 1]) \
                                                 .group(1) + " " + temp
                states_arr.pop(i)

        return states_arr

    def degroup_states(self, states) -> []:
        degrouped_states = []
        current_state = ""

        for char in states:
            current_state += char
            if current_state in self.states:
                degrouped_states.append(current_state)
                current_state = ""

        return degrouped_states

    def has_all_states(self, dictionary):
        states_pattern = re.compile(r'\s(.*)$')

        for key, values in dictionary.items():
            for value in values:
                state = states_pattern.search(value).group(1)

                if state not in dictionary:
                    return False
        return True

    def draw_automaton(self):
        graph = nx.DiGraph()

        for node, edges in self.transitions.items():
            for edge in edges:
                label, target = edge.split(' ', 1)
                graph.add_edge(node, target, label=label)
                if node == target:
                    label = "           " + label
                    graph.add_edge(node, target, label=label)

        pos = nx.planar_layout(graph)
        labels = nx.get_edge_attributes(graph, 'label')
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color="red", font_size=6)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='black', font_size=12)
        plt.show()


automaton = Automaton()
dfa = automaton.nfa_to_dfa()
print(dfa.transitions)
print(dfa.final_states)
print(dfa.states)
print(dfa.is_det())
dfa.draw_automaton()
