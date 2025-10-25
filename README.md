# Traffic-CSV-Analyzer
A Python project that reads traffic CSV files, processes vehicle data, and displays hourly histograms using Tkinter. Users input survey dates in the terminal, and the program calculates vehicle statistics and visualizes hourly traffic patterns.

## Features

- Input validation for survey date (day, month, year)  
- Process multiple CSV files in a loop  
- Calculates:
  - Total vehicles, trucks, electric vehicles, two-wheeled vehicles  
  - Busses going North, straight-going vehicles  
  - Vehicles over the speed limit  
  - Percentages and averages  
- Displays hourly traffic histogram for two junctions:
  - Elm Avenue / Rabbit Road  
  - Hanley Highway / Westway  
- Saves results to `results.txt` for record-keeping  

## CSV File Format

Your CSV files should have the following columns:

| Column Name           | Description                           |
|-----------------------|---------------------------------------|
| JunctionName          | Name of the junction                  |
| timeOfDay             | Time in HH:MM format                  |
| VehicleType           | Car, Truck, Bus, Bicycle, Scooter…    |
| elctricHybrid         | True/False for electric/hybrid cars   |
| TurnLeft              | True/False                            |
| TurnRight             | True/False                            |
| VehicleSpeed          | Vehicle speed at the junction         |
| JunctionSpeedLimit    | Speed limit at the junction           |
| Weather_Conditions    | Light Rain, Heavy Rain, Clear…        |
| Direction             | North, South, East, West              |

> **Tip:** Include 1–2 small example CSV files for testing (already included). Avoid uploading large datasets.

## How to Run

1. Make sure Python 3.x is installed on your system. Tkinter is usually included with Python.  
2. Place your CSV files in the `data/` folder (already included).  
3. Run the Python script:

```bash
python TrafficAnalyzer.py
