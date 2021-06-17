# Here we import any necessary libraries and modules for our program to be able to run
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
from DijkstraAlgorithm import dijkstra_algorithm, route_lines, line_change, calculate_total
from Excel import import_excel_data
from datetime import *
import time
from Hours import hours, off_peak_hours

# Establishing values for the color of tube lines
FONT_COLOUR = '#414b56'
BAKERLOO = '#B26300'
CENTRAL = '#DC241F'
JUBILEE = '#A1A5A7'
HAMCITY = '#F4A9BE'
PICCADILLY = '#0019a8'
CIRCLE = '#FFD329'
DISTRICT = '#007D32'
METROPOLITAN = '#9B0058'
NORTHERN = '#000000'
VICTORIA = '#0098D8'
WATERLOO = '#93CEBA'


# Main GUI

class Main:
    # Configure the main window
    def __init__(self, master):
        self.master = master
        self.master.geometry('800x800')
        self.master.resizable(width=False, height=False)
        self.master.title('London Underground Tube System Route Planner')
        self.master.configure(background="light cyan")

        # Title
        self.headline2 = tk.Label(text='Welcome to the Route Planner', font=("Century Gothic", "35", 'bold'),
                                  fg="light cyan", bg='SkyBlue3', width=100, height=2).place(relx=0.5, rely=0.06,
                                                                                             anchor="center")

        # Instructions for the user (textbox)
        self.welcome_text = tk.Text(height=20, width=42, font=('Century Gothic', '12', 'bold'), fg=FONT_COLOUR,
                                    bg='light blue', bd=4, relief="sunken")
        self.welcome_text.place(relx=0.1, rely=0.19)
        self.welcome_text.insert(tk.END, "\n    To plan a journey, please choose a start time. \n\n\n\n\n   Please "
                                         "choose your starting point. \n\n\n\n\n\n   Please choose your end point. "
                                         "\n\n\n\n\n   If you would like to see the map,\n   please press the \"View "
                                         "Map\" button below.")
        self.timelbl = tk.Label(text="Time departure:", font=("Century Gothic", "14", "italic", "bold"),
                                bg='light cyan', fg=FONT_COLOUR).place(relx='0.6', rely='0.19')
        # Departure hour entry
        self.hours = StringVar(master)
        self.hours.set('Time')
        self.hours_box = ttk.Combobox(self.master, textvariable=self.hours, values=hours).place(relx=0.6,
                                                                                                rely=0.23)
        self.lbl = tk.Label(text='The trains operate from 05:00 until 00:00 (midnight) each day. \n\nTrains run every '
                                 'five minutes with a 1 minute stop at each station to allow passengers to ('
                                 'dis)embark.', font=("Century Gothic", "12", 'bold'), fg="light cyan",
                            bg='SkyBlue3', height=4, width=150).place(relx=0.5, rely=0.95, anchor="center")

        # Start station entry
        self.label_start_station = tk.Label(text="From:", font=("Century Gothic", "14", "italic", 'bold'),
                                            bg='light cyan', fg=FONT_COLOUR).place(relx='0.6', rely='0.3')
        self.start_station = StringVar(master)
        self.start_station.set("Enter Start Station")
        self.cbox_start_station = ttk.Combobox(self.master, textvariable=self.start_station,
                                               values=data_stations.list_nodes()).place(relx=0.6,
                                                                                        rely=0.34)
        # End station entry
        self.label_end_station = tk.Label(text="To:", font=("Century Gothic", "14", "italic", 'bold'),
                                          bg='light cyan', fg=FONT_COLOUR).place(relx=0.6, rely=0.43)
        self.end_station = StringVar(master)
        self.end_station.set("Enter end Station")
        self.cbox_end_station = ttk.Combobox(self.master, textvariable=self.end_station,
                                             values=data_stations.list_nodes()). \
            place(relx=0.6, rely=0.47)
        # Plan journey button
        self.plan_button = tk.Button(text='Plan Journey', font=("Century Gothic", "12", "bold"),
                                     bg="SlateGray3", fg="green4", bd="4", relief="raised",
                                     command=self.planner_window).place(relx=0.7,
                                                                        rely=0.74, anchor='center')
        # Tube map button
        self.map_button = tk.Button(text='View Tube map', font=("Century Gothic", "12", "bold"),
                                    bg="SlateGray3", fg="yellow", bd="4", relief="raised",
                                    command=self.map_window).place(relx=0.26, rely=0.74,
                                                                   anchor='center')
        # Exit button
        self.exit_button = tk.Button(text='Exit', font=("Century Gothic", "12", "bold"),
                                     bg="SlateGray3", fg="red4", bd="4", height=1, command=self.master.destroy). \
            place(relx=0.48, rely=0.82, anchor='center')

    # Command function to open the Tube Map window
    def map_window(self):
        self.list = root.place_slaves()
        for i in self.list:
            i.destroy()

        self.new_window = MapWindow(self.master)

    # Command function to open the planner results window
    def planner_window(self):

        global data_stations
        global off_peak_selected
        correct_entry = 0  # variable to check if correct station has been entered
        for item in data_stations.list_nodes():
            if item == self.start_station.get() or item == self.end_station.get():
                correct_entry = correct_entry + 1

        # Station and time departure validation
        if correct_entry < 2 or self.hours.get() == 'Time':
            tk.messagebox.showerror('Invalid Station', 'You have entered an invalid station name or departure time, '
                                                       'please try again.')
        else:
            for item in off_peak_hours:
                if self.hours.get() == item:
                    off_peak_selected = True

            data_stations = import_excel_data(off_peak_selected)

            self.list = root.place_slaves()
            for i in self.list:
                i.destroy()
            self.new_window = PlannerWindow(self.master, self.start_station.get(), self.end_station.get(),
                                            self.hours.get())


