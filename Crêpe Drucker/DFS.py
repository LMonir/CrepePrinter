def dfs(graph, node, visited):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(graph, neighbor, visited)
                print(f"Back to: {node}") #Hier den Teigfluss unterbinden

# Beispielverwendung
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
    'G': ['H', 'J'],
    'H': ['G', 'J'],
    'J': ['G', 'H'],
}

nodes = ['A','B','C','D','E','F','G','H','J']

while len(nodes) > 0:
    visited = set()
    node = nodes[0]
    dfs(graph, node, visited)
    nodes = [x for x in nodes if x not in visited]
