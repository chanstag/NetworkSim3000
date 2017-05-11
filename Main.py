#!/usr/bin/python

#Link class
class Link:
    linkWeight = 0
    
    # endpoints of each link represented as string IP addresses
    router1 = ""
    router2 = ""
    
    def __init__(self, w, l1, l2):
        self.linkWeight = w
        self.router1 = l1
        self.router2 = l2
    
    def getWeight(self):
        return self.linkWeight
    
    # returns the given link end-point string
    def getLink(self, num):
        if(num == 1):
            return self.router1
        else:
            return self.router2
    
#Router class
class Router:
    IPAddr = ""
    listLinks = []
    listNeighbors = []
    
    # visited node list used when creating the forwarding table
    visited = []
    
    # list of tuples that represent each router's forwarding table
    table = []
    
    pathCost = 0
    numLinks = 0
    
    def __init__(self, ipadd, links, neigh):
        self.IPAddr = ipadd
        self.listLinks = links
        self.listNeighbors = neigh
        self.table = []
        self.visited = []
        self.pathCost = 0
        self.numLinks = 0
    
    # given an IP address and link weight, 
    # a Link object is created and added to both the router and graph object list of links
    def addLink(self, weight, dest, graph):
        
        # if the given IP is identical to the source IP, no link is made
        # else the link is added to self.listLinks (router) and graph.links (network graph)
        if(self.getIP() != dest):
            l = Link(weight, self.getIP(), dest)
            self.listLinks.append(l)
            
            if(self.isLink(l, graph)):
                return "True"
            else:
                graph.links.append(l)
            
            return "True"
        else:
            return "Can not add link between a node and itself."
    
    # checks in existing neighbors list for given IP address
    def isNeigh(self, ip):
        for n in self.getNeighbors():
            if(n.getIP() == ip):
                return True
        return False
    
    # checks if given link is present in the graph's link list
    def isLink(self, link, graph):
        
        # for each link in the network,
        # if the end-points match the given link object's end-points return true else false
        for l in graph.links:
            if((l.getLink(1) == link.getLink(1) or l.getLink(1) == link.getLink(2))
               and (l.getLink(2) == link.getLink(1) or l.getLink(2) == link.getLink(2))):
                return True
        return False
    
#     # removes the given link from both the local router link list and global graph  link list
#     def removeLink(self, rter):
#         
#          # for each link of the router,
#         # if the link end-points match the end-points of the given link object,
#         # remove the link from the local router list
#         for l in self.getLinks():
#             l1 = l.getLink(1)
#             l2 = l.getLink(2)
#             if((l1 == rter.getLink(1) or l1 == rter.getLink(2)) and (l2 == rter.getLink(2) or l2 == rter.getLink(1))):
#                 self.listLinks.remove(l)
#                 self.numLinks -= 1
#                 break;
    
    # add the given neighbor object to the router's neighbor list 
    def addNeigh(self, neigh, graph):
        if(neigh != self.getIP()):
            self.listNeighbors.append(graph.getRouter(neigh))
#             print("neighbor appended", neigh, "to", self.getIP())
    
    # removes the given neighbor from the router's neighbor list,
    # also removes it from the associated link of the neighbor from the router and graph's link list
    def removeNeigh(self, neigh, graph):
        for n in self.listNeighbors:
            if(n.getIP() == neigh):
                self.listNeighbors.remove(n)
                for l in self.getLinks():  
                    if(l.getLink(1) == neigh or l.getLink(2) == neigh):
                        self.listLinks.remove(l)
                        graph.removeGLink(l)
         
    def getIP(self):
        return self.IPAddr
       
    def getLinks(self):
        return self.listLinks

    def getNeighbors(self):
        return self.listNeighbors
    
    # prints the router's forwarding table
    def printTable(self):
        print("--Forwarding Table for:",self.getIP(),"---")
        print("Destination\tOutput Link")
        
        # for each row in the router.table list (represented as a tuple - (dest, output link))
        # print the contents of the tuple
        for t in self.table:
            print(t[0], "\t", t[1])
        print("--------------------------------------\n")
    
    # prints each link object of the router as a tuple (source,dest) (used for debugging purposes)
    def printLinks(self):
        print(self.getIP(),"links:")
        for l in self.listLinks:
            print("(",l.getLink(1)+",",l.getLink(2)+")\n")
    
    # prints each neighbor of the router (used for debugging purposes)
    def printNeighbors(self):
        print("neighbors of", self.getIP())
        for n in self.getNeighbors():
            print(n.getIP(), "->N")
    
    # prints the visited nodes of Dijkstra's algorithm (used for debugging purposes)
    def printVisited(self):
        for r in self.visited:
            print(r.getIP()+":"+str(r.pathCost), "->")