# Results window where the route information is displayed

class PlannerWindow:
    def __init__(self, master, start, end, departure_hour):
        global data_stations
        route = dijkstra_algorithm(data_stations, start, end)  # Calls dijkstra algorithm to find the fastest route
        lines, minutes = route_lines(data_stations, route)
        self.master = master
        self.master.geometry('1200x800')
        self.master.resizable(width=False, height=False)
        self.start = start
        self.end = end
        self.d_hour = departure_hour
        self.master.configure(background="light cyan")
        self.results_table(route, lines, minutes)  # Display results in a table
        # back button
        self.back_button = tk.Button(text='Back', font=("Century Gothic", "12", "bold"),
                                     background="lightsteelblue", fg="goldenrod4", bd="4", height=1,
                                     command=self.go_back). \
            place(relx=0.02, rely=0.02)
        # exit button
        self.exit_button = tk.Button(text='Exit', font=("Century Gothic", "12", "bold"),
                                     background="lightsteelblue", fg="red4", bd="4", height=1,
                                     command=self.master.destroy). \
            pack(side='bottom')

    # Function to return to the main window
    def go_back(self):
        self.list = root.place_slaves() + root.pack_slaves()
        for i in self.list:
            i.destroy()

        global off_peak_selected
        off_peak_selected = False
        self.prev_window = Main(self.master)

    # Function to display results in a table
    def results_table(self, route, lines_list, minutes):
        # Journey Summary:
        self.lbl = tk.Label(text='  Your Journey Summary', font=('Century Gothic', "35", 'bold'), fg='light cyan',
                            bg="SkyBlue3", height=2, width=90).place(relx=0.5, rely=0.06, anchor="center")

        self.journeylbl = tk.Label(text='From {} to {} at {}'.format(route[0], route[-1], self.d_hour),
                                   font=('Century Gothic', 18, "bold", 'underline'),
                                   background="light cyan", width=90, anchor="center").place(relx=0.5, rely=0.17,
                                                                                             anchor="center")

        lines, number_changes = line_change(lines_list)  # number changes = list of stations where a change line is made

        total, total_sum = calculate_total(minutes)

        y = 0.24  # Y Position for widgets
        x = 0.04  # X position for widgets

        prev_station = 0
        # Display summary of the journey for each change of line made
        for item in number_changes:
            self.summary = tk.Label(text=(lines[item] + ':    %s ' % route[prev_station] + 'to ' + route[item]),
                                    font=('Century Gothic', 13, 'bold'),
                                    anchor=NW, fg=self.colour_line(lines[item]),
                                    background="light cyan").place(relx=x, rely=y, anchor=W)
            prev_station = item
            y = y + 0.03
            self.changelbl = tk.Label(text='change', font=('Century Gothic', 10, 'italic'),
                                      anchor=NW, background="light cyan").place(relx=x, rely=y, anchor=W)
            y = y + 0.03

        self.summary = tk.Label(text=(lines[-1] + ':    %s ' % route[prev_station] + 'to ' + route[-1]),
                                font=('Century Gothic', 13, 'bold'),
                                anchor=NW, fg=self.colour_line(lines[-1]), background="light cyan").place(relx=x,
                                                                                                          rely=y,
                                                                                                          anchor=W)
        # Conditional to display the total time in hour:minutes format
        if total_sum < 60:
            self.totallbl = tk.Label(text='Total journey time: {} minutes'.format(total_sum),
                                     font=('Century Gothic', 13, "bold"), anchor='center',
                                     background="light cyan").place(relx=x + 0.1, rely=y + 0.06, anchor=W)

        else:
            self.totallbl = tk.Label(text=('Total journey time %s' % time.strftime("%I:%M",
                                                                                   time.gmtime(
                                                                                       int(total_sum) * 60)) + 'hours'),
                                     font=('Century Gothic', 13, "bold"), anchor='center',
                                     background="light cyan").place(relx=x + 0.11, rely=y + 0.06, anchor=W)

        # Table display of stops information (stop, line, travel time between stops and total travel time) reference:
        # https://stackoverflow.com/questions/47515014/how-do-i-use-tkinter-treeview-to-list-items-in-a-table-of-a
        # -database
        style = ttk.Style()
        style.configure('Treeview', font=('Calibri', 13), background='light cyan')
        style.configure('Treeview.Heading', font=('Helvetica', 15, 'bold'))
        results_table = Treeview(self.master, style='results.Treeview', height=25)

        # Scroll bar for the results table
        self.y_scrollbar = Scrollbar(self.master, orient="vertical", command=results_table.yview)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        results_table.configure(yscrollcommand=self.y_scrollbar.set)
        # Define columns for display results
        results_table['columns'] = ('Station', 'Line', 'Travel Time', 'Total travel time')
        # Configuration of columns and headlines
        results_table.column("Travel Time", width=140)
        results_table.column("Total travel time", width=77)
        results_table['show'] = 'headings'
        results_table.heading('Station', text='Station')
        results_table.heading('Line', text='Line')
        results_table.heading('Travel Time', text='Travel Time')
        results_table.heading('Total travel time', text='Total\nTravel time')

        iid = 0  # Variable that indicates the index position in the Treeview table
        # Insert route data in the table
        for row in route:
            if iid < len(route) - 1:
                results_table.insert('', iid, iid, text='', values=(row, lines[iid], '{} min'.format(minutes[iid]),
                                                                    '{} min'.format(total[iid])), tags=lines[iid])
            else:
                results_table.insert('', iid, iid, text='', values=(row, lines[iid], '', '{} min'.format(total[iid])),
                                     tags=(lines[iid]))
            iid = iid + 1

        # Position of the table of results
        results_table.pack(side=LEFT)
        results_table.place(relx=0.45, rely=0.22, anchor=NW)

        # Change color of table per line (Works on macOS)
        results_table.tag_configure("Bakerloo", foreground=BAKERLOO)
        results_table.tag_configure("Piccadilly", foreground=PICCADILLY)
        results_table.tag_configure("Victoria", foreground=VICTORIA)
        results_table.tag_configure("Circle", foreground=CIRCLE)
        results_table.tag_configure("Central", foreground=CENTRAL)
        results_table.tag_configure("Northern", foreground=NORTHERN)
        results_table.tag_configure("Jubilee", foreground=JUBILEE)
        results_table.tag_configure("Waterloo & City", foreground=WATERLOO)
        results_table.tag_configure("District", foreground=DISTRICT)
        results_table.tag_configure("Hammersmith & City", foreground=HAMCITY)
        results_table.tag_configure("Metropolitan", foreground=METROPOLITAN)

    def colour_line(self, line):
        """ Assign color of line to result in summary
        :param line: line
        :return: Hex color of line entered
        """
        if line == 'Bakerloo':
            colour = BAKERLOO
        elif line == 'Circle':
            colour = CIRCLE
        elif line == 'Metropolitan':
            colour = METROPOLITAN
        elif line == 'Piccadilly':
            colour = PICCADILLY
        elif line == 'Victoria':
            colour = VICTORIA
        elif line == 'Hammersmith & City':
            colour = HAMCITY
        elif line == 'Central':
            colour = CENTRAL
        elif line == 'Jubilee':
            colour = JUBILEE
        elif line == 'Northern':
            colour = NORTHERN
        elif line == 'District':
            colour = DISTRICT
        elif line == 'Waterloo & City':
            colour = WATERLOO
        else:
            colour = 'black'

        return colour


