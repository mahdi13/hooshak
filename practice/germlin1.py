from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


if __name__ == '__main__':
    graph = Graph()
    g = graph.traversal()

    g.addV('person').property('name', 'stephen')

    an = g.V().next()

    print('Hello World!')
