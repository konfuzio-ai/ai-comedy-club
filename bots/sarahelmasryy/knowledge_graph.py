import networkx as nx
import pandas as pd

# Assume this is the most creative jokes 
df = pd.read_csv('df_chatgpt_jokes_clean.csv')
jokes = df['joke'].to_numpy()
# print(jokes)
# Create a directed graph to represent the knowledge graph
knowledge_graph = nx.DiGraph()


# Add jokes as nodes in the graph
knowledge_graph.add_nodes_from(jokes)

# Save the knowledge graph to a GML file
output_file = "creative_jokes_knowledge_graph.gml"
nx.write_gml(knowledge_graph, output_file)

print(f"Knowledge graph saved to {output_file}")
