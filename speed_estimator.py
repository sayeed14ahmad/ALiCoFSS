import math

R_EARTH = 6371000.0  # WGS-84 mean radius in meters

class GNSSSpeedometer:
    def __init__(self, speed_deadband=0.05):
        self.prev_gnss = None
        self.prev_time = None
        self.deadband = speed_deadband  # ignore speeds below 0.05 m/s (~0.18 km/h)

    def update(self, gnss_data):
        """
        gnss_data: carla.GnssMeasurement object from sensor callback
        Returns: speed in m/s (or None on first reading)
        """
        curr_time = gnss_data.timestamp

        if self.prev_gnss is None:
            self.prev_gnss = gnss_data
            self.prev_time = curr_time
            return 0.0

        dt = curr_time - self.prev_time
        if dt <= 0.0:
            return 0.0  # Skip duplicate or non-progressing ticks

        # Equirectangular projection
        lat_mid = math.radians((self.prev_gnss.latitude + gnss_data.latitude) / 2.0)
        d_lat = math.radians(gnss_data.latitude - self.prev_gnss.latitude) * R_EARTH
        d_lon = math.radians(gnss_data.longitude - self.prev_gnss.longitude) * (R_EARTH * math.cos(lat_mid))
        d_alt = gnss_data.altitude - self.prev_gnss.altitude

        distance_3d = math.sqrt(d_lat**2 + d_lon**2 + d_alt**2)
        speed = distance_3d / dt

        # Update historical state
        self.prev_gnss = gnss_data
        self.prev_time = curr_time

        # Filter out static jitter
        if speed < self.deadband:
            return 0.0

        return speed  # Multiply by 3.6 if you need km/h