class Grammar:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def remove_duplicates(self, array):
        unique_strings = set()
        result = []

        for string in array:
            if string not in unique_strings:
                result.append(string)
                unique_strings.add(string)

        return result

    def generate_strings_with_letter_removed(self, s, letter):
        strings = []
        count_b = s.count('B')
        for i in range(0, len(s)):
            if s[i] == letter:
                string = s[0:i] + s[i + 1:]
                strings.append(string)
                strings += self.generate_strings_with_letter_removed(string, letter)
        return strings

    def remove_empty_string(self):
        empty_symbols = []
        for symbol in self.productions:
            for transition in self.productions[symbol]:
                if transition == "":
                    if symbol not in empty_symbols:
                        empty_symbols.append(symbol)
            self.productions[symbol] = list(filter(lambda x: len(x) > 0, self.productions[symbol]))

        for empty_symbol in empty_symbols:
            for symbol in self.productions:
                transitions_to_change = []
                for transition in self.productions[symbol]:
                    if empty_symbol in transition:
                        transitions_to_change.append(transition)

                append_to_productions = []
                for trns in transitions_to_change:
                    append_to_productions += self.generate_strings_with_letter_removed(trns, empty_symbol)

                self.productions[symbol] += append_to_productions
                self.productions[symbol] = self.remove_duplicates(self.productions[symbol])

    def remove_inaccessible(self):
        reachable_symbols = [self.start_symbol]
        while True:
            symbol = reachable_symbols[len(reachable_symbols) - 1]
            found_something = False
            for trns in self.productions[symbol]:
                for i in trns:
                    if i in self.variables:
                        if i not in reachable_symbols:
                            found_something = True
                            reachable_symbols.append(i)

            if not found_something:
                break

        unreachable_symbols = []
        for i in self.variables:
            if i not in reachable_symbols:
                unreachable_symbols.append(i)
        for i in self.variables:
            if len(self.productions[i]) == 0 and i not in unreachable_symbols:
                unreachable_symbols.append(i)

        for symbol in self.productions:
            for idx in range(0, len(self.productions[symbol])):
                for i in unreachable_symbols:
                    self.productions[symbol][idx] = self.productions[symbol][idx].replace(i, "")

        for i in unreachable_symbols:
            del self.productions[i]
            self.variables.remove(i)

    def eliminate_unit_productions(self):
        while True:
            found_something = False
            for symbol in self.productions:
                for idx in range(0, len(self.productions[symbol])):
                    trns = self.productions[symbol][idx]
                    if len(trns) == 1 and trns in self.variables:
                        found_something = True
                        self.productions[symbol].pop(idx)
                        self.productions[symbol] += self.productions[trns]
            if not found_something:
                break

    def convert_to_chomsky_normal_form(self):
        lambda_symbol = "ε"
        new_nonterminals = {}
        k = 1
        for symbol in self.productions:
            for idx in range(0, len(self.productions[symbol])):
                trns = self.productions[symbol][idx]
                if len(trns) >= 2:
                    if len(trns) == 2:
                        cnt_nonterm = 0
                        for i in trns:
                            if i in self.variables:
                                cnt_nonterm += 1
                        if cnt_nonterm == 2:
                            continue

                    rest = self.productions[symbol][idx][1:]
                    nonterm_found = ""
                    for i in new_nonterminals:
                        if rest == new_nonterminals[i]:
                            nonterm_found = i
                            break
                    if nonterm_found == "":
                        new_nonterminals[lambda_symbol + str(k)] = rest
                        nonterm_found = lambda_symbol + str(k)
                        k += 1
                    self.productions[symbol][idx] = self.productions[symbol][idx].replace(rest, nonterm_found)

                    if self.productions[symbol][idx][0] in self.terminals:
                        term = self.productions[symbol][idx][0]
                        nonterm_found = ""
                        for i in new_nonterminals:
                            if term == new_nonterminals[i]:
                                nonterm_found = i
                                break
                        if nonterm_found == "":
                            new_nonterminals[lambda_symbol + str(k)] = term
                            nonterm_found = lambda_symbol + str(k)
                            k += 1
                        self.productions[symbol][idx] = self.productions[symbol][idx].replace(term, nonterm_found)

        self.productions.update(new_nonterminals)

    def transform_to_chomsky_normal_form(self):
        self.remove_empty_string()
        self.remove_inaccessible()
        self.eliminate_unit_productions()
        self.remove_inaccessible()
        print(self.productions)
        self.convert_to_chomsky_normal_form()
        print(self.productions)


variables = {"S", "A", "B", "C", "D", "E"}
terminals = {"a", "b"}
start_symbol = "S"

productions = {
    "S": ["aA", "AC"],
    "A": ["a", "ASC", "BC", "aD"],
    "B": ["b", "bA"],
    "C": ["ε", "BA"],
    "D": ["abC"],
    "E": ["aB"]
}

grammar = Grammar(variables, terminals, productions, start_symbol)

grammar.transform_to_chomsky_normal_form()