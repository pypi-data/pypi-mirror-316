from collections import Counter
from pathlib import Path
from queue import Queue
from typing import NamedTuple

import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from tqdm.auto import tqdm


class ParsedOntology(NamedTuple):
    nodes_list: list[dict]
    goterms: pd.DataFrame
    graph: dict[str, set[str]]
    gene2go: pd.DataFrame

    def __repr__(self):
        n_terms = len(self.goterms)
        n_associations = len(self.gene2go)

        return f"ParsedOntology with {n_terms} GO terms and {n_associations} gene2go associations"


def parse_obo(
    obo_filepath: str | Path, gene2go_associations: pd.DataFrame
) -> ParsedOntology:
    """Parses an OBO file and gene2go associations dataframe into a graph.

    The graph is represented as a dictionary where each key is a node ID and
    the value is a set of node IDs that are connected to the node.

    Parameters
    ----------
    obo_filepath : str | Path
        Path to the OBO file.
    gene2go_associations : pd.DataFrame
        Dataframe containing the gene2go associations. It must contain at least
        columns `gene_id` and `go_term_id`.

    Returns
    -------
    ParsedOntology
        NamedTuple containing the nodes list, the GO terms dataframe and the graph.
    """

    # download from http://current.geneontology.org/ontology/go.obo
    obo_filepath = Path(obo_filepath)

    known_node_types = set()
    known_ids = set()
    known_keys = set()
    alt_id_map = {}
    edges = set()
    edges_by_relationship = {}
    edges_by_intersection = {}
    nodes_list: list[dict] = []
    node_ids_by_type = {}

    with obo_filepath.open() as file:
        node_type = None
        node = {}
        for i, line in enumerate(file):
            line = line.strip()

            # empty lines
            if not line:
                if node:
                    node["node_type"] = node_type
                    known_ids.add(node["id"])
                    nodes_list.append(node)

                    if node_type not in node_ids_by_type:
                        node_ids_by_type[node_type] = set()
                    node_ids_by_type[node_type].add(node["id"])

                    node = {}
                continue

            # start of a new node
            if line.startswith("["):
                node_type = line.strip().strip("[]")
                known_node_types.add(node_type)
                continue

            # there is no node yet (header of file)
            if node_type is None:
                continue

            # this should be a key-value pair
            key, data = [s.strip() for s in line.split(":", 1)]
            known_keys.add(key)

            # unique keys
            if key in [
                "id",
                "name",
                "namespace",
                "def",
                "is_obsolete",
                "replaced_by",
                "holds_over_chain",
                "created_by",
                "creation_date",
            ]:
                assert key not in node, f"{key}, {node}"
                node[key] = data
                continue

            if key == "alt_id":
                alt_id_map[data] = node["id"]

            # non-unique keys
            if key in [
                "alt_id",
                "subset",
                "consider",
                "synonym",
                "comment",
                "xref",
                "property_value",
            ]:
                if key not in node:
                    node[key] = []
                node[key].append(data)
                continue

            if key == "is_a":
                parent_id, parent_name = [s.strip() for s in data.split("!", 1)]
                edge = (node["id"], parent_id)
                edges.add(edge)
                continue

            if key.startswith("is_"):
                if data == "true":
                    node[key] = True
                elif data == "false":
                    node[key] = False
                else:
                    raise ValueError("This wasn't a boolean value")
                continue

            if key == "relationship":
                assert "GO:" in data
                assert data.count("!") == 1
                rel_type_and_id, other_node_name = [s.strip() for s in data.split("!")]
                rel_type, other_id = [s.strip() for s in rel_type_and_id.split(" ")]
                known_ids.add(other_id)

                edge = (node["id"], other_id)
                if rel_type not in edges_by_relationship:
                    edges_by_relationship[rel_type] = set()
                edges_by_relationship[rel_type].add(edge)

                if key not in node:
                    node[key] = {}
                if rel_type not in node[key]:
                    node[key][rel_type] = []
                node[key][rel_type].append(other_id)
                continue

            if key == "intersection_of":
                assert "GO:" in data
                assert data.count("!") == 1
                rel_type_and_id, other_node_name = [s.strip() for s in data.split("!")]
                if rel_type_and_id.startswith("GO:"):
                    rel_type, other_id = "intersection", rel_type_and_id
                else:
                    rel_type, other_id = [s.strip() for s in rel_type_and_id.split(" ")]
                known_ids.add(other_id)

                edge = (node["id"], other_id)
                if rel_type not in edges_by_intersection:
                    edges_by_intersection[rel_type] = set()
                edges_by_intersection[rel_type].add(edge)

                if key not in node:
                    node[key] = {}
                if rel_type not in node[key]:
                    node[key][rel_type] = []
                node[key][rel_type].append(other_id)
                continue

            if key in ["disjoint_from", "transitive_over", "inverse_of"]:
                # ignore these for now
                continue

            print(f"{i: 6d} ignored:\t{key}: {data} for node {node['id']}")

    all_edges = edges
    for rel_type, edges_set in edges_by_relationship.items():
        all_edges = all_edges.union(edges_set)
    for rel_type, edges_set in edges_by_intersection.items():
        all_edges = all_edges.union(edges_set)

    alt_ids_edges = set()
    for node in nodes_list:
        node_id = node["id"]
        if "alt_id" in node:
            for alt_id in node["alt_id"]:
                edge = (alt_id, node_id)
                alt_ids_edges.add(edge)
    all_edges = all_edges.union(alt_ids_edges)

    graph: dict[str, set[str]] = {}
    for edge in all_edges:
        # note that the direction of the graph goes from leaves to roots
        parent_node_id, child_node_id = edge
        if parent_node_id not in graph:
            graph[parent_node_id] = set()
        graph[parent_node_id].add(child_node_id)

    for k in list(graph.keys()):
        if not k.startswith("GO:"):
            graph.pop(k)

    goterms = pd.DataFrame(
        [
            {k: v for k, v in n.items() if isinstance(v, str)}
            for n in nodes_list
            if n["id"].startswith("GO:")
        ]
    )
    gene2go_dict = (
        gene2go_associations.groupby("gene_id")["go_term_ids"].apply(list).to_dict()
    )
    for gene_id, go_term_id_list in gene2go_dict.items():
        if gene_id not in graph:
            graph[gene_id] = set()
        for go_term_id in go_term_id_list:
            graph[gene_id].add(go_term_id)
    return ParsedOntology(
        nodes_list=nodes_list,
        graph=graph,
        goterms=goterms,
        gene2go=gene2go_associations,
    )


