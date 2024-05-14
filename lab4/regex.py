import re
import itertools


def generate_combinations(regex, limit=3):
    def expand_group(part):
        return part.strip('()').split('|')

    quantifiers = {'*': (0, limit), '+': (1, limit), '?': (0, 1), '^': (1, 1)}

    def expand_quantifiers(part):
        if part[-1] in quantifiers:
            base = part[-1]
            min_rep, max_rep = quantifiers[part[-1]]
            return [base * i for i in range(min_rep, max_rep + 1)]
        elif part[-1] == '^':
            base = part[:-1]
            return [base * limit]
        elif '{' in part and '}' in part:
            base, quant = part.split('{')
            min_rep, max_rep = map(int, quant.strip('}').split(','))
            return [base * i for i in range(min_rep, max_rep + 1)]
        else:
            return [part]

    parts = re.split(r'(\([^()]*\)|\[\^?.+?\]|\.\*|\.\+|\.\?|\.[\d*+]|\{[^\}]+\}|.)', regex)
    parts = list(filter(None, parts))

    expanded = []
    for part in parts:
        if '(' in part and ')' in part:
            expanded.append(expand_group(part))
        else:
            expanded.append(expand_quantifiers(part))

    combinations = list(itertools.product(*expanded))

    strings = [''.join(combo) for combo in combinations]

    results = []

    for comb in strings:
        base = ''
        prev = ''
        for chr in comb:
            if chr == '+' or chr == '*':
                base += base[-1]
            elif chr == '?':
                base = base[:-1]
            elif prev == '^':
                base = base[:-1] + base[len(base) - 2] * int(chr)
            else:
                base += chr

            prev = chr

        results.append(base)

    return results


# Define regular expressions
regex1 = '(a|b)(c|d)E+G?'
regex2 = 'P(Q|R|S)T(UV|W|X)*Z+'
regex3 = '1(0|1)*2(3|4)^536'

# Generate combinations
combinations1 = generate_combinations(regex1)
combinations2 = generate_combinations(regex2)
combinations3 = generate_combinations(regex3)

print("Combinations for regex1:", list(set(combinations1)))
print("Combinations for regex2:", list(set(combinations2)))
print("Combinations for regex3:", list(set(combinations3)))


def process_regex(regex):
    steps = []

    def add_step(description):
        steps.append(description)

    parts = re.split(r'(\([^()]*\)|\[\^?.+?\]|\.\*|\.\+|\.\?|\.[\d*+]|\{[^\}]+\}|.)', regex)
    parts = list(filter(None, parts))

    for part in parts:
        if '(' in part and ')' in part:
            options = part.strip('()').split('|')
            add_step(f"Processing group: {part}")
            add_step(f"Expanding group into options: {options}")
        else:
            add_step(f"Processing part: {part}")
            if part[-1] in '*+?':
                quantifier = part[-1]
                base = part[:-1]
                add_step(f"Expanding quantifier '{quantifier}' for base '{base}'")
            elif part[-1] == '^':
                base = part[:-1]
                add_step(f"Expanding '{base}' to repeat {limit} times")
            elif '{' in part and '}' in part:
                base, quant = part.split('{')
                min_rep, max_rep = map(int, quant.strip('}').split(','))
                add_step(f"Expanding custom quantifier '{{{min_rep},{max_rep}}}' for base '{base}'")
            else:
                add_step(f"Literal match for '{part}'")

    return steps


# Example usage for regex1
steps = process_regex(regex1)
for step in steps:
    print(step)
