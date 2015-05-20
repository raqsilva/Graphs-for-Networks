# -*- coding: utf-8 -*-

class MyGraph:
    def __init__(self,g={}):
        self.graph=g
    
    def printGraph(self):
        for v in self.graph.keys():
            print(str(v)+"->"+str(self.graph[v]))
    
    def getNodes(self):
        return self.graph.keys()
    
    def getEdges(self):#Arcos
        edges=[]
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges

    def addVertex(self,v):
        if v not in self.graph.keys():
            self.graph[v]=[]
        
    def addEdge(self,o,d):
        if o not in self.graph.keys():
            self.addVertex(o)
        if d not in self.graph.keys():
            self.addVertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)
        
    def getSuccessors(self,v):
        return self.graph[v]
    
    def getPredecessors(self,v):
        res=[]
        for vert in self.graph.keys():
            if v in self.graph[vert]:
                res.append(vert)
        return res
    
    def getAdjacents(self,v):#sucessores e predecessores nao repetidos
        suc=self.getSuccessors(v)
        pred=self.getPredecessors(v)
        res=pred
        for p in suc:
            if p not in res:
                res.append(p)
        return res

    def outDegree(self,v):
        return len(self.graph[v])
    
    def inDegree(self,v):
        res=0
        for k in self.graph.keys():
            if v in self.graph[k]:
                res += self.graph[k].count(v)
        return res
        
    def degree(self,v):
        return len(self.getAdjacents(v))
    
    def allDegrees(self,deg_type="inout"):
        degs={}
        for v in self.graph.keys():
            if deg_type=="out" or deg_type=="inout":
                degs[v]=len(self.graph[v])
            else:
                degs[v]=0
        if deg_type=="in" or deg_type=="inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type=="in" or v not in self.graph[d]:
                        degs[d]=degs[d] + 1
        return degs

    def meanDegree(self, deg_type="inout"):
        degs=self.allDegrees(deg_type)
        return sum(degs.values())/float(len(degs))
        
    def probDegree(self, deg_type="inout"):
        degs=self.allDegrees(deg_type)
        res={}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]]+=1
            else:
                res[degs[k]]=1
        for k in res.keys():
            res[k]/=float(len(degs))
        return res
        
    def reachableBFS(self,v):
        l=[v]
        res=[]
        while len(l)>0:
            node=l.pop(0)
            if node !=v:
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.append(elem)
        return res
        
    def reachableDFS(self,v):
        l=[v]
        res=[]
        while len(l)>0:
            node=l.pop(0)
            if node !=v:
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(0,elem)
        return res
        
    def distance(self,s,d):
        if s==d:
            return 0
        l=[(s,0)]
        visited=[s]
        while len(l)>0:
            node, dist=l.pop(0)
            for elem in self.graph[node]:
                if elem==d:
                    return dist+1
                elif elem not in visited:
                    l.append((elem,dist+1))
                    visited.append(elem)
        return float("inf")#acontece quando o nó não é atingivel

    def shortestPath(self,s,d):
        if s==d:
            return 0
        l=[(s,[])]
        visited=[s]
        while len(l)>0:
            node, preds=l.pop(0)
            for elem in self.graph[node]:
                if elem==d:
                    return preds+[node,elem]
                elif elem not in visited:
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None

    
    def reachableWithDist(self,s):
        res=[]
        l=[(s,0)]
        while len(l)>0:
            node, dist=l.pop(0)
            if node!=s:
                res.append((node,dist))
            for elem in self.graph[node]:
                if not isinTupleList(l,elem) and not isinTupleList(res,elem):
                    l.append((elem,dist+1))
        return res
    
    
    
    def nodeHasCycle(self,v):
        l=[v]
        res=False
        visited=[v]
        while len(l)>0:
            node=l.pop(0)
            for elem in self.graph[node]:
                if elem==v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res
    
    def hasCycle(self):
        res=False
        for v in self.graph.keys():
            if self.nodeHasCycle(v):
                return True
        return res
    
    
    def clusteringCoef(self,v):
        adjs=self.getAdjacents(v)
        if len(adjs)<=1:
            return 0   ##returning None
        ligs=0
        for i in adjs:
            for j in adjs:
                if i!=j:
                    if j in self.graph[i]:
                        ligs=ligs+1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
      
      
    def size(self):
        return len(self.getNodes()),len(self.getEdges())
    
    
    def meanDistances(self):
        tot=0
        num_reachable=0
        for k in self.graph.keys():
            distsk=self.reachableWithDist(k)
            for _, dist in distsk:
                tot +=dist
            num_reachable +=len(distsk)
        meandist=float(tot)/num_reachable
        n=len(self.getNodes())
        return meandist, float(num_reachable)/((n-1)*n)

      
    def allClusteringCoefs(self):
        ccs= {}
        for k in self.graph.keys():
            ccs[k]=self.clusteringCoef(k)
        return ccs
    
    
    def meanClusteringCoef(self):
        css=self.allClusteringCoefs()
        return sum(css.values())/float(len(css))
        
    
    def meanClusteringPerDeg(self, deg_type="inout"):
        degs=self.allDegrees(deg_type)
        css=self.allClusteringCoefs()
        degs_k={}
        for k in degs.keys():
            if degs[k] in degs_k:
                degs_k[degs[k]].append(k)
            else:
                degs_k[degs[k]]=[k]
        ck={}
        for k in degs_k.keys():
            tot=0
            for v in degs_k[k]:
                tot+=css[v]
            ck[k]=float(tot)/len(degs_k[k])
        return ck
         

    def checkIfValidPath(self,p):
        if p[0] not in self.graph:
            return False
        for i in range(1,len(p)):
            if p[i] not in self.graph or p[i] not in self.graph[p[i-1]]:
                return False
        return True
        
        
    def checkIfHamiltonianPath(self,p):
        if not self.checkIfValidPath(p):
            return False
        to_visit=list(self.getNodes())
        if len(p) != len(to_visit):
            return False
        for i in range(len(p)):
            if p[i] in to_visit:
                to_visit.remove(p[i])
            else:
                return False
        if not to_visit:
            return True
        else:
            return False       

  
    def searchHamiltonianPath(self):
        for ke in self.graph.keys():
            p= self.searchHamiltonianPathFromNode(ke)
            if p: return p
        return None
        
        
    def searchHamiltonianPathFromNode(self,start):
        current=start
        visited={start:0}
        path=[start]
        while len(path) < len(self.getNodes()):
            nxt_index=visited[current]
            if len(self.graph[current]) > nxt_index:
                nxt_node=self.graph[current][nxt_index]
                visited[current] += 1
                if nxt_node not in path:
                    path.append(nxt_node)
                    visited[nxt_node]=0
                    current=nxt_node
            else:
                if len(path) > 1:
                    rmv_node=path.pop()
                    del visited[rmv_node]
                    current=path[-1]
                else:
                    return None
        return path
                        

    def checkBalancedNode(self, node):
        return self.inDegree(node)==self.outDegree
        
    
    def checkBalancedGraph(self):
        for n in self.graph.keys():
            if not self.checkBalancedNode(n):
                return False
        return True
        
    def eulerianCycle(self):
        if not self.checkBalancedGraph():
            return None
        edges_visit=list(self.getEdges())
        res=[]
        while edges_visit:
            pair=edges_visit[0]
            i=1
            if res!=[]:
                while pair[0] not in res:
                    pair=edges_visit[i]
                    i=i+1
            edges_visit.remove(pair)
            start, nxt= pair
            cycle =[start, nxt]
            while nxt!= start:
                for suc in self.graph[nxt]:
                    if (nxt, suc) in edges_visit:
                        pair=(nxt, suc)
                        nxt=suc
                        cycle.append(nxt)
                        edges_visit.remove(pair)
            if not res:
                res=cycle
            else:
                pos=res.index(cycle[0])
                for i in range(len(cycle)-1):
                    res.insert(pos + i + 1, cycle[i+1])
        return res
 

    def checkNearlyBalancedGraph(self):
        res=-1,-1
        for n in self.graph.keys():
            indeg= self.inDegree(n)
            outdeg= self.outDegree(n)
            if indeg-outdeg ==1 and res[1]==-1:
                res=res[0],n
            elif indeg-outdeg==-1 and res[0]==-1:
                res=n,res[1]
            elif indeg==outdeg:
                pass
            else:
                return -1,-1
        return res


    def eulerianPath(self):
        unb=self.checkNearlyBalancedGraph()
        if unb[0]<0 or unb[1]<0:
            return None
        self.graph[unb[1]].append(unb[0])
        cycle=self.eulerianCycle()
        for i in range(len(cycle)-1):
            if cycle[i]==unb[1] and cycle[i+1]==unb[0]:
                break
        path= cycle[i+1]+cycle[1:i+1]
        return path


       
