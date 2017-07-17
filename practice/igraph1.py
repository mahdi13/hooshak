import igraph
from igraph import *

if __name__ == '__main__':
    print(igraph.__version__)

    g = Graph()
    # print(g)

    g.add_vertices('a')
    g.add_vertices('b')
    g.add_vertices(['c', 'd', 'e'])
    g.add_vertices([10])
    # print(g)

    g.add_edges([('a', 'b')])
    g.add_edges([('c', 'd')])
    g.add_edges([('b', 'e')])
    # g.add_edges([('b', '10')])

    # g[0]['name'] = 'salam'
    # print(g[0]['name'])

    g.vs.find('a')['type'] = 'user'
    print(g.vs.find('a'))
    print('Hello World!')
