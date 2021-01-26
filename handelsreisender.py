import json, time
graph_strings = [
    "Bernburg - Köthen - Bitterfeld - Delitzsch - Leipzig",
    "Köthen - Dessau - Wolfen - Bitterfeld - Halle",
    "Könnern - Bitterfeld",
    "Bernburg - Könnern - Halle - Merseburg",
    "Halle - Leipzig",
    "Halle - Leipzig",
    "Querfurt - Eisleben - Teutschenthal - Halle",
    "Leipzig - Merseburg - Querfurt - Teutschenthal"
]

graph = {

}

def add_edge(start, end):
    if start in graph:
        if not end in graph[start]:
            graph[start].append(end)
    else:
        graph[start] = []
        graph[start].append(end)

def make_graph():

    for string in graph_strings:
        places = string.split(" - ")
        for i in range(len(places)):
            if i > 0:
                add_edge(places[i], places[i-1])
                add_edge(places[i-1], places[i])
            elif i < len(places)-1:
                add_edge(places[i], places[i+1])
                add_edge(places[i+1], places[i])

def find_cycles():
    print(graph)
    print("\nEs gibt " + str(len(graph)) + " verschiedene Städte.")
    start = input("\nStartstadt eingeben: ")

    path_indices = []
    cycles = []

    def get_last_knot(path_indices):
        knot = graph[start]
        for each in path_indices[0:-1]:
            knot = graph[knot[each]]
        return knot

    def get_path(path_indices):
        path = [start]
        knot = start
        out = graph[start]
        for each in path_indices:
            knot = out[each]
            out = graph[knot]
            path.append(knot)
        return path

    def check_for_cycle(path_indices):
        path = [start]
        knot = start
        out = graph[start]
        for each in path_indices:
            knot = out[each]
            out = graph[knot]
            if knot in path:
                path.append(knot)
                return True
            else:
                path.append(knot)
        return False

    found_all = False
    while not found_all:
        # Pfad erweitern, bis Zyklus gefunden wird
        cycle = False
        while not cycle:
            cycle = check_for_cycle(path_indices)
            if not cycle:
                path_indices.append(0)
        if not cycle in cycles:
            cycles.append(get_path(path_indices))

        # Im Pfad zurückgehen, bis man verzweigen kann
        while True:
            last_knot = get_last_knot(path_indices)
            siblings_count = len(last_knot)
            last_path_index = path_indices[-1]

            if siblings_count-1 > last_path_index:
                incr = path_indices.pop()
                incr += 1
                path_indices.append(incr)
                if len(path_indices) == 1:
                    found_all = True
                break
            else:
                path_indices.pop()

    solutions = []

    for each in cycles:
        if len(each) == len(graph)+1 and each[0] == each[-1]:
            solutions.append(each)

    print("\nLösungen: \n")
    print(solutions)

    print("\n" + str(len(solutions)) + " Lösung(en) gefunden!")

make_graph()
find_cycles()