def isinTupleList(tl,val):
    res=False
    for (x,y) in tl:
        if val==x:
            return True
    return res    
        


#funcoes de teste
def grafo1():
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    gr.printGraph()
    print(gr.getNodes())
    print(gr.getEdges())

def grafo2():#Grafo 2 - criar vertices e arcos
    gr2=MyGraph()
    gr2.addVertex(1)
    gr2.addVertex(2)
    gr2.addVertex(3)
    gr2.addVertex(4)
    gr2.addEdge(1,2)
    gr2.addEdge(2,3)
    gr2.addEdge(3,2)
    gr2.addEdge(3,4)
    gr2.addEdge(4,2)
    gr2.printGraph()

def grafo3():#Grafo 3 - Graus  
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    gr.printGraph()
    print(gr.getSuccessors(2))
#    s=gr.getSuccessors(2)
#    print(s)
#    s.append(4)
#    gr.printGraph()
    print(gr.getPredecessors(2))
    print(gr.getAdjacents(2))
    print(gr.inDegree(2))
    print(gr.outDegree(2))
    print(gr.degree(2))

def grafo4():#mais graus
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    print(gr.allDegrees())
    print(gr.meanDegree())
    print(gr.probDegree())
    

def grafo5():#travessia dos grafos
    gr2=MyGraph({1:[2,3],2:[4],3:[5],4:[],5:[]})
    print(gr2.distance(2,1))
    print(gr2.distance(1,5))
    print(gr2.reachableBFS(1))#em largura
    print(gr2.reachableDFS(1))#em profundidade
    print("\nGrafo seguinte")
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    print(gr.distance(1,4))
    print(gr.distance(4,3))
    print("\nGrafo seguinte")
    gr2=MyGraph({1:[2,3],2:[4],3:[5],4:[],5:[]})
    print(gr2.distance(2,1))
    print(gr2.distance(1,5))