###############
#Graph class
###############
class Graph:
    listRouters = []
    links = []
    
    # string used to dynamically generate host ID of each router added
    mostcurrentip = 0
    
    def __init__(self):
        self.listRouters = []
        self.links = []
        self.mostcurrentip = 0
    
    # generates IP address based on the mostcurrentip
    def genIP(self):
        subnet= "200.25.3."
        self.mostcurrentip += 1
        return subnet+str(self.mostcurrentip)
    
    def getGLinks(self):
        return self.links
    
    # searches and returns router object with given IP from exiting router list
    def getRouter(self, ip):
        for r in self.listRouters:
            if(r.getIP() == ip):
                return r
        return "Router does not exist."
    
    # returns weight of link between given router objects
    def getLinkWeight(self, rter1, rter2):
        toReturn = None;
        for x in self.links:
            if((x.getLink(1) == rter1.getIP()
               or x.getLink(1) == rter2.getIP()) and 
               (x.getLink(2) == rter1.getIP() 
               or x.getLink(2) == rter2.getIP())):
                toReturn = x
                return toReturn.getWeight()
        return 0
    
    # checks if given IP is in the visited node list
    def isVisited(self, ip, visited):
        for v in visited:
            if(v.getIP() == ip):
                return True
        return False
    
    # removes given link object from graph's link list
    def removeGLink(self, rter):
        rml1 = rter.getLink(1)
        rml2 = rter.getLink(2)
        for l in self.links:
            if((l.getLink(1) == rml1 or l.getLink(1) == rml2) or (l.getLink(2) == rml1 or l.getLink(2) == rml2)):
                self.links.remove(l)
    
    # prints links of the graph (debugging purposes)
    def printGLinks(self):
        print("Graph links:")
        for l in self.links:
            print("(",l.getLink(1)+",",l.getLink(2)+")\n")
    
    # removes the router w/ given IP from the network
    def rmRouter(self, ip):
        toRemove = None;
        # remove router w/given IP from listRouters
        for r in self.listRouters:
            if(r.getIP() == ip):
                toRemove = self.getRouter(r.getIP())
                self.listRouters.remove(toRemove)
                break
        # removes the toRemove router object from each router's neighbor list if applicable
        # this will also remove the router's links to and from it
        for x in self.listRouters:
            x.removeNeigh(toRemove.getIP(), self)


        print("Router removed ...", ip)
        #self.mostcurrentip -= 1
        
        # for each existing router, their forwarding tables are updated
        for y in self.listRouters:
            if(y.getLinks() != None and y.getNeighbors() != None):
#                 y.printNeighbors()
#                 print("Creating table for", y.getIP())
                self.createTable(y)


    
    # adds a router to the network with a dynamic IP address and user-input links/link weights
    def addRouter(self):
        lnks = []
        neigh = []
        ip = self.genIP()
        i = 1
        
        # new router object created with dynamic IP, empty links and neighbors list
        # router is added to graph's list of routers
        toAdd = Router(ip, lnks, neigh)
        self.listRouters.append(toAdd)
        
        # if this is the first router created, no links will be added, method terminates
        if(self.mostcurrentip < 2):
            print("First Router created ...", ip)
            return 0
        
        # user is prompted to enter the number of links for the new router,
        # the link end-points and the link weights
        while(True):
            try:
                numLinks = int(input("Please enter the number of links you'd like to add for this newly-created router: "))
                if(numLinks > len(self.listRouters) - 1):
                    print("Too many links for too few routers. Please try again")
                    continue
                break
            except ValueError:
                print("You must enter an integer for the number of links. Please try again.")
                continue
                    
            
        while(i <= numLinks):
            linkIP = input("Please enter the destination IP address for link #"+str(i)+": ")
            if(self.getRouter(linkIP) == "Router does not exist."):
                print("Router does not exist. Please try again.")
                continue
            try:
                weight = int(input("Now, please enter the weight for link #"+str(i)+": "))
                if(weight < 1 or weight > 10):
                    print("Link weights must be valued between 1 and 10. Please try again.")
                    continue
            except ValueError:
                print("You must enter an integer for the link weight. Please try again.")
                continue
            
            # link and associated neighbors of new router are added
            toAdd.addLink(weight, linkIP, self)
            toAdd.addNeigh(linkIP, self)
