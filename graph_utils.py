from random import shuffle
# Retorna o index do vértice(célula) no sudoku.
def index(l, c):
    return 9 * l + c

# Cria o grafo do sudoku, do seguinte formato:
#   [A1,A2,A3...] onde A é uma aresta da forma: (v1,v2)
#   [(v1,v2),(v2,v3),(v3,v4)...]
#   As arestas são feitas em cada linha, coluna e quadrante do sudoku.
def mk_sudoku_graph():
    # edge = (Vi, Vi+1)
    def mk_complete_graph(vertices):
        graph = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                edge = (vertices[i], vertices[j])
                graph += [tuple(sorted(edge))]
        return graph
    graph = []
    # Arestas da linha.
    for r in range(9):
        edges = []
        for c in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    # Arestas da coluna.
    for c in range(9):
        edges = []
        for r in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    # Arestas do quadrante.
    for rb in range(0, 9, 3):
        for cb in range(0, 9, 3):
            edges = []
            for r in range(3):
                for c in range(3):
                    edges += [index(rb + r, cb + c)]
            graph += mk_complete_graph(edges)
    # Remove duplicados.
    return list(set(graph))

# Converte a lista graph[] em um dictionary de adjacências da forma:
# {
#   index_V0:[index_V0_adj],
#     ...
#   index_Vi:[index_Vi_adj]
#  }
def adj_list(graph):
    adj = {}
    def insert_edge(v1, v2):
        if v1 in adj:
            adj[v1] += [v2]
        else:
            adj[v1] = [v2]
    for (v1, v2) in graph:
        insert_edge(v1, v2)
        insert_edge(v2, v1)
    return adj

# Variáveis globais.
adjacencies = adj_list(mk_sudoku_graph())
colors = [0]*81
fixed = [False]*81
ncolor = 0
debug = False

# Lê o sudoku do txt passado.
def read_puzzle():
    global ncolor
    f = open('sudoku.txt')
    for r in range(9):
        l = f.readline()
        for c in range(9):
            if l[c] == '.':
                continue
            v = index(r, c)
            # Marca a linha ja preenchida como fixo.
            fixed[v] = True
            # Adiciona a cor(valor) em colors
            colors[v] = int(l[c])
            # Incrementa o número de vértices(células) coloridas.
            ncolor += 1

# Imprime as soluções.
def print_solution(soln):
    for r in range(9):
        for c in range(9):
            v = soln[index(r, c)]
            if v == 0:
                print(".", end="")
            else:
                print(v, end="")
        print()



# Função de coloração:
def color_puzzle(max_solns, shuffle_colors):
    global ncolor, colors, debug
    if debug:
        print("coloring %d" % (ncolor,))
    # Verificação de casos base.
    if max_solns != None and max_solns <= 0:
        return []
    if ncolor >= 81:
        return [colors*1]
    # Retorna as cores dos vizinhos de v para saber de quais cores são possíveis pintar v.
    def neighbor_colors(v):
        ncs = set([])
        for v0 in adjacencies[v]:
            if colors[v0] > 0:
                ncs = ncs.union({colors[v0]})
        return ncs
    # Encotra o primeiro v que tem o menor numero de cores possiveis.
    def most_constrained_free():
        ncs = -1
        target = -1
        for v in range(len(colors)):
            # Don't recolor a vertex
            if colors[v] > 0:
                continue
            ncsv = len(neighbor_colors(v))
            if ncsv > ncs:
                target = v
                ncs = ncsv
        assert target != -1
        return target
    # Retorna o primeiro vértice sem cor.
    def first_free():
        for v in range(len(colors)):
            if colors[v] == 0:
                return v
        assert False
    # No point in MCF if all solutions? I'm not sure
    # this is right / needed
    if max_solns == 1:
        v = most_constrained_free()
    else:
        v = first_free()
    # Retorna os valores válidos de cor para v.
    cs = set(range(1,10)).difference(neighbor_colors(v))
    # Se não existir cor possível.
    if len(cs) == 0:
        return []
    # Embaralha as cores
    if shuffle_colors:
        cs = list(cs)
        shuffle(cs)
    # Testa as cores possiveis para v, chamando color_puzzle() recursivamente
    # e caso ache inclui a solução na lista de soluções solns
    ncolor += 1
    solns = []
    for c in cs:
        if debug:
            print("coloring %d with %d (%d)" % (v, c, ncolor))
        colors[v] = c
        solns_cur = color_puzzle(max_solns, shuffle_colors)
        if debug:
            print("found %d solutions" % (len(solns_cur),))
        solns += solns_cur
        if max_solns != None:
            max_solns -= len(solns_cur)
            if max_solns <= 0:
                break
    colors[v] = 0
    ncolor -= 1
    # Retorna as soluções
    return solns
