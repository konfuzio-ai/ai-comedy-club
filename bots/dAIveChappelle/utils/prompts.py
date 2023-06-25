

def get_prompts():
    prompts = []
    with open('bots/dAIveChappelle/config/prompts.txt', 'r') as f:
        for line in f:
            prompts.append(line.strip())
    return prompts
