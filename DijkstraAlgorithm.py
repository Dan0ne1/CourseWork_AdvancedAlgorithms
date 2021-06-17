# Dijkstra algorithm and retrieve route's data functions
# Code based on: https://www.youtube.com/watch?v=IG1QioWSXRI&ab_channel=IanSullivan
def dijkstra_algorithm(data, start, end):
    graph = {}  # Dictionary that contains the nodes of the graph as key value pairs

    # Upload data from the doubly linked list to the graph as graph[node]=[node's data]
    for node in data.iterate():
        graph[node[0]] = node[1]

    total_costs = {}  # List that contains total cost of each node (from start point)
    previous_node = {}  # List that contains previous node of each station to form a path
    unvisited_nodes = graph  # Ensures every node will be visited
    infinity = float('inf')
    path = []

    for node in unvisited_nodes:
        total_costs[node] = infinity  # Node's start cost will be infinity until a lower cost has been found
    total_costs[start] = 0  # Except for start node

    while unvisited_nodes:
        minNode = None  # Selected Node
        for node in unvisited_nodes:  # Finds the node with the lowest cost
            if minNode is None:
                minNode = node
            elif total_costs[node] < total_costs[minNode]:
                minNode = node

        for i in graph[minNode]:
            temp = i
            neighbour = temp[0]  # Neighbour of the selected node
            cost = temp[1]  # Cost of the neighbour node
            if cost + total_costs[minNode] < total_costs[neighbour]:
                # Updates total cost of each node only if is lower than its current total cost
                total_costs[neighbour] = cost + total_costs[minNode]
                # Saves the selected node as predecessor of the neighbour node
                previous_node[neighbour] = minNode

        del unvisited_nodes[minNode]  # Deletes last visited node

    current_node = end
    # Find the path from the end point to start point
    while current_node != start:
        path.insert(0, current_node)
        current_node = previous_node[current_node]
    path.insert(0, current_node)

    return path


def route_lines(data_stations, route):
    """
    Get data from the selected route (line and minutes between two stops)
    :param data_stations: where the data is located (doubly linked list)
    :param route: route list from dijkstra algorithm
    :return: a list containing the lines and minutes of each stop in order
    """
    lines = []  # line of each station in route list
    minutes = []  # minutes to next stop
    line = ""
    for index in range(len(route)):  # index in route list
        if index == len(route) - 1:  # line is not referenced first as this will always be the last case
            lines.append(line)
        elif index < len(route):
            line, minute = data_stations.stop_details(route[index], route[index + 1])
            lines.append(line)
            minutes.append(minute)
    return lines, minutes


def line_change(lines):
    """
    Function to save in which stop a change of line is made (displaying purposes)
    :param lines:
    :return: a list of lines of the route and list of indexes where the changes are made
    """
    change_line = lines[0]  # variable that keeps track of the current line
    changes_index = []  # list that indicates the indexes in lines list where a change of line is made
    for index in range(len(lines)):
        if lines[index] != change_line:  # if a change of line is made
            lines[index], change_line = change_line, lines[index]  # update values
            changes_index.append(index)  # add current index to the list
    return lines, changes_index


def calculate_total(minutes):
    total = [0, ]  # list of total time at each stop
    total_sum = 0  # final total time

    # Count the total time for each station
    for i in range(len(minutes) - 1):
        total_sum = minutes[i] + 1 + total_sum  # Update total sum
        total.append(total_sum)

    total_sum = total_sum + minutes[-1]
    total.append(total_sum)

    return total, total_sum
