import unittest
from DijkstraAlgorithm import dijkstra_algorithm, route_lines, line_change, calculate_total
from Excel import import_excel_data


class Coursework_testing(unittest.TestCase):

    def test_stations_storage(self):
        """ Test that all the stations has been uploaded to the Doubly Linked List"""
        number_of_stations = 267
        stations = import_excel_data(False)
        self.assertEqual(number_of_stations, stations.length())

    def test_route1(self):
        stations = import_excel_data(False)
        expected_route = ['Warren Street', 'Oxford Circus', 'Piccadilly Circus', 'Charing Cross']
        route = dijkstra_algorithm(stations, 'Warren Street', 'Charing Cross')
        self.assertEqual(expected_route, route)

    def test_route2(self):
        stations = import_excel_data(False)
        expected_route = ['Warwick Avenue', 'Paddington', 'Royal Oak', ]
        route = dijkstra_algorithm(stations, 'Warwick Avenue', 'Royal Oak')
        self.assertEqual(expected_route, route)

    def test_total(self):
        # Testing how to display the total time for each journey
        stations = import_excel_data(False)
        route = dijkstra_algorithm(stations, 'Stanmore',
                                   'Kingsbury')  # Calls dijkstra algorithm to find the fastest route
        lines, minutes = route_lines(stations, route)
        expected_total_list = [0, 5, 9, 11]
        total, total_sum = calculate_total(minutes)
        self.assertEqual(expected_total_list, total)

    def test_lines(self):
        """Testing route for avoiding display of unnecessary changing of lines"""
        expected_lines = ['Circle', 'Circle', 'Circle', 'Circle']
        stations = import_excel_data(True)
        route = dijkstra_algorithm(stations, 'Liverpool Street', 'Farringdon')
        lines_list, minutes = route_lines(stations, route)
        lines, changes = line_change(lines_list)
        self.assertEqual(expected_lines, lines)

    def test_peak_time(self):
        expected_minutes = [1.0, 0.5, 1.0, 1.0, 0.5]
        stations = import_excel_data(True)
        route = dijkstra_algorithm(stations, 'Kilburn Park', 'Marylebone')
        lines_list, minutes = route_lines(stations, route)
        self.assertEqual(expected_minutes, minutes)


if __name__ == "__main__":
    unittest.main()
