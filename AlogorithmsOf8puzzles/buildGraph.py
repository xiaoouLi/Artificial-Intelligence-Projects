import cPickle as pickle
import sys

### build graph:
### takes as input a file in the form:
## a b dist time
### where a and b are destinations, dist is the distance between them, and
### time is the time needed to travel between them and constructs a graph.

### This graph should be represented as an adjacency list, and stored as a
### dictionary, with the key in the dictionary being the source of an edge and
### the value being a tuple containing the destination, distance, and cost.
### For example:
### g[a] = (b,dist,time)

class Graph:
    def __init__(self, infile=None) :
        self.adjlist = {}
        if infile :
            self.buildGraph(infile)

    ### method to print a graph.
    def __repr__(self) :
        return '%s' % self.adjlist

    ### helper methods to construct edges and vertices. Use these in buildGraph.
    def createVertex(self, inStr) :
        name, lat,longitude = inStr.split(" ",2)
        lat = lat.split("=")[1]
        longitude = longitude.split("=")[1]
        return Vertex(name, lat, longitude)

    def createEdges(self, inStr) :
        src, dest, dist, time = inStr.split(" ",4)
        dist = dist.split("=")[1]
        time=time.split("=")[1]
        e1 = Edge(src,dest,dist, time)
        e2 = Edge(dest,src,dist, time)
        return e1, e2

### method that takes as input a file name and constructs the graph described
### above.
    def buildGraph(self, infile) :
        f = open(infile)
        line = f.readline()
    ## consume comments
        while line.startswith("#") :
            line = f.readline().strip()
    ## create vertices
        while not line.startswith("#") and len(line) > 1 :
            v = self.createVertex(line)
            ### adjlist is indexed by the string representing the
            ##location. The first object in the list is the vertex,
            ## which is saved for more complete book-keeping
            ## (note there are other ways to do this)
            self.adjlist[v.name]=[v]
            line = f.readline().strip()
    ## consume comments
        while line.startswith("#") or len(line) <= 1 :
            line = f.readline().strip()
    ## create edges
        while line and len(line) > 1 :
            e1,e2 = self.createEdges(line)
            self.adjlist[e1.src].append(e1)
            self.adjlist[e2.src].append(e2)
            line = f.readline().strip()


### this method should take as input the name of a starting vertex
### and compute Dijkstra's algorithm,
### returning a dictionary that maps destination cities to
### a tuple containing the length of the path, and the vertices that form the path.
    def dijkstra(self, source) :
        pass

### classes representing vertices and edges

class Vertex:
    def __init__(self, name, lat, longitude) :
        self.name = name
        self.lat = lat
        self.longitude = longitude
    def __hash__(self) :
        return hash(self.name)
    def __repr__(self):
        return self.name
    def __eq__(self, other) :
        return self.name == other.name

class Edge:
    def __init__(self, src, dest, distance, time) :
        self.src = src
        self.dest = dest
        self.distance = distance
        self.time = time
    def __repr__(self):
        return "(%s, %s, %s, %s)" % (self.src, self.dest, self.distance, self.time)


### usage: buildGraph {--pfile=outfile} {-d=startNode} infile
### if --pfile=outfile is provided, write a pickled version of the graph
### to outfile. Otherwise, print it to standard output.
### if --d=startNode is provided, compute dijkstra with the given starting node
###  as source
### Doesn't
if __name__ == '__main__' :
    #g = Graph("/Users/cindi/Documents/Teaching/AI/assignments/HW1/sfdata.txt")
    #print g

    #with open("sfdata.p", 'w') as f:
    #    pickle.dump(g, f)
    #g2 = Graph("/Users/cindi/Documents/Teaching/AI/students/HW1/buildG/wikidata.txt")
    outfile = None
    for arg in sys.argv[1:-1]:
        if arg.startswith("--pfile="):
            outfile=arg[8:]
        elif arg.startswith["-d="]:
            startNode = arg[3:]
    infile = sys.argv[-1]
    g = Graph(infile)
    if outfile:
        pickle.dump(g, open(outfile, 'wb'))
    else:
        print g





