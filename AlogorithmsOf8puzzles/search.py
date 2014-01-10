import buildGraph
import searchQueues
import argparse
import math

### A NodeFactory is a helper class that is used to create new Nodes.
### It stores the graph representing our problem and uses it to find successors.
MAX = 99999

class NodeFactory :
    def __init__(self, inputgraph) :
        self.inputgraph = inputgraph

    ### return a list of all nodes reachable from this state
    ### you complete this.
    ### For a given node, find the corresponding vertex in the input graph.
    ### Find the vertices it is connected to, and generate a Node for each
    ### one. Update parentState and cost to reflect the new edge added to the
    ### solution.
    ### nlist is a list of successor nodes.

    def successors(self, oldstate) :
        nlist = []
        for e in self.inputgraph.adjlist[oldstate.vertex.name]:
            if isinstance(e,buildGraph.Edge):
                #find the connected vertex(not a edge)
                vertex = None
                for i in self.inputgraph.adjlist.keys():
                    if i == e.dest:
                        vertex = self.inputgraph.adjlist[i][0]
                        break
        # get all connected nodes
        # I read in the distance and remove the "km" after the length
                nlist.append(Node(vertex,oldstate,oldstate.cost + float(e.distance[:-2])))
        return nlist

class Node:
    def __init__(self, vertex, parentState=None, cost=0) :
    # this cost should be the distance between
    #vertex and parent vertex, or the beginning vertex?
    # I treat it as from beginning at present.
        self.vertex = vertex
        self.parent = parentState
        self.cost = cost

    def isGoal(self, goalTest) :
        return goalTest(self)

    def isStart(self) :
        return self.parent is None

    def __repr__(self) :
        return self.vertex.__repr__()

    def __hash__(self) :
        return self.vertex.name.__hash__()

    ## you do this.
    def __lt__(self, other) : #less than
        if isinstance(other,Node):
            return self.cost<other.cost

    def __le__(self, other) :#less or equal
        if isinstance(other,Node):
            return self.cost<=other.cost

    def __gt__(self, other) :# greater than
        if isinstance(other,Node):
            return self.cost > other.cost

    def __ge__(self, other) :#greater and equal
        if isinstance(other,Node):
            return self.cost >= other.cost

    def __eq__(self, other) :#equal
        if isinstance(other,Node):
            return self.cost == other.cost and self.vertex.name == other.vertex.name
            # return self.cost == other.cost

    def __ne__(self, other) :#not equal
        if isinstance(other,Node):
            return self.cost != other.cost

### search takes as input a search queue, the initial state,
### a node factory,
### a function that returns true if the state provided as input is the goal,
### and the maximum depth to search in the search tree.
### It should print out the solution and the number of nodes enqueued, dequeued,
###  and expanded.

def IDAStarSearch(queue,initialState,factory,goalTest,hF):
    bound = hF(initialState)
    nodesEnqueued = 1
    nodesDequeued = 0
    nodesExpanded = 0
    while True:
        state,Enqueued,Dequeued,Expanded,t = subSearchForIDAStar(queue, initialState, factory, goalTest, hF, bound)
        nodesEnqueued = nodesEnqueued + Enqueued
        nodesDequeued = nodesDequeued + Dequeued
        nodesExpanded = nodesExpanded + Expanded
        if goalTest(state):
            return state,Enqueued,Dequeued,Expanded
        bound = t

def subSearchForIDAStar(queue, initialState, factory, goalTest, hF, bound):
    closedList = {}
    nodesEnqueued = 1
    nodesDequeued = 0
    nodesExpanded = 0
    minf = MAX
    minState = None
    queue.insert(initialState)

    while not queue.isEmpty():
        currentState = queue.pop()
        nodesDequeued = nodesDequeued + 1
        f = hF(currentState) + currentState.cost

        #check this before goalTest,
        #because I cut off the over bound node even though it is goal
        if f > bound:
            if f < minf:
                #store minf. When we cut off all available nodes before,
                #return the minf as the new bound.
                minf = f
                # store the minState. When we cut off all available nodes before,
                #return the minState. It's useless here, but I think there might
                #be some other places will use it in the future.
                minState = currentState
            continue
        if goalTest(currentState):
            return currentState,nodesEnqueued,nodesDequeued,nodesExpanded,minf
        else:
            for child in factory.successors(currentState):
                if child.vertex.name not in closedList.keys():
                    queue.insert(child)
                    nodesEnqueued = nodesEnqueued + 1
            closedList[currentState.vertex.name] = True
            nodesExpanded = nodesExpanded + 1
    return minState,nodesEnqueued,nodesDequeued,nodesExpanded,minf

def idsSearch(queue, initialState, factory, goalTest):
    depth = 1
    while True:
        result = search(queue, initialState, factory, goalTest, maxdepth=depth)
        if result and goalTest(result[0]):
            return result[0],result[1],result[2],result[3]
        else:
            depth = depth + 1

