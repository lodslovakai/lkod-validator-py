from rdflib import Graph
from pyshacl import validate
from rdflib import ConjunctiveGraph
from rdflib.plugins.sparql import prepareQuery
import sys

global g
g = ConjunctiveGraph()

# Funkcia pre načítanie RDF z externího zdroja do grafu
def load_rdf_from_url(url, format):
    print(url, format)
    g.parse(url, format=format)
    return g

# Funkce pro provedení SPARQL dotazu
def execute_sparql_query(graph, lkodURI):
    # SPARQL dotaz na získánie všetkých datasetov
    print(lkodURI)
    sparql_query = """
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    SELECT distinct ?dataset
    WHERE {
      <"""+lkodURI+"""> a dcat:Catalog ;
          dcat:dataset ?dataset.
          }
    """
    print(sparql_query)
    query = prepareQuery(sparql_query)

    results = graph.query(query)
    return results

# Funkcia pre nahratie metadát o datasetoch do LKODu
def load_ttl_files_from_datasets(datasets, rdfFormat):

    for dataset in datasets:
        print("Loading dataset", dataset.dataset)
        g = load_rdf_from_url(dataset.dataset, rdfFormat)

if __name__ == "__main__":

    lkodURI = sys.argv[1]
    rdfFormat = sys.argv[2]

    rdf_graph = load_rdf_from_url(lkodURI, rdfFormat)
    print("LKOD Catalog file loaded")

    datasets = execute_sparql_query(rdf_graph, lkodURI)

    # print(datasets)
    load_ttl_files_from_datasets(datasets, rdfFormat)

    print("LKOD Dataset files loaded")

    # Načtení SHACL konfigurace
    shacl_graph = Graph()
    shacl_graph.parse("https://raw.githubusercontent.com/slovak-egov/centralny-model-udajov/main/tbox/national/dcat-ap-sk-2.0-shapes-2023b.02.ttl", format="ttl")
    #print(shacl_graph.serialize(format="turtle"))

    print("SHACL Graph loaded")

    # Validácia
    conforms, report_graph, report_text = validate(rdf_graph, shacl_graph=shacl_graph, inference="rdfs", debug=True)

    print("SHACL Validation completed")

    sourceFile = open('rdf_graph.ttl', 'w')
    print(rdf_graph.serialize(format="turtle"), file = sourceFile)
    sourceFile.close()

    sourceFile = open('shacl_graph.ttl', 'w')
    print(shacl_graph.serialize(format="turtle"), file = sourceFile)
    sourceFile.close()

    sourceFile = open('report_graph.ttl', 'w')
    print(report_graph.serialize(format="turtle"), file = sourceFile)
    sourceFile.close()