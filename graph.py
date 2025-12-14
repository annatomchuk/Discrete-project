import random
import time
import statistics
import matplotlib.pyplot as plt
import networkx as nx
class Graph:
    def __init__(self,n,use_matrix=False):
        #use_matrix=False список суміжності
        #use_matrix=True матриця суміжності
        self.n=n
        self.use_matrix=use_matrix
        if use_matrix:
            self.matrix=[[0]*n for i in range(n)]
            self.adj=None
        else:
            self.adj=[[] for i in range(n)]
            self.matrix=None
    def add_edge(self,u,v):
        #u-v додає орієнтоване ребро
        if self.use_matrix:
            self.matrix[u][v]=1
        else:
            self.adj[u].append(v)
    def to_adj_list(self):
        #перетворює матрицю суміжності в список
        if self.adj is not None:
            return
        self.adj=[[] for i in range(self.n)]
        for u in range(self.n):
            for v in range(self.n):
                if self.matrix[u][v]==1:
                    self.adj[u].append(v)
    #список суміжності-матриця суміжності
    def to_matrix(self):
        #Перетворює список суміжності в матрицю
        if self.matrix is not None:
            return
        self.matrix=[[0]*self.n for i in range(self.n)]
        for u in range(self.n):
            for v in self.adj[u]:
                self.matrix[u][v]=1
def generate_random_DAG(n,density,use_matrix=False):
    #генеруємо випадковий орієнтований граф з н вершин та щільністю
    g=Graph(n,use_matrix)
    max_edges=n*(n-1)//2
    target_edges=int(max_edges*density)
    perm=list(range(n))
    random.shuffle(perm)
    pos={perm[i]: i for i in range(n)}
    edges=set()
    while len(edges)<target_edges:
        u=random.randrange(n)
        v=random.randrange(n)
        if u==v:
            continue
        if pos[u]<pos[v]:
            edges.add((u,v))
        else:
            edges.add((v,u))
    for u, v in edges:
        g.add_edge(u,v)
    return g
def toposort_dfs(graph:Graph):
    graph.to_adj_list()
    n=graph.n
    visited=[False]*n
    on_stack=[False]*n
    order=[]
    def dfs(u):
        visited[u]=True
        on_stack[u]=True
        for v in graph.adj[u]:
            if not visited[v]:
                dfs(v)
            elif on_stack[v]:
                raise ValueError("Граф має цикл, топологічне сортування неможливе")
        on_stack[u]=False
        order.append(u)
    for u in range(n):
        if not visited[u]:
            dfs(u)
    return order[::-1]
def run_experiments():
    #Починає експеримент різні розміри, щільності, два подання графа
    sizes=[20,40,60,80,100,120,140,160,180,200]
    densities=[0.05,0.1,0.2,0.4,0.7]
    trials=20
    results=[]
    for use_matrix in [False,True]:
        mode="matrix" if use_matrix else "list"
        print(f"\n PREDST: {mode}________\n")
        for n in sizes:
            for d in densities:
                times=[]
                for i in range(trials):
                    g=generate_random_DAG(n,d,use_matrix)
                    t1=time.perf_counter()
                    toposort_dfs(g)
                    t2=time.perf_counter()
                    times.append(t2-t1)
                avg=statistics.mean(times)
                results.append((mode,n,d,avg))
                print(f"{mode} n={n:3d} density={d:.2f}  time={avg:.6f} s")
    return results
def plot_results(results):
    #будує графік залежно від часу роботи алгоритму
    sizes=sorted(set(r[1] for r in results))
    densities=sorted(set(r[2] for r in results))
    colors=["blue","green","red","purple","orange"]
    plt.figure(figsize=(12,6))
    #графік для списку суміжності
    for i,d in enumerate(densities):
            filtered=[r for r in results if r[0]=="list" and r[2]==d]
            times=[r[3] for r in filtered]
            plt.plot(
                sizes,
                times,
                marker="o",
                color=colors[i],
                label=f"density={d}"
            )
    plt.title("Топологічне сортування DFS - список суміжності")
    plt.xlabel("Кількість вершин n")
    plt.ylabel("Середній час (секунди)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    #Графік для матриці суміжності
    for i,d in enumerate(densities):
            filtered=[r for r in results if r[0]=="matrix" and r[2]==d]
            times=[r[3] for r in filtered]
            plt.plot(
                sizes,
                times,
                marker="s",
                linestyle="--",
                color=colors[i],
                label=f"density={d}"
            )
    plt.title("Топологічне сортування DFS - матриця суміжності")
    plt.xlabel("Кількість вершин n")
    plt.ylabel("Середній час (секунди)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
def graph(graph:Graph, title="Візуальне представлення графа"):
    graph.to_adj_list()
    G=nx.DiGraph()
    G.add_nodes_from(range(graph.n))
    for u in range(graph.n):
        for v in graph.adj[u]:
            G.add_edge(u,v)
    pos=nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6,5))
    nx.draw(
        G,pos,
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        arrowsize=20,
        font_size=10
    )
    plt.title(title)
    plt.show()
if __name__=="__main__":
    print("")
    demo=Graph(5,use_matrix=False)
    demo.add_edge(0,1)
    demo.add_edge(0,2)
    demo.add_edge(1,3)
    demo.add_edge(2,3)
    demo.add_edge(3,4)
    print("Демонстрація топологічного графу")
    print("Список суміжності:")
    for i, neigh in enumerate(demo.adj):
        print(f"{i}:{neigh}")
    order=toposort_dfs(demo)
    print("Топологічний порядок", order)
    print("\nЗапуск ")
    results=run_experiments()
    print("\nПобудова графіків")
    plot_results(results)
    print("\n Готово")
    graph(demo,"")