def search(queue, initialState, factory, goalTest, maxdepth=10) :
    closedList = {}
    nodesEnqueued = 1
    nodesDequeued = 0
    nodesExpanded = 0
    queue.insert(initialState)

    while not queue.isEmpty():
        if isinstance(queue,searchQueues.AStarQueue):
            currentState = queue.pop()[1]
        else:
            currentState = queue.pop()

        nodesDequeued = nodesDequeued + 1
        if goalTest(currentState):
            return currentState,nodesEnqueued,nodesDequeued,nodesExpanded
        else:
            if nodeDepth(currentState) < maxdepth:
                for child in factory.successors(currentState):
                    if child.vertex.name not in closedList.keys():
                        queue.insert(child)
                        nodesEnqueued = nodesEnqueued + 1
                closedList[currentState.vertex.name] = True
                nodesExpanded = nodesExpanded + 1
            elif nodeDepth(currentState) > maxdepth:
                return None,nodesEnqueued,nodesDequeued,nodesExpanded
    return None,nodesEnqueued,nodesDequeued,nodesExpanded

def nodeDepth(node):
    depth = 0
    while node.parent:
        depth = depth + 1
        node = node.parent
    return depth

### you complete this.
### While there are states in the queue,
###   1. Dequeue
###   2. If this is the goal, stop
###   3. If not, insert in the closed list and generate successors
###   4. If successors are not in the closed list, enqueue them.

### code for printing out a sequence of states that leads to a solution
def printSolution(node) :
    if node:
        print "Solution *** "
        print "cost: ", node.cost
        moves = []
        current = node
        while current.parent:
            moves.append(current)
            current = current.parent
        moves.append(current)
        moves.reverse()
        for move in moves :
            print move
    else:
        print "\n     **Failed**"
        print "Goal cannot be found!"

### usage: search --search=[BFS| DFS | AStar] {-l=depthLimit} {-i}
###               initialState goal infile
### python search.py CableCarMuseum FishermansWharf inputFile --search BFS

### If -l is provided, only search to the given depth.
### if -i is provided, use an iterative deepening version (only applies
        ### to DFS, 10pts extra credit for IDA*)
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--search",choices=["BFS", "DFS", "AStar","IDAStar"],required=True)
    parser.add_argument("-l",type=int)
    parser.add_argument("-i",action="store_true")
    parser.add_argument("initialState")
    parser.add_argument("goal")
    parser.add_argument("infile")
    args = parser.parse_args()

    if args.l and args.i:
        print "l and i cannot exist at the same time! Exit!"
        exit()

    initialState = args.initialState #string
    goal = args.goal #string
    infile = args.infile
    if args.l > 0:
        depth = args.l
    elif args.l == 0:
        print "l should be bigger than 0! Exit!"
        exit()
    else:
        depth = MAX
    iterativeFlag = args.i
    graph = buildGraph.Graph(infile)

    findG = False
    for v in graph.adjlist:
        if v == goal:
            findG = True
            goal = graph.adjlist[v][0]
            break
    if not findG:
        print "Wrong goal inputed! Exit!"
        exit()
    findI = False
    for v in graph.adjlist:
        if v == initialState:
            findI = True
            initialState = graph.adjlist[v][0]
            break
    if not findI:
        print "Wrong initialState inputed! Exit!"
        exit()

    goal = Node(buildGraph.Vertex(goal.name,goal.lat,goal.longitude))
    initialState = Node(buildGraph.Vertex(initialState.name,initialState.lat,initialState.longitude))

    def goalTest(state):
        if state:
            return state.vertex.name == goal.vertex.name
        return False

    if args.search == "BFS":
        q = searchQueues.BFSQueue()
        print "===You are doing BFS==="
        result = search(q, initialState, NodeFactory(graph), goalTest)
    elif args.search == "DFS":
        q = searchQueues.DFSQueue()
        if not args.i:
            print "===You are doing DFS==="
            if not args.l:
                result = search(q, initialState, NodeFactory(graph), goalTest)
            else:
                print "Limit level: %d" %args.l
                result = search(q, initialState, NodeFactory(graph), goalTest, depth)
        else:
            print "===You are doing IDS==="
            result = idsSearch(q, initialState, NodeFactory(graph), goalTest)
    elif args.search == "AStar":
        #calculate goal's position
        goalLong = searchQueues.convertLatLong(goal.vertex.longitude)
        goalLat = searchQueues.convertLatLong(goal.vertex.lat)
        def rad(d):
            return (d * 3.14) / 180.0
        def getDistance(lg1,lg2,lt1,lt2):
            lg1 = -lg1 * math.pi/180
            lg2 = -lg2 * math.pi/180
            lt1 = lt1 * math.pi/180
            lt2 = lt2 * math.pi/180
            a1 = -lg1
            a2 = -lg2
            a0 = (a1 - a2)/2
            b1 = lt1
            b2 = lt2
            b0 = (b1 - b2)/2
            return math.sqrt(pow(math.sin(b0),2) + math.cos(b1) * math.cos(b2) * pow(math.sin(a0),2))
        def hFunction(state):
            sLong = searchQueues.convertLatLong(state.vertex.longitude)
            sLat = searchQueues.convertLatLong(state.vertex.lat)
            return getDistance(goalLong,sLong,goalLat,sLat) * 6371 * 2

        if not args.i:
            q = searchQueues.AStarQueue(hFunction)
            print "===You are doing A*==="
            result = search(q, initialState, NodeFactory(graph), goalTest, depth)
        else:
            q = searchQueues.DFSQueue()
            print "===You are doing IDA*==="
            result = IDAStarSearch(q,initialState,NodeFactory(graph),goalTest,hFunction)
    node,enqueued,dequeued,expanded = result[0],result[1],result[2],result[3]

    printSolution(node)
    print "\nEnqueued: %d" %enqueued
    print "Dequeued: %d" %dequeued
    print "Expanded: %d" %expanded