def _go_term_hits(go_graph, genes_list, verbose=False):
    totals = Counter()
    q = Queue()
    if verbose:
        genes_list = tqdm(genes_list, desc="Counting GO term hits")

    for gene_id in genes_list:
        branch = set()
        q.put(gene_id)
        while not q.empty():
            parent_id = q.get()

            if parent_id in branch:
                continue

            if parent_id != gene_id:
                branch.add(parent_id)

            if parent_id not in go_graph:
                continue

            for child_id in go_graph[parent_id]:
                q.put(child_id)
        totals += Counter(branch)

    return totals


def go_enrichment(
    ontology: ParsedOntology,
    genes_universe: list[str],
    genes_list: list[str],
    verbosity: int = 2,
):
    """
    Runs a GO enrichment analysis.

    Parameters
    ----------
    ontology: ParsedOntology
        Parsed Gene Ontology object.
    genes_universe: list[str]
        List of all genes in the universe.
    genes_list: list[str]
        List of genes to test for enrichment.
    verbosity: int, optional
        How much output to display. Defaults to 2.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the results of the enrichment analysis. The index is the
        GO term identifier and the columns are "hits", "background", "pvalue",
        "bonferroni", and "benjamini". The "hits" and "background" columns are integer
        values and the others are float values.

    """

    go_graph = ontology.graph
    goterms = ontology.goterms

    tst_genes = pd.Index(genes_list)
    oth_genes = pd.Index(genes_universe).difference(tst_genes)
    tst_genes_hits = _go_term_hits(go_graph, tst_genes, verbose=verbosity > 1)
    oth_genes_hits = _go_term_hits(go_graph, oth_genes, verbose=verbosity > 1)
    all_genes_hits = _go_term_hits(go_graph, genes_universe, verbose=verbosity > 1)

    result_df = (
        goterms.drop_duplicates("id")
        .drop(
            columns=[
                "def",
                "node_type",
                "is_obsolete",
                "replaced_by",
                "created_by",
                "creation_date",
            ]
        )
        .set_index("id")
    )

    result_df["hits"] = 0
    result_df["background"] = 0
    result_df["pvalue"] = 1.0

    if verbosity > 0:
        result_df_iterrows = tqdm(
            result_df.iterrows(), total=result_df.shape[0], desc="Running tests"
        )
    else:
        result_df_iterrows = result_df.iterrows()

    for gid, row in result_df_iterrows:
        result_df.loc[gid, "background"] = all_genes_hits[gid]
        yy = tst_genes_hits[gid]
        yn = oth_genes_hits[gid]
        ny = tst_genes.size - yy
        nn = oth_genes.size - yn
        if (yy + yn) > 0 and yy > 2:
            contingency_table = [[yy, yn], [ny, nn]]
            test_result = fisher_exact(contingency_table, alternative="greater")
        else:
            continue
        result_df.loc[gid, "hits"] = yy
        result_df.loc[gid, "pvalue"] = test_result.pvalue

    result_df = result_df.dropna().sort_values("pvalue").reset_index()
    for namespace in result_df["namespace"].unique():
        mask = result_df["namespace"] == namespace

        bonferroni = multipletests(result_df.loc[mask, "pvalue"], method="bonferroni")
        result_df.loc[mask, "bonferroni"] = bonferroni[1]

        benjamini = multipletests(result_df.loc[mask, "pvalue"], method="fdr_bh")
        result_df.loc[mask, "benjamini"] = benjamini[1]

    return result_df.set_index("id")
