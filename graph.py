from igraph import *


g = Graph()

g.add_vertices(6)

g.add_edges([(0,1),(1,2)])

g.layout("kk")


plot(g)


