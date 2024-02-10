from rdflib import Graph, URIRef, RDF, Literal, FOAF, Namespace
import networkx as nx
import matplotlib.pyplot as plt
import collections


g=Graph()
graphe = g.parse("exemples_ontologies/exemple3.rdf")

def get_graph_input():
    query = """
        PREFIX ex: <http://example.org/>

        Select ?studentName ?universityName ?cityName
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
    results =  graphe.query(query)
    # Créer le graphe
    G = nx.Graph()
    # Parcourir les résultats de la requête SPARQL et ajouter les nœuds et les arêtes
    for row in results:
        student_name, university_name, city_name = row
        G.add_node(student_name, type='student')
        G.add_node(university_name, type='university')
        G.add_node(city_name, type='city')
        G.add_edge(student_name, university_name, relation="studentAt", length=100)
        G.add_edge(university_name, city_name, relation="locatedIn", length=30)
    
    results.serialize("input_graphe.rdf", format="xml")

    return G


if __name__=='__main__()':
    pass