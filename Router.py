class router:
    ipaddress = ""
    links = []
    neighbors = []
    table = []
    numlinks = len(links)
    weights = {}
    visited = []

    def __init__(self, ipadd, links, neigh):
        self.ipaddress = ipadd
        self.links = links
        self.neighbors = neigh
        self.table = table


    def addLink(self, dest):
        l = link(self, dest, weight)
        self.links.append[l]


    def removeLink(self):

    def removeAllLinks(self):
        for i in self.links:
            self.links.remove(self.links[i])




    def getLinks(self):
       return self.links


    def getNeighbors(self):
        return self.neighbors


    def createTable(self, graph):


    def getNumLinks(self):



class graph:
    routers = []
    links = []
    mostcurrentip = 0

    def rmrouter(self, ip):
        self.router[ip].removeAllLinks
        self.routers.remove(ip)

    def addrouter(self, ip):

        input("How many links will this router have?")
        input("What links will this router have and what weights?")
        locallinks = []
        neighbors = []

        self.routers.append(router(self.genIP(), locallinks, neighbors))

    def getLinkweight(self, router1, router2):

    def genIP(self):
        subnet= "200.25.3."
        self.mostcurrentip += 1
        return subnet+str(self.mostcurrentip)







