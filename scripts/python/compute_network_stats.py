import argparse
import os
import json


import networkx as nx


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute network stats of pony interactions in my little pony dialog"
    )
    parser.add_argument(
        "-i", type=argparse.FileType("r"), help="Json network of pony dialog"
    )
    parser.add_argument(
        "-o", type=str, help="Output json file containing network stats of pony dialog"
    )
    args = parser.parse_args()
    return args.i, args.o


def import_data(input):
    return json.load(input)


def compute_degree(graph: nx.Graph):
    deg = nx.degree_centrality(graph)

    # only keep top 3
    deg = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:3]

    return deg


def compute_weighted_degree(graph: nx.Graph):
    deg = graph.degree(weight="weight")
    # only keep top 3
    sorted_deg = sorted(deg, key=lambda x: x[1], reverse=True)[:3]  # type: ignore
    return sorted_deg


def compute_closeness(graph: nx.Graph):
    closeness = nx.closeness_centrality(graph)
    # only keep top 3
    closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:3]
    return closeness


def compute_betweenness(graph: nx.Graph):
    betweenness = nx.betweenness_centrality(graph)
    # only keep top 3
    betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3]
    return betweenness


def compute_stats(data: dict):
    G = nx.Graph()

    for speaker, listeners in data.items():
        G.add_node(speaker)
        for listener, weight in listeners.items():
            G.add_edge(speaker, listener, weight=weight)

    deg_centrality = compute_degree(G)
    weighted_deg_centrality = compute_weighted_degree(G)
    closeness = compute_closeness(G)
    betweenness = compute_betweenness(G)

    return deg_centrality, weighted_deg_centrality, closeness, betweenness


def main():
    input, output = parse_args()

    data = import_data(input)

    deg, weighted_deg, closeness, betweenness = compute_stats(data)

    stats = {
        "degree": deg,
        "weighted_degree": weighted_deg,
        "closeness": closeness,
        "betweenness": betweenness,
    }

    # if output file is specified, check that path exists
    # if not, create it
    if output:
        # extract directory path
        output_dir = os.path.dirname(output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    with open(output, "w") as f:
        json.dump(stats, f, indent=4)
    pass


if __name__ == "__main__":
    main()
