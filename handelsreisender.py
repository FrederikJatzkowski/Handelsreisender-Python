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

CONSTRUCTION_STRING = "Köthen → Bernburg, Bernburg → Könnern, Eisleben → Querfurt, Querfurt → Teutschenthal, Könnern → Halle, Halle → Bitterfeld, Leipzig → Delitzsch, Leipzig → Merseburg, Querfurt → Merseburg, Merseburg → Halle"

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

def remove_construction():
    constructions = CONSTRUCTION_STRING.split(", ")
    for con in constructions:
        con_arr = con.split(" → ")
        graph[con_arr[1]].remove(con_arr[0])


def find_cycles():
    print(graph)
    print("\nEs gibt " + str(len(graph)) + " verschiedene Städte.")
    start = input("\nStartstadt eingeben: ")
    end = input("\nEndstadt eingeben: ")

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
            print(get_path(path_indices))

        # Im Pfad zurückgehen, bis man verzweigen kann
        while True:
            last_knot = get_last_knot(path_indices)
            siblings_count = len(last_knot)
            last_path_index = path_indices[-1]

            if siblings_count-1 > last_path_index:
                incr = path_indices.pop()
                incr += 1
                path_indices.append(incr)
                break
            else:
                path_indices.pop()
                if len(path_indices) < 1:
                    found_all = True
                    break

    solutions = []
    length = len(graph)+1
    if start is not end:
        length = len(graph)

    for each in cycles:
        if len(each) == length and each[0] == start and each[-1] == end:
            if start != end and each.index(end) == len(each)-1:
                solutions.append(each)
            elif start == end:
                solutions.append(each)

    print("\nLösungen: \n")
    print(solutions)

    print("\n" + str(len(solutions)) + " Lösung(en) gefunden!")

make_graph()

confirm = input("\nSollen die Baustellen berücksichtigt werden? (j,n)")
if confirm == "j":
    remove_construction()

find_cycles()

