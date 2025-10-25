# Author: H.A.K Senadhi Mandina
# Date: 12/24/2024
# Student ID: 20232534 / w2120613

import csv
import os
import tkinter as tk

# Task A: Input Validation
def validate_date_input(prompt, lower, upper):
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    while True:
        try:
            number = int(input(prompt))
            if lower <= number <= upper:
                return number
            else:
                print(f"Out of range - values must be in the range {lower} and {upper}.")
        except ValueError:
            print("Integer required")

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        choice = input("Do you wish to load a new dataset? (Y/N): ").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        print("Please enter 'Y' to continue or 'N' to exit.")

# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    total_two_wheeled = 0
    total_bicycles = 0
    total_busses_north = 0  
    total_straight_vehicles = 0  
    vehicles_over_speed_limit = 0
    elm_rabbit_avenue_vehicles = 0
    hanley_westway_highway_vehicles = 0
    elm_rabbit_avenue_scooters = 0
    rain_hours_set = set()
    hourly_traffic = {"Elm Avenue/Rabbit Road": [0] * 24, "Hanley Highway/Westway": [0] * 24}

    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            total_vehicles += 1
            junction = row.get('JunctionName', '')
            time_of_day = row.get('timeOfDay', '')
            try:
                hour = int(time_of_day.split(':')[0]) if time_of_day else 0
            except ValueError:
                hour = 0  
            if row.get('VehicleType') == 'Truck':
                total_trucks += 1
            if row.get('elctricHybrid') == 'True':
                total_electric_vehicles += 1
            if row.get('VehicleType') in ['Bicycle', 'Motorcycle', 'Scooter']:
                total_two_wheeled += 1
            if row.get('VehicleType') == 'Bicycle':
                total_bicycles += 1
            if row.get('VehicleType') == 'Bus' and row.get('Direction') == 'North':
                total_busses_north += 1
            if row.get('TurnLeft') == 'False' and row.get('TurnRight') == 'False':
                total_straight_vehicles += 1
            try:
                vehicle_speed = int(row.get('VehicleSpeed', 0)) if row.get('VehicleSpeed') else 0
                junction_speed_limit = int(row.get('JunctionSpeedLimit', 0)) if row.get('JunctionSpeedLimit') else 0
                if vehicle_speed > junction_speed_limit:
                    vehicles_over_speed_limit += 1
            except ValueError:
                pass
            if junction == 'Elm Avenue/Rabbit Road':
                elm_rabbit_avenue_vehicles += 1
                hourly_traffic["Elm Avenue/Rabbit Road"][hour] += 1
                if row.get('VehicleType') == 'Scooter':
                    elm_rabbit_avenue_scooters += 1
            if junction == 'Hanley Highway/Westway':
                hanley_westway_highway_vehicles += 1
                hourly_traffic["Hanley Highway/Westway"][hour] += 1
            if row.get('Weather_Conditions') in ['Light Rain', 'Heavy Rain']:
                rain_hours_set.add(hour)

        # Calculate percentages and averages
        truck_percentage = round((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0
        avg_bicycles_per_hour = round(total_bicycles / 24) if total_bicycles > 0 else 0
        elm_rabbit_avenue_scooter_percentage = round((elm_rabbit_avenue_scooters / elm_rabbit_avenue_vehicles) * 100) if elm_rabbit_avenue_vehicles > 0 else 0
        busiest_hour_count = max(hourly_traffic["Hanley Highway/Westway"], default=0)
        busiest_hour = hourly_traffic["Hanley Highway/Westway"].index(busiest_hour_count) if busiest_hour_count > 0 else None

        return {
            "total_vehicles": total_vehicles,
            "total_trucks": total_trucks,
            "total_electric_vehicles": total_electric_vehicles,
            "total_two_wheeled": total_two_wheeled,
            "total_bicycles": total_bicycles,
            "total_busses_north": total_busses_north,
            "total_straight_vehicles": total_straight_vehicles,
            "vehicles_over_speed_limit": vehicles_over_speed_limit,
            "truck_percentage": truck_percentage,
            "avg_bicycles_per_hour": avg_bicycles_per_hour,
            "elm_rabbit_avenue_vehicles": elm_rabbit_avenue_vehicles,
            "hanley_westway_highway_vehicles": hanley_westway_highway_vehicles,
            "elm_rabbit_avenue_scooter_percentage": elm_rabbit_avenue_scooter_percentage,
            "busiest_hour": f"{busiest_hour:02}" if busiest_hour is not None else "N/A",
            "busiest_hour_count": busiest_hour_count,
            "rain_hours": len(rain_hours_set),
            "hourly_traffic": hourly_traffic,
        }

def display_outcomes(outcomes, file_name):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    result = (
        f"\n*****************************************\n"
        f"data file selected is {file_name}\n"
        f"\n"
        f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}\n"
        f"The total number of trucks recorded for this date is {outcomes['total_trucks']}\n"
        f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}\n"
        f"The total number of two-wheeled vehicles for this date is {outcomes['total_two_wheeled']}\n"
        f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['total_busses_north']}\n"
        f"The total number of Vehicles through both junctions not turning left or right is {outcomes['total_straight_vehicles']}\n"
        f"The percentage of total vehicles recorded that are trucks for this date is {int(outcomes['truck_percentage'])}%\n"
        f"the average number of Bikes per hour for this date is {outcomes['avg_bicycles_per_hour']}\n"
        f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['vehicles_over_speed_limit']}\n"
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['elm_rabbit_avenue_vehicles']}\n"
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['hanley_westway_highway_vehicles']}\n"
        f"{int(outcomes['elm_rabbit_avenue_scooter_percentage'])}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n"
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['busiest_hour_count']}\n"
        f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes['busiest_hour']}:00 and {int(outcomes['busiest_hour']) + 1}:00\n"
        f"The number of hours of rain for this date is {outcomes['rain_hours']}\n"
        f"\n*****************************************\n"
    )
    print(result)
    return result

# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    result = display_outcomes(outcomes, file_name)  
    with open(file_name, "a") as file:
        file.write(result)
   
# Task D: Histogram Display
canvas_width = 1400
canvas_height = 450
bar_width = 20  
bar_spacing = 13
edge_padding = 80

class HistogramApp:
    
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing 

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title("Histogram")
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        self.canvas.create_line(edge_padding, canvas_height - edge_padding, canvas_width - edge_padding, canvas_height - edge_padding, width=1)
        self.canvas.create_text(canvas_width // 2, canvas_height - edge_padding // 2, text="Hours 00.00 to 24:00",font=("Arial Narrow", 10), fill="black")
        combined_data = self.traffic_data["Elm Avenue/Rabbit Road"] + self.traffic_data["Hanley Highway/Westway"]
        max_value = max(combined_data, default=1)
        scale = (canvas_height - 2 * edge_padding) / max_value
        
        for i in range(24):
            x_green = edge_padding + i * (bar_width * 2 + bar_spacing)
            x_red = x_green + bar_width
            y_green = canvas_height - edge_padding - self.traffic_data["Elm Avenue/Rabbit Road"][i] * scale
            y_red = canvas_height - edge_padding - self.traffic_data["Hanley Highway/Westway"][i] * scale

            self.canvas.create_rectangle(x_green, y_green, x_green + bar_width, canvas_height - edge_padding,fill="lightgreen", outline="green")
            self.canvas.create_text(x_green + bar_width / 2, y_green - 10,text=str(self.traffic_data["Elm Avenue/Rabbit Road"][i]),font=("Arial", 8), fill="green")
            self.canvas.create_rectangle(x_red, y_red, x_red + bar_width, canvas_height - edge_padding,fill="salmon", outline="red")
            self.canvas.create_text(x_red + bar_width / 2, y_red - 10,text=str(self.traffic_data["Hanley Highway/Westway"][i]),font=("Arial", 8), fill="red")
            self.canvas.create_text(x_green + bar_width, canvas_height - edge_padding + 15,text=f"{i:02d}", font=("Arial", 10), fill="black")
        self.add_legend()

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        self.canvas.create_rectangle(20, 60, 40, 40, fill="lightgreen", outline="black")
        self.canvas.create_text(60, 50, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10), fill="black")
        self.canvas.create_rectangle(20, 100, 40, 80, fill="salmon", outline="black")
        self.canvas.create_text(60, 90, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10), fill="black")
        self.canvas.create_text(20, 20, text=f"Histogram of vehicle frequency per hour ({self.date})",font=("Arial Narrow", 14), fill="black", anchor="w")

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()

# Task E: MultiCSVProcessor fixes
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path, day, month, year):
        """
        Loads a CSV file and processes its data.
        """
        outcomes = process_csv_data(file_path)
        hourly_traffic = outcomes['hourly_traffic']  
        date = f"{day:02}/{month:02}/{year}"
        app = HistogramApp(hourly_traffic, date)
        app.setup_window()
        app.draw_histogram()
        app.root.mainloop()

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        # Prompt user for the day, month, and year to construct the file name
        day = validate_date_input("Please enter the day of the survey in the format dd:", 1, 31)
        month = validate_date_input("Please enter the month of the survey in the format MM:", 1, 12)
        year = validate_date_input("Please enter the year of the survey in the format YYYY:", 2000, 2024)
        file_name = f"traffic_data{str(day).zfill(2)}{str(month).zfill(2)}{year}.csv"

        # Check if file exists and process
        if os.path.exists(file_name):
            outcomes = process_csv_data(file_name)
            if outcomes:
                save_results_to_file(outcomes)
                self.load_csv_file(file_name, day, month, year)
        else:
            print(f"The file '{file_name}' was not found.")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            self.handle_user_interaction()
            if not validate_continue_input():
                print("Exiting the program.")
                break
                    
multi_csv_processor = MultiCSVProcessor()
multi_csv_processor.process_files()
