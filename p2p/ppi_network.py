#!/usr/bin/env python
# linxingzhong@1gene.com.cn 2016-8-17
# Create network graph for ppi result.


import sys

import networkx as nx
import matplotlib.pyplot as plt


def readPPI(ppi):
    '''
    Read protein to protein interaction file,
    then convert to a list:
        [[ppa, ppb], [ppa,ppc], ...]
    '''

    with open(ppi) as handle:
        links = handle.readlines()[1:]      # exclude header line
    links = [x.split() for x in links]
    return links


def getNodes(links):
    '''
    Get unique nodes from links, remove duplicates.
    '''
    return list(set(reduce(lambda a,b : a+b, links)))


def readFC(nodeattr):
    with open(nodeattr) as handle:
        attributes = handle.readlines()
    attributes = [x.strip().split('\t') for x in attributes 
                 if (not x.startswith('#')) and (not x.startswith('GeneID'))]
    return dict([(x[0],x[1]) for x in attributes])
            


if __name__ == "__main__":
    links = readPPI(sys.argv[1])
    nodes = getNodes(links)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    plt.figure(figsize=(10,10))
    plt.axis('off')
    pos = nx.fruchterman_reingold_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.savefig(sys.argv[2])