# Tube Map display window
class MapWindow:
    def __init__(self, master):
        self.master = master
        # adjusting window to map
        self.master.geometry('1150x800')
        self.master.resizable(width=False, height=False)

        # labels
        self.headline = tk.Label(text='London Underground Tube System', font=("Century Gothic", "12"), fg='white',
                                 bg="#031580", width=115, anchor='ne').pack(fill='x')
        # map
        self.load_map = Image.open("Tube Map.png")
        self.load_map = self.load_map.resize((1100, 770))
        self.map = ImageTk.PhotoImage(self.load_map)
        self.map_label = tk.Label(image=self.map).place(relx=0.5, rely=0.52, anchor='center')
        # back button
        self.back_button = tk.Button(text='BACK', font=("Century Gothic", "11", "bold"),
                                     bg="lightsteelblue", fg="green4", bd="4", padx=6, pady=3,
                                     command=self.go_back).place(
            relx=0.02, rely=0.005)

    # Go back to main window command
    def go_back(self):
        self.list = root.place_slaves()
        for i in self.list:
            i.destroy()

        self.prev_window = Main(self.master)


# Execution function
if __name__ == '__main__':
    global off_peak_selected  # Variable that indicates if selected hour is off-peak
    off_peak_selected = False  # True when the user selects a peak hour
    root = Tk()
    global data_stations  # Doubly linked list that will store stations data
    data_stations = import_excel_data(off_peak_selected)
    journey_planner = Main(root)
    root.mainloop()
