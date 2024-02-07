from rdflib import Graph, Namespace, Literal


def generate_graph():
    g = Graph()

    g.add((Literal("John"), Namespace("ontologie").aPourNom, Literal("John Doe")))
    g.add((Literal("John"), Namespace("ontologie").aPourAge, Literal(30)))

    return g


def template(type:str):
    temp = "PREFIX ontologie: <http://exemple.org/ontologie#>\n{} ?sujet ?predicate ?objet\nWHERE {{ }}".format(type)
    return temp
    
def generate_requete(G: Graph):
    requete = input('Entrer le type de requete souhaite SELECT ou CONSTRUCT:')
    if requete.lower() != 'select' and requete.lower() != 'construct':
        raise ValueError('Veuiller entrer SELECT ou CONSTRUCT')
    else:
        pass
    
    
print(template("SELECT"))