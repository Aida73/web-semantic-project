# Génération de requête SPARQL à partir d'un graphe RDF

Etant donné un besoin exprimé comme une ontologie,
l'objectif est de générer automatiquement une requête Sparql permettant de retrouver les triplets instances de cette ontologie en identifiant les triplets candidats et générer les BGP représentatifs de ces triplets candidats.

## Fonctionnement

1. **Entrée de données**: Le script prend en entrée un graphe RDF

2. **Analyse du graphe**: Le script analyse le graphe RDF pour extraire les triplets, qui sont les unités de données fondamentales dans le graphe RDF.

3. **Détection des valeurs littérales**: Les valeurs littérales des objets dans les triplets sont identifiées. Ces valeurs littérales peuvent représenter différents types d'entités telles que des étudiants, des universités, des villes, etc.

4. **Construction de la requête SPARQL**: En fonction des valeurs littérales détectées, le script construit dynamiquement une requête SPARQL. Il génère les clauses SELECT, WHERE et FILTER nécessaires en utilisant les patterns appropriés pour chaque type d'entité détecté.

5. **Assemblage de la requête complète**: Le script assemble les différentes parties de la requête SPARQL, y compris les préfixes, la clause SELECT, la clause WHERE et la clause FILTER, pour former une requête SPARQL valide.

6. **Sortie de données**: La requête SPARQL générée est fournie en sortie, prête à être utilisée pour interroger le graphe RDF et récupérer les informations souhaitées.

## Utilisation

1. Assurez-vous d'avoir installé Python sur votre système.

2. Créer un environnement virtual avec `virtualenv myenv`

3. Activer l'environnement virtuel avec `source myenv/bin/activate` si vous êtes sur macOs ou `.\myenv\Scripts\activate` sur windows

4. Installez les dépendances requises en exécutant `pip install -r requirements.txt` dans votre environnement Python.

5. Exécutez le notebook `main.ipynb`. Noter que vous pourrez modifier le graphe d'entrée au niveau du fichiers `utils2.py` qui contient toutes les fonctions nécessaires pour créer la requête.

## Avertissement

Ce script devra être plus generique pour les prochaines versions en prenant en compte les autres
types de relation pouvant exister entre les sources.
On pourrait utiliser un Large Language Model pour détecter toutes les relations existantes dans le graphe reçu en entrée.
    