def grafo6():
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    print(gr.shortestPath(1,4))
    print(gr.shortestPath(4,3))
    gr2=MyGraph({1:[2,3],2:[4],3:[5],4:[],5:[]})
    print(gr2.shortestPath(1,5))
    print(gr2.shortestPath(2,1))


def grafo7():
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    print(gr.reachableWithDist(1))
    print(gr.reachableWithDist(3))
    gr2=MyGraph({1:[2,3],2:[4],3:[5],4:[],5:[]})
    print(gr2.reachableWithDist(1))
    print(gr2.reachableWithDist(5))


def grafo8():
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    print(gr.nodeHasCycle(2))
    print(gr.nodeHasCycle(1))
    print(gr.hasCycle())
    gr2=MyGraph({1:[2,3],2:[4],3:[5],4:[],5:[]})
    print(gr2.nodeHasCycle(1))
    print(gr2.hasCycle())


def grafo9():
    gr=MyGraph({1:[2],2:[3],3:[2,4],4:[2]})
    print(gr.clusteringCoef(1))
    print(gr.clusteringCoef(2))
    gr2=MyGraph({1:[2,3],2:[4],3:[5],4:[],5:[]})
    print(gr2.clusteringCoef(1))
    gr3=MyGraph({1:[2,3],2:[1,3],3:[1,2]})
    print(gr3.clusteringCoef(1))


def grafo10():
    gr=MyGraph({1:[2],2:[3,1],3:[4],4:[2,5],5:[6],6:[4]})
    gr.printGraph()
    print(gr.checkBalancedGraph())
    print(gr.eulerianCycle())


def grafo11():
    gr=MyGraph({1:[2],2:[3,1],3:[4],4:[2,5],5:[6],6:[]})
    gr.printGraph()
    print(gr.checkBalancedGraph())
    print(gr.checkNearlyBalancedGraph())
    print(gr.eulerianPath())


if __name__ == "__main__":
#    print("Grafo 1")    
#    grafo1()
#    print("\nGrafo 2")
#    grafo2()
#    print("\nGrafo 3")
#    grafo3()
#    print("\nGrafo 4")
#    grafo4()
#    print("\nGrafo 5")
#    grafo5()
#    print("\nGrafo 6")
#    grafo6()
#    print("\nGrafo 7")
#    grafo7()
#    print("\nGrafo 8")
#    grafo8()
#    print("\nGrafo 9")
#    grafo9()
    grafo10()
    grafo11()