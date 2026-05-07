"""
ISS Real-Time Tracker
---------------------
Fetches the names of astronauts currently aboard the International
Space Station, saves them to a local text file, and continuously tracks
the station's live position on an interactive world map using Turtle.
"""

import json
import time
import turtle
import urllib.request
import webbrowser

# --- Constants ---
ASTRONAUTS_API = (
    "https://corquaid.github.io/international-space-station-APIs"
    "/JSON/people-in-space.json"
)
ISS_POSITION_API = "http://api.open-notify.org/iss-now.json"
ASTRONAUTS_FILE = "iss.txt"
ASSETS_FOLDER = "assets/"


def get_and_save_astronauts():
    """
    Get ISS crew from API, write the list to a file, and open it.
    
    Queries the people-in-space API, filters for crew members currently
    aboard the ISS (the endpoint also returns people on other missions),
    writes a summary to ASTRONAUTS_FILE, and opens the file with the
    system's default text application.

    Raises
    ------
    Exception
        Network and I/O errors are caught internally and reported to the
        console output. Execution continues normally after the error.
    """
    print("Fetching astronauts on the ISS...")
    try:
        response = urllib.request.urlopen(ASTRONAUTS_API)
        people_in_space = json.loads(response.read())

        # The endpoint includes people on other missions. Keep only ISS crew.
        astronauts_on_iss = [
            p for p in people_in_space["people"] if p.get("iss") is True
        ]

        with open(ASTRONAUTS_FILE, "w") as file:
            file.write(
                f"There are currently {len(astronauts_on_iss)}"
                " astronauts on board the ISS:\n\n"
            )
            for astronaut in astronauts_on_iss:
                file.write(f"{astronaut['name']} - on board\n")
            
        webbrowser.open(ASTRONAUTS_FILE)
    except Exception as error:
        print(f"Error fetching astronauts: {error}")


def setup_world_map():
    """
    Create and configure the Turtle window with the world map and ISS icon.

    Sets up a 1280x700 Turtle screen using real geographic coordinates
    (longitude mapped to the x-axis, latitude to the y-axis), loads the
    world-map background image, and registers the ISS sprite shape.

    Returns
    -------
    iss: turtle.Turtle
        Turtle object with the ISS icon.
    screen: turtle.Screen
        The configured Turtle screen.
    """
    print("Setting up world map...")
    screen = turtle.Screen()
    screen.title("Real-Time ISS Tracker")
    screen.setup(1280, 700)
    # Map screen coordinates to real-world geography:
    # x-axis = longitude (-180, 180), y-axis = latitude (-90, 90)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic(ASSETS_FOLDER + "map.gif")
    screen.register_shape(ASSETS_FOLDER + "iss.gif")

    iss = turtle.Turtle()
    iss.shape(ASSETS_FOLDER + "iss.gif")
    iss.penup()

    return iss, screen


def track_iss(iss):
    """
    Query the ISS position API every 5 seconds and update the sprite location.

    Runs an infinite loop that gets the live position endpoint, extracts
    the current latitude and longitude, and moves the Turtle sprite to the
    corresponding point on the world map. Errors are reported to the console
    output without interrupting the loop.

    Parameters
    ----------
    iss: turtle.Turtle
        The turtle object representing the ISS on the world map.
    """
    print("Starting ISS tracking...")
    while True:
        try:
            response = urllib.request.urlopen(ISS_POSITION_API)
            iss_position_data = json.loads(response.read())

            # "iss_position" is a nested dictionary with "latitude" and "longitude".
            position = iss_position_data["iss_position"]
            lat = float(position["latitude"])
            lon = float(position["longitude"])

            print(f"ISS Position - Latitude: {lat:.4f} | Longitude: {lon:.4f}")
            iss.goto(lon, lat)
        except Exception as error:
            print(f"Error updating ISS position: {error}")

        # 5-second delay prevents overloading the API and reduces idle CPU usage.
        time.sleep(5)


if __name__ == "__main__":
    get_and_save_astronauts()
    iss_turtle, screen = setup_world_map()
    track_iss(iss_turtle)
