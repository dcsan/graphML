import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import json


def load_graph(fname):
    g = nx.read_edgelist(fname, create_using=nx.DiGraph)
    return g


def net_stats(g):

    # 1. The number of nodes in the network. (Gsmall has 3 nodes.)
    # how to find length of a generator?
    # is there another snap method for node count?
    print(f'nodes: {g.number_of_nodes()}')

    # 3. The number of directed edges in the network,
    # i.e., the number of ordered pairs (a, b) ∈ E for which a ̸= b. (Gsmall has 3 directed edges.)
    print('edges:', len(g.edges()))
    # print('edges:', nx.number_of_edges(g))

    # 2. The number of nodes with a self-edge (self-loop),
    # i.e., the number of nodes a ∈ V where (a, a) ∈ E. (Gsmall has 1 self-edge.)
    # https://snap.stanford.edu/snappy/doc/reference/CntSelfEdges.html
    print(f'self_loops:', nx.number_of_selfloops(g))

    # 4. The number of undirected edges in the network,
    # i.e., the number of unique unordered pairs (a,b), a ̸= b,
    # for which (a,b) ∈ E or (b,a) ∈ E (or both).
    # If both (a,b) and (b,a) are edges, this counts a single undirected edge. (Gsmall has 2 undirected edges.)

    # print('g.out', g.out_edges('1'))
    # print('g.in', g.in_edges('1'))
    print('edges', g.edges)


def find_reciprocal(g):

    # 5. The number of reciprocated edges in the network,
    # i.e., the number of unique unordered pairs of nodes (a, b), a ̸= b,
    # for which (a, b) ∈ E and (b, a) ∈ E. (Gsmall has 1 reciprocated edge.)
    edges = g.edges()
    recip1 = []
    edges = g.edges()
    for edge in edges:
        if (edge[1] == edge[0]):
            # skip self loops
            continue
        rev = (edge[1], edge[0])
        if (rev in edges):
            if edge not in recip1:  # we dont want BOTH directions
                recip1.append(rev)

    print('len(recip1):', len(recip1))
    print('recip1', recip1)

    nodes = g.nodes()
    recip2 = []
    for start in nodes:
        for other in g.adj[start]:
            if g.adj[other].get(start) is not None:
                rev = (other, start)
                if edge not in recip2 and rev not in recip2:
                    recip2.append(edge)

    print('len(recip2):', len(recip2))
    print('recip2', recip2)

    # 6. The number of nodes of zero out-degree. (Gsmall has 1 node with zero out-degree.)
    # 7. The number of nodes of zero in-degree. (Gsmall has 0 nodes with zero in-degree.)
    # 8. The number of nodes with more than 10 outgoing edges (out-degree > 10).
    # 9. The number of nodes with fewer than 10 incoming edges (in-degree < 10).


def render_graph(g, fname='plot'):
    fpath = f'output/{fname}.png'
    options = {
        # 'node_color': range(4),
        # 'cmap': plt.cm.Blues,
        'font_color': 'black',
        'node_size': 200,
        # 'width': 3,
        'arrowstyle': '-|>',
        'arrowsize': 10,
    }
    plt.clf()

    edges = [(u, v) for (u, v, d) in g.edges(data=True)]
    print('edges:', len(edges))

    # pos = nx.spring_layout(g)
    # pos = nx.kamada_kawai_layout(g)
    # weights = [1, 2, 3, 4, 5, 6]
    weights = range(1, len(edges)+1)

    pos = nx.circular_layout(g)
    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_edges(g, pos, edgelist=edges, width=weights)

    # labels
    nx.draw_networkx_labels(g, pos, font_size=10, font_family="sans-serif")

    # # nx.draw(g)

    # nx.draw_spring(g, with_labels=True)
    plt.savefig(fpath)
    # plt.axis("off")
    # plt.show()

    # nx.draw_networkx(g, arrows=True, **options)
    # plt.savefig(fpath)

    # as .dot
    nx.nx_agraph.write_dot(g, 'output/plot.dot')
    print(f'rendered to {fpath}')


def cycle_info(g):
    print('cycle basic', g.cycle_basis)


def remove_cycles(g):
    k = 0
    while True:
        k += 1
        try:
            c = nx.find_cycle(g)
            last = c.pop()
            print('removing', k, last)
            g.remove_edge(*last)
            print('edges:', len(g.edges()))
        except nx.NetworkXNoCycle:
            print('removed cycles', k)
            break
        except BaseException as err:
            print('err type', type(err))
    return g


def to_json(g):
    # node-link format to serialize
    d = nx.json_graph.node_link_data(g)
    print(json.dumps(d, indent=2))


def main():
    # g = load_graph("data/wiki-Vote.txt")
    # g = load_graph("data/vsmall.txt")
    # g = load_graph("data/micro.tsv")
    g = load_graph("data/cycle.tsv")
    render_graph(g, fname='before')

    net_stats(g)
    g = remove_cycles(g)
    net_stats(g)

    # to_json(g)
    render_graph(g, fname='after')


main()
