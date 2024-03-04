from rdflib import Graph, URIRef, RDF, Literal, FOAF, Namespace
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

from rdflib import Graph, Namespace
import networkx as nx
import matplotlib.pyplot as plt

def create_subgraph(graph, results):
    subgraph = Graph()
    for row in results:
        student_name, university_name, city_name = row
        # Add triples matching the query results to the subgraph
        for triple in graph.triples((student_name, None, None)):
            subgraph.add(triple)
        for triple in graph.triples((university_name, None, None)):
            subgraph.add(triple)
        for triple in graph.triples((None, None, university_name)):
            subgraph.add(triple)
        for triple in graph.triples((None, None, city_name)):
            subgraph.add(triple)
    return subgraph

# Load the RDF graph
g = Graph()
graphe = g.parse("exemples_ontologies/exemple3.rdf")

# Execute the SPARQL query
query = """
    PREFIX ex: <http://example.org/>

    SELECT ?studentName ?universityName ?cityName
    WHERE {
        ?student rdf:type ex:Student ;
                 ex:name ?studentName ;
                 ex:studiesAt ?university .

        ?university rdf:type ex:University ;
                    ex:name ?universityName ;
                    ex:locatedIn ?city .

        ?city rdf:type ex:City ;
              ex:name "Nantes" ;
              ex:name ?cityName .
    }
"""
results = graphe.query(query)

# Create the subgraph based on the query results
subgraph = create_subgraph(graphe, results)

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10)
    plt.title("Subgraph Visualization")
    plt.show()  


if __name__=='__main__':
    print("starting")
    # Utiliser la fonction pour sauvegarder le graphe G dans un fichier RDF
    #save_graph_as_rdf(get_graph_input(), "data/graph/graph_output.rdf")
    #print()
    subgraph = create_subgraph(graphe, results)
    visualize_graph(create_subgraph(graphe, results))