#             toAdd.printNeighbors()
            
            # for each existing router, neighbors and link lists are updated
            # to reflect new connection to new router
            for r in self.listRouters:
                if(r.getIP() == linkIP and r.getIP() != ip):
                    r.addLink(weight, ip, self)
                    r.addNeigh(ip, self)
#                     r.printNeighbors()
#                     print("Link added between",r.getIP(), "and", ip)
            i += 1
        print("Router created ...", ip)
        
        # each router's forwarding table is updated
        for n in self.listRouters:
            if(n.getLinks() != None and n.getNeighbors() != None):
#                 n.printNeighbors()
#                 print("Creating table for", n.getIP())
                self.createTable(n)
    
    # updates the given source router's forwarding table
    def createTable(self, src):
        
        # visited node list initialized with source node, source pathCost is 0, minCost is infinity
        src.visited = []
        src.pathCost = 0;
        src.visited.append(src);
#         print("appending", src.getIP())
        minCost = float("inf")
        
        # each node that is not the source is initialized to infinity
        for r in self.listRouters:
            if(r.getIP() != src.getIP()):
                r.pathCost = float("inf")
        x = None
        minLink = None
        
        # each link attached to source has its pathCost initialized to the link's weight
        # the minimum link to visit next is chosen using smallest pathCost
        for l in src.getLinks():
#             print("l is", l.getLink(1), "-", l.getLink(2))
            if(l.getLink(1) == src.getIP()):
                x = self.getRouter(l.getLink(2))
#                 print("grabbed link 2", l.getLink(2))
                x.pathCost = l.getWeight()
                
            if(l.getLink(2) == src.getIP()):
                x = self.getRouter(l.getLink(1))
#                 print("grabbed link 1", l.getLink(1))
                x.pathCost = l.getWeight()
                
#             print("x is", x.getIP(), "path cost:", x.pathCost)
            if(x.pathCost <= minCost):
                minCost = x.pathCost
#                 print("minCost is", minCost)
                minLink = x
        
        # if no minimum link is found, method terminates
        if(x == None or minLink == None):
            return 0
        
        # minLink is added to the visited nodes and 
        # visited is updated by the return value of updatePaths method
        src.visited.append(minLink)
#         print("appending", minLink.getIP())
        src.visited = self.updatePaths(minLink, src, src.visited)
        
        
#         src.printVisited()
        
        # forwarding table is updated, first initialized to empty
        src.table = []
        
        # for each visited node, the shortest path is traced back from node 'n'
        # destination and output link are added as a tuple to the forwarding table list
        for n in src.visited:
#             print("n is", n.getIP())
            if(n.getIP() != src.getIP() ):
                index = 0                             # index used to traverse visited list 
                curr = self.getRouter(n.getIP())      # currently evaluated node 
                newSrc = self.getRouter(src.getIP())  # previous node
                
                
                while(True):
#                     print("are neighbors:", curr.isNeigh(newSrc.getIP()))
#                     print("correct path:", newSrc.pathCost + self.getLinkWeight(curr, newSrc) == curr.pathCost)

                    # if the current node is not the source and it's path cost is equal to
                    # the path cost of the previous node + the link weight between both nodes,
                    # and the previous node is the source, then the output link to the current's destination is itself

                    if((curr.isNeigh(newSrc.getIP())) and 
                       (newSrc.pathCost + self.getLinkWeight(curr, newSrc) == curr.pathCost)):
                        if(newSrc.getIP() == src.getIP()):
#                             print("neighbors and source newSrc:", newSrc.getIP(), "curr:", curr.getIP(), "index:", index)
                            break
                        else:
