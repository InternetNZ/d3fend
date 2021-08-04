#!/usr/bin/env python3
"""
A module to work with MITRE D3FEND
"""
import argparse
import csv
import logging

from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDFS, RDF

D3FEND_JSON_LD = "https://d3fend.mitre.org/ontologies/d3fend.json"
D3FEND_NAMESPACE = "http://d3fend.mitre.org/ontologies/d3fend.owl#"
D3FEND_URL_PREFIX = "https://d3fend.mitre.org/technique/d3f"

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def generate_csv(args):
    """
    Generates a CSV file from MITRE D3FEND JSON-LD content.

    :param args: Input arguments.
    """
    LOGGER.info('Transforming MITRE D3FEND JSON-LD to CSV...')
    rows = []
    row_header = [
        "d3fend-id",
        "tactic",
        "label",
        "definition",
        "how-it-works",
        "url"
    ]

    graph = Graph()

    LOGGER.debug(f"Loading d3fend.json from {D3FEND_JSON_LD}")
    graph.parse(location=D3FEND_JSON_LD, format='json-ld')

    graph.namespace_manager.bind('rdf', RDF)
    graph.namespace_manager.bind('owl', OWL)
    graph.namespace_manager.bind('rdfs', RDFS)

    d3fend = Namespace(D3FEND_NAMESPACE)
    graph.bind('d3fend', d3fend)

    for tactic in graph.subjects(RDFS.subClassOf, d3fend.DefensiveTactic):
        for technique_l1 in graph.subjects(d3fend.enables, tactic):
            for technique_l2 in graph.subjects(RDFS.subClassOf, technique_l1):
                kb_article = graph.value(subject=technique_l2, predicate=d3fend["kb-article"])
                how_it_works = ""
                kb_article = kb_article.split('##') if kb_article else []
                for article in kb_article:
                    if "How it works" in article:
                        how_it_works = article.replace("How it works", '').strip().rstrip('/n')
                        break
                row = [
                    graph.value(subject=technique_l2, predicate=d3fend["d3fend-id"]),  # de3fend-id
                    graph.value(subject=tactic, predicate=RDFS.label),  # tactic
                    "{}: {}".format(
                        graph.value(subject=technique_l1, predicate=RDFS.label),
                        graph.value(subject=technique_l2, predicate=RDFS.label)
                    ),  # label
                    graph.value(subject=technique_l2, predicate=d3fend.definition),  # definition
                    how_it_works,  # how-it-works
                    "{}:{}".format(D3FEND_URL_PREFIX, technique_l2.split('#')[1])  # url
                ]
                LOGGER.debug(row)
                rows.append(row)

    with open(args.output, 'w') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(row_header)
        csv_writer.writerows(rows)

    LOGGER.info(f"{args.output} has been generated successfully.")


if __name__ == '__main__':
    try:
        main_parser = \
            argparse.ArgumentParser(
                description="""This script is used to load MITER D3FEND ontology and work with it.""")

        subparsers = main_parser.add_subparsers(title="Commands",
                                                help="Available commands")

        csv_parser = subparsers.add_parser("csv", help="Generates CSV file")
        csv_parser.add_argument('-o', '--output', default='d3fend.csv', type=str,
                                help="Output csv file name. Default 'd3fend.csv'")
        csv_parser.add_argument('-v', '--verbose', default=False, action='store_true',
                                help="More verbose")
        csv_parser.set_defaults(func=generate_csv)

        arguments = main_parser.parse_args()

        if arguments.verbose:
            LOGGER.setLevel(logging.DEBUG)

        arguments.func(arguments)
    except Exception as ex:  # pylint: disable=broad-except
        LOGGER.error(ex)
