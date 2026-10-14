# ALiCoFSS: Automatic Lift-and-Coast Fuel Saving System

## About the Project
Lift-and-Coast (LiCo) is a driving technique used by skilled racing drivers to save fuel and reduce brake wear by lifting off the throttle early and coasting into a turn. However, average drivers lack the precision to do this safely and consistently. 

**ALiCoFSS** automates this process for everyday drivers. By utilizing GPS, map data, and machine learning, the system predicts the optimal lift-off point before sharp junction turns. It adapts to the specific vehicle's condition, road surface friction, and weather—all tested and validated within the **CARLA** simulation environment.

## How It Works
1. **Sense:** GPS and IMU sensors read the vehicle's position, speed, and real coasting behavior.
2. **Classify:** Map data characterizes the upcoming turn's geometry and current road surface grip.
3. **Decide:** An ML model predicts the exact lift-off point required to reach the safe turn speed without braking.
4. **Act:** The system cuts the throttle to coast, handing control back to the driver instantly if they override it.

## Repository Files
* **`simulation.py`**: The main execution script. Connects to the CARLA server, loads the map (`Town02`), spawns the vehicle on autopilot, and attaches the GNSS sensor.
* **`speed_estimator.py`**: Contains the `GNSSSpeedometer` class. It converts raw GPS coordinates into an accurate vehicle speed (km/h) using a flat-earth equirectangular projection to filter out noise.
* **`Spawn_Car.py`**: A lightweight script to simply test spawning a Citroën C3 at a random map location.
* **Review Presentations**: PowerPoint decks outlining the problem definition, literature survey, and multidisciplinary requirements.

## Running the Simulation
To run this project locally, you must have the [CARLA Simulator](https://carla.readthedocs.io/) installed and running in the background.

1. Start the CARLA server (e.g., run `CarlaUE4.exe`).
2. Install the required Python library:
   ```bash
   pip install carla