#                             print("neighbors not source newSrc:", newSrc.getIP(), "curr:", curr.getIP(), "index:", index)
                            curr = self.getRouter(src.visited[index].getIP())
                            break
                    else:
#                         print("not neighbors/not path newSrc:", newSrc.getIP(), "curr:", curr.getIP(), "index:", index)
                        index += 1
                        if(index > 2):
#                             src.printTable()
                            return  
#                         print("index changed to", index)
                        newSrc = self.getRouter(src.visited[index].getIP())
                        
                src.table.append((n.getIP(), curr.getIP()))
#                 src.printTable()
#         src.printTable()                
        
    # the shortest path from the source node to every other node is computed recursively using Dijkstra's algorithm 
    # and the pathCosts of each node are updated
    def updatePaths(self, min, src, visited):
        newMin = None
        minCost = float("inf")
#         print("min =", min.getIP())
        
        # for each link connected to the current min cost link, their pathCosts are updated
        # if they are larger than the min.pathCost + the link weight between them
        for l in min.getLinks():
            r2IP = ""
            if(l.getLink(1) == min.getIP()):
                r2IP = l.getLink(2)
#                 print("2grabbed link 2", r2IP, "from", min.getIP())
                
            if(l.getLink(2) == min.getIP()):
                r2IP = l.getLink(1)
#                 print("2grabbed link 1", r2IP, "from", min.getIP())
            
            r2 = self.getRouter(r2IP)
            if(r2 == "Router does not exist."):
                continue
#             print("r2 is", r2.getIP())
            if(r2IP != src.getIP() and r2.pathCost > l.getWeight() + min.pathCost):
                r2.pathCost = l.getWeight() + min.pathCost
        
        # after path costs are updated, the new minimum link that has not been visited before is chosen 
        # and passed in the recursive call with the old min as the new src node
        for r in self.listRouters:
            if(r.pathCost <= minCost and r.getIP() != src.getIP() and not(self.isVisited(r.getIP(), visited))):
                minCost = r.pathCost
                newMin = self.getRouter(r.getIP())
        if(newMin == None):
            return visited
        visited.append(newMin)
#         newMin.printLinks()
#         print("appending", newMin.getIP())
        if(len(visited) == len(self.listRouters)):
#             print("visited returned")
            return visited
        else: 
            return self.updatePaths(newMin, min, visited)  



# graph = Graph()
#
# print("Welcome to Group Awful's Awful-Network-Simulator\u00a9 (by Travis Anderson & Chandler Staggs)",
#       "\nBelow, you can see the current state of the network.",
#       "\nType the appropriate key to add routers, remove routers, and view a particular router's forwarding table.")
#
# while(True):
#
#     ######### DISPLAY NETWORK STATE HERE #############
#     print("------------- Network State -------------",
#           "\nRouter|-Link Weight->|Link ")
#
#
#     if(graph.listRouters != []):
#         for r in graph.listRouters:
#             i = 1
#             if(len(graph.listRouters) == 1):
#                 print (r.getIP())
#             for l in r.getLinks():
#                 if(i == 1):
#                     print(r.getIP()+"|-"+ str(graph.getLinkWeight(r, graph.getRouter(l.getLink(2)))) +"->|"+l.getLink(2))
#                     i += 1
#                 else:
#                     print("          "+"|-"+ str(graph.getLinkWeight(r, graph.getRouter(l.getLink(2)))) +"->|"+l.getLink(2))
#
#
#     userIn = input("Add router: 'a' || Remove router: 'r' || View Forwarding Table: 'f' || Exit: 'e' -> ")
#
#     if(userIn == "a"):
#         graph.addRouter()
#     elif(userIn == "r"):
#         ip = input("Please enter the IP address of the router you wish to remove: ")
#         if(graph.getRouter(ip) == "Router does not exist."):
#             print("Router does not exist. Please try again.")
#             continue
#         else:
#             graph.rmRouter(ip)
#     elif(userIn == "f"):
#         ip = input("Please enter the IP address of the router you wish to see the forwarding table of: ")
#         if(graph.getRouter(ip) == "Router does not exist."):
#             print("Router does not exist. Please try again.")
#             continue
#         else:
#             graph.getRouter(ip).printTable()
#     elif(userIn == "e"):
#         exit(0)
#     else:
#         print("Please enter a valid key option.")

    



    

