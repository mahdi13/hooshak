import igraph
from igraph import *


if __name__ == '__main__':

    print(igraph.__version__)

    g = Graph()
    # print(g)

    g.add_vertices(3)
    # print(g)

    g.add_edges([(0, 1), (1, 2)])


    # g[0]['name'] = 'salam'
    # print(g[0]['name'])

    print('Hello World!')
