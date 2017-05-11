import networkx as nx
import warnings
import matplotlib.cbook
import matplotlib.pyplot as plt
from Main import *



warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

g = nx.Graph()


# g.add_nodes_from([0,9])
# g.add_edges_from([(0,1),(1,2)])
#
# nx.draw(g)
#nx.draw(g,pos=nx.spring_layout(g))
#nx.draw_networkx(g,arrows=True, with_label=True)
def build(graph):

    for i in range(0,len(graph.listRouters)):
        g.add_node(i, ip=graph.listRouters[i].getIP())
    i=0
    list = g.nodes(data=True)
    #print(len(graph.links))
    for i in range(0, len(graph.links)):
        #print(i)
        num=0
        for j in list:

            for k, value in j[1].items():
                #print("Router"+str(num)+" in links list: ", value)

                if(value == graph.links[i].getLink(1)):

                    g.add_edge(value, graph.links[i].getLink(2), weight="weight is "+str(graph.links[i].getWeight()))
            num += 1


def printTable(graph):


    if (len(graph.links) == 0):
        print("Sorry, no graph to plot.")
        return
    select = input("would you like to see the forwarding table for a router? Y or N: ")
    if(select == "Y"):
        fwdtable = input("Please provide the IP for the forwarding table desired: ")
        routerobj = graph.getRouter(fwdtable)
        print(routerobj)
        #get the forwarding table for this specific router
        holdtable = "--|Forwarding Table|--\n" #String to holdtable the forwarding table
        holdtable += "For " + fwdtable + "   \n"
        holdtable += "________________________\n"

        #get2ndElem through the stored table list in the router object
        for e in routerobj.table:
            #print(e)
            holdtable += "Destination: "
            get2ndElem = 0
            for ips in e:
                #print (ips)
                holdtable += ips +" "
                if(get2ndElem == 0):
                    holdtable += "Output: "
                get2ndElem += 1

            holdtable += '\n'
        # Plot the text to the spawned screen
        plt.text(0, 0, holdtable, fontsize=12, verticalalignment='top', horizontalalignment='right')
    #print(holdtable)

    #this will holdtable the nodes we want to draw to the plot
    nodestodraw = []
    p = g.nodes(data=True)
    for l in p:
        for m , value in l[1].items():
            nodestodraw.append(value)
    #print(nodestodraw)
    nx.draw_networkx(g, pos=nx.random_layout(g), nodelist=nodestodraw, node_color='c')
    pos = nx.get_node_attributes(g, 'pos')
    labels = nx.get_edge_attributes(g,'weight')
    #print(labels)
    nx.draw_networkx_edge_labels(g, pos=nx.random_layout(g), edge_labels=labels, label_pos=0)

    plt.ioff()
    axes = plt.gca()
    #Set the dimensions
    axes.set_xlim([-1,1])
    axes.set_ylim([-1,1])
    #Show the graph here
    plt.show()




graph = Graph()

print("Welcome to Group Awful's Awful-Network-Simulator\u00a9 (by Travis Anderson & Chandler Staggs)",
      "\nBelow, you can see the current state of the network.",
      "\nType the appropriate key to add routers, remove routers, and view a particular router's forwarding table.")

while (True):

    ######### DISPLAY NETWORK STATE HERE #############
    print("------------- Network State -------------",
          "\n Router | -Link Weight-> | Link ")

    if (graph.listRouters != []):
        for r in graph.listRouters:
            i = 1
            if (len(graph.listRouters) == 1):
                print(r.getIP())
            for l in r.getLinks():
                if (i == 1):
                    print(r.getIP(), "-" + str(graph.getLinkWeight(r, graph.getRouter(l.getLink(2)))) + "->",
                          l.getLink(2))
                    i += 1
                else:
                    print("          ", "-" + str(graph.getLinkWeight(r, graph.getRouter(l.getLink(2)))) + "->",
                          l.getLink(2))

    userIn = input("Add router: 'a' || Remove router: 'r' || View Forwarding Table: 'f' || Exit: 'e' -> ")

    if (userIn == "a"):
        graph.addRouter()
        build(graph)
        printTable(graph)
    elif (userIn == "r"):
        ip = input("Please enter the IP address of the router you wish to remove: ")
        if (graph.getRouter(ip) == "Router does not exist."):
            print("Router does not exist. Please try again.")
            continue
        else:
            graph.rmRouter(ip)
            build(graph)
            printTable(graph)
    elif (userIn == "f"):
        ip = input("Please enter the IP address of the router you wish to see the forwarding table of: ")
        if (graph.getRouter(ip) == "Router does not exist."):
            print("Router does not exist. Please try again.")
            continue
        else:
            graph.getRouter(ip).printTable()
            build(graph)
            printTable(graph)
    elif (userIn == "e"):
        exit(0)
    else:
        print("Please enter a valid key option.")