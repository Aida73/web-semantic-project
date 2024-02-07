from rdflib import *

# def ontologie_to_graph(ontologie):
#     graph_ontologie = Graph()
#     graph_ontologie.parse(ontologie, format='xml')
    
#     for sujet,predicat, objet in graph_ontologie:
#         print(f"Sujet: {sujet}, Prédicat: {predicat}, Objet: {objet}")
      
#     # print("\nGraphe RDF en format Turtle:")
#     # print(graph_ontologie.serialize(format="turtle").encode())  
    
# ontologie_to_graph('./exemples_ontologies/superhero.rdf')


# import networkx as nx
# import matplotlib.pyplot as plt
# from rdflib import Graph
# import os

# def load_rdf_from_xml(file_path):
#     g = Graph()
#     g.parse(file_path, format="xml")
#     return g

# def build_graph_from_rdf(ontology_graph):
#     graph = nx.DiGraph()

#     for s, p, o in ontology_graph:
#         subject = str(s)
#         predicate = str(p)
#         obj = str(o)

#         graph.add_node(subject)
#         graph.add_node(obj)
#         graph.add_edge(subject, obj, label=predicate)

#     return graph

# def visualize_graph(graph):
#     pos = nx.spring_layout(graph)
#     labels = nx.get_edge_attributes(graph, 'label')

#     nx.draw(graph, pos, with_labels=True, node_size=400, node_color="skyblue", font_size=6)
#     nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

#     plt.show()

# if __name__ == "__main__":
#     path=os.getcwd()
#     rdfxml_file = path + "/exemples_ontologies/superhero.rdf"
#     rdf_graph = load_rdf_from_xml(rdfxml_file)

#     ontology_digraph = build_graph_from_rdf(rdf_graph)

#     visualize_graph(ontology_digraph)

# import rdflib
# from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
# import networkx as nx
# import matplotlib.pyplot as plt

# url = 'https://www.w3.org/TeamSubmission/turtle/tests/test-30.ttl'

# g = rdflib.Graph()
# result = g.parse(url, format='turtle')

# G = rdflib_to_networkx_multidigraph(result)

# # Plot Networkx instance of RDF Graph
# pos = nx.spring_layout(G, scale=2)
# edge_labels = nx.get_edge_attributes(G, 'r')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
# nx.draw(G, with_labels=True)

# #if not in interactive mode for 
# plt.show()


import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, Literal

# Création du graphe d'ontologie
g = Graph()

# Exemple de triplets dans le graphe d'ontologie
#g.add((Literal("John"), Namespace("ontologie").aPourNom, Literal("John Doe")))
#g.add((Literal("John"), Namespace("ontologie").aPourAge, Literal(30)))
g.parse('http://purl.org/ontology/mo/')

# Création du graphe NetworkX
G = nx.Graph()

# Ajouter les triplets au graphe NetworkX
for sujet, propriete, objet in g:
    G.add_node(str(sujet))
    G.add_node(str(objet))
    G.add_edge(str(sujet), str(objet), label=str(propriete))

# Visualiser le graphe
pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, 'label')
nx.draw(G, pos, with_labels=True, node_size=1700, node_color="skyblue",)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels,font_size=5)
plt.show()
