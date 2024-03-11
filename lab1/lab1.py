import random

class Grammar:
    """Represents a context-free grammar."""

    def __init__(self, variables, terminals, productions, start_symbol):
        """Initialize the grammar components."""
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def generate_string(self):
        """Generates a string by randomly expanding the start symbol based on the grammar's productions."""

        def expand(symbol):
            if symbol in self.terminals:
                return symbol
            if symbol not in self.productions:
                return ''
            prod = random.choice(self.productions[symbol])
            return ''.join(expand(sym) for sym in prod)

        return expand(self.start_symbol)


class FiniteAutomaton:
    """Represents a deterministic finite automaton."""

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        """Initialize the finite automaton components."""
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def string_belongs_to_language(self, input_string):
        """Checks if the given string is accepted by the automaton."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False  # Reject strings with symbols not in the automaton's alphabet
            if symbol in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][symbol]
            else:
                return False
        return current_state in self.accept_states


# Initialize grammar and finite automaton with given components
variables = ['S', 'A', 'B', 'C']
terminals = ['a', 'b', 'c', 'd']
productions = {
    'S': ['dA'],
    'A': ['aB', 'bA'],
    'B': ['bC', 'aB', 'd'],
    'C': ['cB']
}
start_symbol = 'S'
my_grammar = Grammar(variables, terminals, productions, start_symbol)

# Generate and print valid strings from the grammar
print("A list of valid strings: ")
for _ in range(10):
    print(my_grammar.generate_string())

# Define the finite automaton's components
states = {'S', 'A', 'B', 'C'}
alphabet = {'a', 'b', 'c', 'd'}
transition_function = {
    'S': {'d': 'A'},
    'A': {'a': 'B', 'b': 'A'},
    'B': {'b': 'C', 'a': 'B', 'd': 'D'},
    'C': {'c': 'B'}
}
start_state = 'S'
accept_states = {'D'}

# Initialize finite automaton
fa = FiniteAutomaton(states, alphabet, transition_function, start_state, accept_states)

# Test and print whether each string is accepted by the automaton
test_strings = [
    'dad',
    'dbc',
    'dac',
    'dab',
    'daad',
    'dbb',
    'daabb',
    'daab',
    'dd',
    'aaa',
    'dcc',
    'aaaa',
    'bbbb',
    'ddd',
    'dadc',
    'daabc',
    'dabcd',
    'daacb',
    'dacd',
    'dbca'
]

# Test and print whether each string is accepted by the automaton
for string in test_strings:
    if fa.string_belongs_to_language(string):
        print(f"The string '{string}' is accepted by the automaton.")
    else:
        print(f"The string '{string}' is not accepted by the automaton.")
