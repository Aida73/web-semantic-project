from rdflib import Graph, URIRef, RDF, Literal, FOAF, Namespace
import networkx as nx
import matplotlib.pyplot as plt
import collections

def get_graph_input():
    g=Graph()
    graphe = g.parse("exemples_ontologies/exemple3.rdf")
    """
        Fonction pour creer notre graphe d'entree (ceci est dans le cadre du test)
        On suppose qu'on a à notre disposition notre BD(rdf contenant des données sur 
        les etudiants, les etudiants et les villes d'etudes)
    """
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
    """
        Cette fonction prend en entrée un graphe 
        Et permet la visualisation delui-ci.
    """
    G = input
    pos = nx.spring_layout(G,seed=42)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=8, font_weight='bold')
    plt.show()


def get_triplets(G: Graph):
    """
        Cette fonction nous permet de récupérer
        les triplets de notre graphe d'entrée
    """
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
    """
        Input: liste de triplets RDF au format (sujet, prédicat, objet)
        Output: liste contenant les valeurs littérales des objets dans les triplets
        Methode: Extraire les valeurs littérales des objets dans une liste de triplets RDF.
            Pour chaque triplet, elle vérifie si l'objet est une instance de la classe Literal,
            ce qui signifie qu'il s'agit d'une valeur littérale.
            Si l'objet est une valeur littérale, elle extrait sa valeur à l'aide de l'attribut value
            et l'ajoute à la liste literals.
            Enfin, elle retourne la liste contenant toutes les valeurs littérales des objets trouvées
            dans les triplets.
            La fonction parcourt chaque triplet dans la liste triplets.
    """
    literals=[]
    for _, _, obj in triplets:
        if isinstance(obj, Literal):
            literals.append(obj.value)
    return literals


def get_propriete_values(triplets,propriete):
    """
        Obj:    Trouver la valeur des propriétés pour peupler la clause FILTER 
        Input:  Une liste de triplets RDF au format (sujet, prédicat, objet)
                La propriété pour laquelle nous voulons extraire les valeurs
        Output: Une liste des valeurs associées à la propriété spécifiée.
        Méthode: La fonction parcourt chaque triplet dans la liste triplets.
                Pour chaque triplet, elle vérifie si le prédicat correspond à la propriété spécifiée 
                et si l'objet est une valeur littérale égale à propriete.
                Si ces conditions sont remplies, elle extrait la valeur du sujet du triplet
                (en supprimant l'URL du sujet)
                et l'ajoute à un set (values) pour éliminer les doublons
    """
    values = set()
    for triplet in triplets:
        # Vérifier si le triplet correspond à la propriété donnée
        if triplet[1] == URIRef('http://example.org/type') and triplet[2] == Literal(propriete):
            # Ajouter la valeur du sujet à la liste des valeurs de city
            values.add(triplet[0].toPython().split('/')[-1])

    return list(values)


def get_filters(filters):
    """
        Pour construire la clause Filter de la requete, s'il y'en a:
        On récupère toutes les valeurs des objets pour la propriété x dans
        les triplets, en procédant comme suit :
        - Parcourir les triplets.
        - Filtrer les triplets où la propriété est égale à *ex:type* et où la valeur de 
            l'objet est un littéral égal à 'x'.
        - Collecter toutes les valeurs des sujets de ces triplets.
    """
    if len(filters.items())>0:
        filter_temp = ""
        for key, values in filters.items():
            if len(values) > 0:
                temp = f"FILTER ("
                for el in values:
                    if key == 1:
                        temp += f"?studentName = {el} || "
                    elif key == 2:
                        temp += f"?universityName = {el} || "
                    elif key == 3:
                        temp += f"?cityName = {el} || "
                filter_expr = temp[:-4] + ")\n" 
                filter_temp += filter_expr
        return filter_temp
    return ""



def generate_query(graph: Graph, output_format: str):

    triplets = get_triplets(graph)
    source_literals = get_literals(triplets)
    """
        Cette fonction est conçue pour être générique et générer une requête SPARQL adaptée aux informations
        présentes dans le graphe RDF, en s'assurant d'inclure uniquement les éléments nécessaires à partir 
        des valeurs littérales détectées.

        Input: un graphe RDF. 

        Elle extrait les triplets du graphe et les valeurs
        littérales des objets de ces triplets. En fonction des valeurs littérales détectées
        (par exemple "student", "university", "city"), elle construit dynamiquement une requête SPARQL.
        Pour chaque type d'entité détecté, elle ajoute les patterns correspondants aux triplets dans la clause WHERE de la requête,
        ainsi que les variables à extraire dans la clause SELECT.
        Elle récupère également les valeurs spécifiques des propriétés (noms des étudiants, des universités et des villes).
        
        Génération de la requête Sparql
        Input: graph
        Output: requête Sparkl 
        Persp: la fonction devra être plus generique pour les prochaines versions en prenant en compte les autres
        types de relation pouvant exister entre les sources.
        On pourrait utiliser un Large Language Model pour détecter toutes les relations existantes dans le graphe reçu en entrée.
    
    """
    prefixes = "PREFIX ex: <http://example.org/>\n"

    where_clause = "WHERE {\n"
    filter_clause = {}
    
    # Initialiser les variables à extraire
    select_vars = []
    mylist={}

    for literal in list(set(source_literals)):
        if literal == "student":
            triple = "?student ex:name ?studentName ; ex:studiesAt ?university ."
            # Ajouter la variable à extraire
            select_vars.append("?studentName")
            mylist[1]=triple
            filter_clause[1]=get_propriete_values(triplets,literal)
        if literal == "university":

            triple="?university ex:name ?universityName ; ex:locatedIn ?city ."
            # Ajouter la variable à extraire
            select_vars.append("?universityName")
            mylist[2]=triple
            filter_clause[2]=get_propriete_values(triplets,literal)
        if literal == "city":
            # Ajouter le filtre pour la ville
            where_clause += f"  ?city ex:name ?cityName .\n"
            # Ajouter la variable à extraire
            select_vars.append("?cityName")
            triple="?city ex:name ?cityName ."
            mylist[3]=triple
            filter_clause[3]=get_propriete_values(triplets,literal)

    # Construire la clause where
    triplets=list(collections.OrderedDict(sorted(mylist.items())).values())
    for triplet in triplets:
        where_clause += f"\t{triplet}\n"
    where_clause += "}"

    # Construire la clause FILTER
    filter_temp = get_filters(filter_clause)

    # Definition du format & Construire la requête complète
    if output_format=="SELECT":
        query = prefixes + "SELECT " + " ".join(list(set(select_vars))) + "\n" + where_clause + "\n" + filter_temp
    elif output_format=="CONSTRUCT":
        query = prefixes + "CONSTRUCT " + " ".join(list(set(select_vars))) + "\n" + where_clause + "\n" + filter_temp

    return query

