# ISS Real-Time Tracker

This project tracks the **International Space Station** in real time, showing its current position on a world map and listing the astronauts on board. It was built as a hands-on Python exercise, focused on API calls and library handling.

## Features

The tracker fetches live ISS coordinates from Open Notify API every five seconds and displays its icon on an animated world map using Python's Turtle graphics. It also queries the People in Space API for the current crew, filtering specifically for ISS astronauts, and saves their names to a text file that opens automatically.

## Technologies

The project was built entirely with Python's standard libraries, using `turtle` to display the world map and animate the ISS icon, `urllib.request` and `json` to handle API calls, and `webbrowser` to open the astronauts list text file.

## How to Run

1. Clone the repository:
```bash
git clone git@github.com/davibarrionuevo/iss-real-time-tracker.git
```
2. Make sure the `assets` folder contains `map.gif` and `iss.gif`
3. Run the project:
```bash
python main.py
```

<img width="1267" height="645" alt="image" src="https://github.com/user-attachments/assets/1630608e-1e81-43fd-84ab-93cfad08e0a2" />
