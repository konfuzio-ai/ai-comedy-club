import pyjokes
import networkx as nx
import re 
import os


class Bot:
    def __init__(self, name):
        self.name = name
        
        
    def chat(self):
        print(f"Hello, I'm {self.name}! Type 'quit' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print(f"{self.name}: Goodbye!")
                break
            response = self.tell_joke()
            rating= self.rate_joke(response)
            print(f"{self.name}: {response}")
            print('rating: ' + str(rating))

    def tell_joke(self, user_profile=None):
        joke = self.generate_joke()
        return joke

    def generate_joke(self):
        joke = pyjokes.get_joke()
        return joke

    
    
    def is_style(self,joke):
        punctuation_pattern = r'[!,.\']'
        pattern = re.compile(punctuation_pattern, re.IGNORECASE)
        if pattern.search(joke):
            return 1
        return 0
    
    def is_creative(self,joke):
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        input_file= os.path.join(script_dir, 'creative_jokes_knowledge_graph.gml')
        knowledge_graph = nx.read_gml(input_file)
            # Iterate through the nodes (jokes) in the knowledge graph
        for node in knowledge_graph.nodes:
            # Check if the new text contains the joke (case-insensitive)
            if node.lower() in joke.lower():
                return 0
    # If no match is found
        return 1
    
    
    def rate_joke(self, joke):
        is_creative= self.is_creative(joke)
        is_style= self.is_style(joke)
        rating_metrics=[]
        rating_metrics.append(is_creative)
        rating_metrics.append(is_style)

        score= sum(rating_metrics) / len(rating_metrics)
        
        return score


