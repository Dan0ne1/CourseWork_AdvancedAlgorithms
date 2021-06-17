# Data structures classes
# Code based on: https://www.youtube.com/watch?v=8kptHdreaTA&ab_channel=LucidProgramming

class Node:
    """
    Node for Single Linked List
    station = principal station neighbour
    time = distance in minutes between stops
    line = line of the route
    """

    def __init__(self, station, time, line):
        self.station = station
        self.time = time
        self.line = line
        self.next = None


class SingleLinkedList:
    """One Single linked list per Doubly Linked List node"""

    def __init__(self):
        self.head = None

    def appendl(self, station, data, line):
        # Append node
        if self.head is None:
            new_node = Node(station, data, line)
            self.head = new_node
        else:
            new_node = Node(station, data, line)
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.next = None

    def prependl(self, station, data, line):
        # Prepend node
        if self.head is None:
            new_node = Node(station, data, line)
            self.head = new_node
        else:
            new_node = Node(station, data, line)
            new_node.next = self.head
            self.head = new_node

    def print_slist(self):
        # Function to print single linked list
        current = self.head
        while current:
            print('s', current.station, current.time, current.line)  # 's' used as reference for 'stop'
            current = current.next

    def iterate_sl(self):
        # Function to iterate through the single linked list
        current = self.head
        neighbours = []
        while current:
            neighbour = current.station
            time = current.time
            line = current.line
            neighbours.append([neighbour, time, line])
            current = current.next
        return neighbours

    def return_details(self, station):
        # Function to retrieve the details (minutes and line) of the selected neighbour node.
        current = self.head
        while current.next is not None and current.station != station:
            current = current.next
        line = current.line
        minutes = current.time
        return line, minutes


class NodeDll:
    """
        Node for Doubly Linked List
        station_name = principal station
        neighbour_s = Singly linked list with the neighbors of the principal station and its distance
    """

    def __init__(self, station_name):
        self.station = station_name
        self.neighbour_s = SingleLinkedList()
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, station_name):
        # Append Node
        if self.head is None:
            new_node = NodeDll(station_name)
            new_node.prev = None
            self.head = new_node
        else:
            new_node = NodeDll(station_name)
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
            new_node.next = None

    def prepend(self, station_name):
        # Prepend Node
        if self.head is None:
            new_node = NodeDll(station_name)
            new_node.prev = None
            self.head = new_node
        else:
            new_node = NodeDll(station_name)
            self.head.prev = new_node
            new_node.prev = None
            new_node.next = self.head
            self.head = new_node

    def search_node(self, station, neighbour, time, line):
        # Function used to append data to the single linked list of a specific node (station)
        current = self.head
        if current.next is None:
            current.neighbour_s.appendl(neighbour, time, line)
        else:
            # iterates until it finds main station as a node
            while current.next is not None and current.station != station:
                current = current.next
            current.neighbour_s.appendl(neighbour, time, line)

    def print_dlist(self):
        # Print the doubly linked list
        current = self.head
        while current:
            print(current.station)
            current.neighbour_s.print_slist()  # Calls print function of the Single Linked List
            current = current.next

    def iterate(self):
        # Function to iterate through the Doubly Linked list and retrieve the data of each node
        current = self.head
        while current:
            station_name = current.station
            neighbours = current.neighbour_s.iterate_sl()  # Calls iterate function of the Single Linked List
            yield station_name, neighbours
            current = current.next

    def length(self):  # Length of the doubly linked list function
        current = self.head
        length = 0
        while current:
            length = length + 1
            current = current.next
        return length

    def stop_details(self, station, next_station):
        # Function to retrieve the details (minutes and line) between two stops (station, next_station) .
        current = self.head
        while current.station != station:  # Loop to find the same node
            current = current.next
        line, minutes = current.neighbour_s.return_details(next_station)  # Retrieve data of the single linked
        # list's neighbour node
        return line, minutes

    def list_nodes(self):
        # Returns a list of each main node. Used in the program as input for station combobox.
        current = self.head
        stations = []
        while current:
            stations.append(current.station)
            current = current.next
        stations.sort()
        return stations
