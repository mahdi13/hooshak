from graph_tool.all import *

if __name__ == '__main__':
    g = Graph(directed=False)

    v1 = g.add_vertex()

    print(v1)

    v2 = g.add_vertex()
    vprop_name = g.new_vertex_property('string')

    vprop_name[v2] = 'salam'
    print(vprop_name[v2])

    print(v2)

    e = g.add_edge(v1, v2)
    print(e)

    print('hi')
