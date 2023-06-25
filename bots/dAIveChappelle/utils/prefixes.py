

def get_prefixes():
    jokes_prefixes = []
    with open('bots/dAIveChappelle/config/prefixes.txt', 'r') as f:
        for line in f:
            jokes_prefixes.append(line.strip())
    return jokes_prefixes
