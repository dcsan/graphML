import snap


def load_graph(fname):
    g = snap.LoadEdgeList(snap.TNGraph, fname, 0, 1)
    # g = snap.LoadEdgeList(snap.PNGraph, "vsmall.txt", 0, 1)
    print('loaded graph:', fname)
    # snap.PrintInfo(g)
    # this will fail silently if it cannot find the path
    snap.PrintInfo(g, "QA Stats", "output/qa-info.txt", False)
    # how to get this info in a variable not a file?
    return g


def make_labels(g):
    # format: {0: "zero", 1: "one", 2: "two", 3: "three"}
    labels = {}

    for _idx, node in enumerate(g.Nodes()):
        nid = node.GetId()
        labels[nid] = f"n_{nid}"
        # labels have to start from 1 not 0
        # labels[idx + 1] = f"node_{idx + 1}"

    return labels


def render_graph(g, fname: str):
    fpath = fname.replace(".txt", ".dot")
    labels = make_labels(g)
    print('graph rendered to:', fpath)
    g.SaveGViz(fpath, fname, labels)


def graph_info(g):

    # 1. The number of nodes in the network. (Gsmall has 3 nodes.)
    # how to find length of a generator?
    # is there another snap method for node count?
    print('nodes:', len(list(g.Nodes())))

    # 2. The number of nodes with a self-edge (self-loop), i.e., the number of nodes a ∈ V where (a, a) ∈ E. (Gsmall has 1 self-edge.)
    # https://snap.stanford.edu/snappy/doc/reference/CntSelfEdges.html
    c = g.CntSelfEdges()
    print('self edges:', c)

    # 3. The number of directed edges in the network, i.e., the number of ordered pairs (a, b) ∈ E for which a ̸= b. (Gsmall has 3 directed edges.)
    print('directed edges:', g.CntUniqDirEdges())

    # 4. The number of undirected edges in the network, i.e., the number of unique unordered pairs (a,b), a ̸= b, for which (a,b) ∈ E or (b,a) ∈ E (or both). If both (a,b) and (b,a) are edges, this counts a single undirected edge. (Gsmall has 2 undirected edges.)
    print('UNdirected edges:', g.CntUniqUndirEdges())

    # 5. The number of reciprocated edges in the network, i.e., the number of unique unordered pairs of nodes (a, b), a ̸= b, for which (a, b) ∈ E and (b, a) ∈ E. (Gsmall has 1 reciprocated edge.)

    # 6. The number of nodes of zero out-degree. (Gsmall has 1 node with zero out-degree.)
    # 7. The number of nodes of zero in-degree. (Gsmall has 0 nodes with zero in-degree.)
    # 8. The number of nodes with more than 10 outgoing edges (out-degree > 10).
    # 9. The number of nodes with fewer than 10 incoming edges (in-degree < 10).


def make_graph():
    g = snap.GenForestFire(1000, 0.35, 0.35)
    return g


def run():
    fname = "data/vsmall.txt"
    # fname = "wiki-Vote.txt"
    g = load_graph(fname=fname)

    # g = make_graph()
    graph_info(g)
    render_graph(g, "output/vsmall.dot")


if __name__ == "__main__":
    run()
