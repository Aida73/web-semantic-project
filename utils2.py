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
                ex:name "IDF" ;
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

    return G


def visualization(input):
    G = input
    # Définir les positions des nœuds pour le dessin
    pos = nx.spring_layout(G,seed=42)

    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=8, font_weight='bold')
    plt.show()


def get_triplets(G: Graph):
    from rdflib import Graph, URIRef, Literal, Namespace, RDF
    rdf_graph = Graph()
    ex = Namespace("http://example.org/")

    # Ajouter les nœuds en tant que ressources dans le graphe RDF
    for node in G.nodes():
        node_uri = URIRef(ex[node])
        rdf_graph.add((node_uri, RDF.type, ex.Node))

        # Ajouter d'autres propriétés du nœud en tant que triplets
        for key, value in G.nodes[node].items():
            property_uri = URIRef(ex[key])
            rdf_graph.add((node_uri, property_uri, Literal(value)))

    # Ajouter les arêtes en tant que triplets dans le graphe RDF
    for edge in G.edges():
        source_uri = URIRef(ex[edge[0]])  # URI pour le nœud source
        target_uri = URIRef(ex[edge[1]])  # URI pour le nœud cible
        rdf_graph.add((source_uri, ex.hasEdge, target_uri))  # Ajouter un triplet pour l'arête
    
    # Trouver les triplets
    query_trp = """
    SELECT ?s ?p ?o
    WHERE {
    ?s ?p ?o .
    }
    """
    return rdf_graph.query(query_trp)


def get_literals(triplets):
    literals=[]
    for subj, pred, obj in triplets:
        if isinstance(obj, Literal):
            literals.append(obj.value)
    return literals

# Générer la requête
def generate_query(source_literals):
    # Définir les préfixes
    prefixes = "PREFIX ex: <http://example.org/>\n"

    # Initialiser la partie WHERE de la requête
    where_clause = "WHERE {\n"
    
    # Initialiser les variables à extraire
    select_vars = []
    mylist={}
    # Parcourir les triplets pour construire la requête
    for literal in list(set(source_literals)):
        # Vérifier si le littéral est un nom de ville, etudiant, cite
        if literal == "student":
            # Ajouter le pattern pour l'étudiant et son université
            triple = "?student ex:name ?studentName ; ex:studiesAt ?university ."
            # Ajouter la variable à extraire
            select_vars.append("?studentName")
            mylist[1]=triple
        if literal == "university":

            triple="?university ex:name ?universityName ; ex:locatedIn ?city ."
            # Ajouter la variable à extraire
            select_vars.append("?universityName")
            mylist[2]=triple
        if literal == "city":
            # Ajouter le filtre pour la ville
            where_clause += f"  ?city ex:name ?cityName .\n"
            # Ajouter la variable à extraire
            select_vars.append("?cityName")
            triple="?city ex:name ?cityName ."
            mylist[3]=triple
    # Construction de la clause where
    triplets=list(collections.OrderedDict(sorted(mylist.items())).values())
    for triplet in triplets:
        where_clause += f"\t{triplet}\n"
    where_clause += "}"

    # Construire la requête complète
    query = prefixes + "SELECT " + " ".join(list(set(select_vars))) + "\n" + where_clause
    return query


