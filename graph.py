import random
class Graph: #створення класу для графа
    def __init__(self,n,use_matrix=False): #False-список суміжності, True-матриця суміжності
        self.n=n #кількість вершин
        self.use_matrix=use_matrix
        if use_matrix: #створення матриці
            self.matrix=[[0]*n for i in range(n)]
            self.adj=None
        else: #створення списка
            self.adj=[[] for i in range(n)]
            self.matrix=None
    def add_edge(self,u,v):
        if self.adj is not None:
            self.adj[u].append(v)
        if self.matrix is not None:
            self.matrix[u][v]=1
    def to_adjlist(self):
        if self.adj is not None:
            return self
        g=Graph(self.n,use_matrix=False)
        for u in range(self.n):
            for v in range(self.n):
                if self.matrix[u][v]:
                    g.add_edge(u,v)
        return g
    def to_matrix(self):
        if self.matrix is not None:
            return self
        g=Graph(self.n, use_matrix=True)
        for u in range(self.n):
            for v in self.adj[u]:
                g.add_edge(u,v)
        return g
def generate_random_dag(n,density):
    perm=list(range(n))
    random.shuffle(perm)
    max_edges=n*(n-1)//2
    m=int(round(max_edges*density))
    edges=set()
    pos=[0]*n
    for i,v in enumerate(perm):
        pos[v]=i
    while len(edges)<m:
        u=random.randrange(n)
        v=random.randrange(n)
        if u==v:
            continue
        if pos[u]<pos[v]:
            edges.add((u,v))
        else:
            edges.add((v,u))
    g=Graph(n,use_matrix=False)
    for (u,v) in edges:
        g.add_edge(u,v)
    return g
