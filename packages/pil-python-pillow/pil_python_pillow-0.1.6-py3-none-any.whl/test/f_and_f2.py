from collections import defaultdict

# Function to calculate FIRST sets
def calculate_first(grammar):
    first = defaultdict(set)

    def first_of(symbol):
        if not symbol.isupper():  # Terminal
            return {symbol}
        if symbol in first and first[symbol]:
            return first[symbol]
        for production in grammar[symbol]:
            for char in production:
                first[symbol] |= first_of(char)
                if 'ε' not in first_of(char):
                    break
                else:
                    first[symbol].discard('ε')
            else:
                first[symbol].add('ε')
        return first[symbol]

    for non_terminal in grammar:
        first_of(non_terminal)

    return first

# Function to calculate FOLLOW sets
def calculate_follow(grammar, start_symbol, first):
    follow = defaultdict(set)
    follow[start_symbol].add('$')  # Start symbol gets end marker

    def follow_of(symbol):
        for lhs, productions in grammar.items():
            for production in productions:
                for i, char in enumerate(production):
                    if char == symbol:
                        if i + 1 < len(production):  # Check next symbol
                            follow[symbol] |= first[production[i + 1]] - {'ε'}
                        if i + 1 == len(production) or 'ε' in first[production[i + 1]]:
                            follow[symbol] |= follow_of(lhs)
        return follow[symbol]

    for non_terminal in grammar:
        follow_of(non_terminal)

    return follow

# Example Grammar
grammar = {
    'E': ['TX'],
    'X': ['+TX', 'ε'],
    'T': ['FY'],
    'Y': ['*FY', 'ε'],
    'F': ['(E)', 'id']
}

first = calculate_first(grammar)
follow = calculate_follow(grammar, 'E', first)

def generate_parse_table(grammar, first, follow):
    table = defaultdict(dict)

    for lhs, productions in grammar.items():
        for production in productions:
            for terminal in first[production[0]] - {'ε'}:
                table[lhs][terminal] = production
            if 'ε' in first[production[0]]:
                for terminal in follow[lhs]:
                    table[lhs][terminal] = production

    return table

# Generate parse table
parse_table = generate_parse_table(grammar, first, follow)
print("Parse Table:")
for non_terminal, rules in parse_table.items():
    print(f"{non_terminal}: {dict(rules)}")

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, symbol_type, value=None):
        self.symbols[name] = {
            'type': symbol_type,
            'value': value
        }

    def update_symbol(self, name, value):
        if name in self.symbols:
            self.symbols[name]['value'] = value

    def lookup(self, name):
        return self.symbols.get(name, None)

    def display(self):
        print("Symbol Table:")
        for name, attributes in self.symbols.items():
            print(f"{name}: {attributes}")

# Example usage
symbol_table = SymbolTable()
symbol_table.add_symbol('x', 'int', 10)
symbol_table.add_symbol('y', 'float')
symbol_table.update_symbol('y', 20.5)
symbol_table.display()


print("First Sets:", dict(first))
print("Follow Sets:", dict(follow))
