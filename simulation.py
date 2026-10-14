import carla
import time
from speed_estimator import GNSSSpeedometer

def main():
    actor_list = []

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        # 1. Load world and capture the NEW world instance
        world = client.load_world('Town02')

        # 2. Setup Spectator and Vehicle
        blueprint_library = world.get_blueprint_library()
        citroen_bp = blueprint_library.find('vehicle.citroen.c3')
        citroen_bp.set_attribute('role_name', 'c3')

        # Elevation z is set high enough so the tires don't clip into the road
        spawn_transform = carla.Transform(
            carla.Location(x=166.256805, y=302.498657, z=2.0),
            carla.Rotation(pitch=-7.594385, yaw=175.603058, roll=0.000050)
        )
        citroen = world.spawn_actor(citroen_bp, spawn_transform)
        actor_list.append(citroen)

        # 3. Setup GNSS Sensor
        gnss_bp = blueprint_library.find('sensor.other.gnss')
        gnss_bp.set_attribute('sensor_tick', '0.1')
        sensor_transform = carla.Transform(carla.Location(x=0.0, z=1.5))
        gnss = world.spawn_actor(gnss_bp, sensor_transform, attach_to=citroen)
        actor_list.append(gnss)

        speedometer = GNSSSpeedometer()

        def gnss_callback(data):
            speed_mps = speedometer.update(data)
            speed_kmh = speed_mps * 3.6

            # Query vehicle control inputs
            ctrl = citroen.get_control()

            print(
                f"Speed: {speed_kmh:5.1f} km/h | "
                f"Throttle: {ctrl.throttle:.2f} | "
                f"Brake: {ctrl.brake:.2f} | "
                f"Steer: {ctrl.steer:+.2f} | "
                f"Gear: {ctrl.gear}"
                )

        gnss.listen(gnss_callback)

        # 4. Traffic Manager & Autopilot
        traffic_manager = client.get_trafficmanager(8000)
        traffic_manager.ignore_lights_percentage(citroen, 100.0)
        traffic_manager.ignore_signs_percentage(citroen, 100.0)
        citroen.set_autopilot(True, 8000)

        print("Vehicle running on autopilot. Press Ctrl+C to stop.")

        # 5. Keep the main thread alive!
        while True:
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nStopping simulation...")

    finally:
        # 6. Always clean up actors
        print("Cleaning up spawned actors...")
        for actor in actor_list:
            if actor.is_alive:
                actor.destroy()
        print("Done.")

if __name__ == '__main__':
    main()