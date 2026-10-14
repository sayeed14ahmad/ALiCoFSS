import carla
import random

client = carla.Client('localhost', 2000)
world = client.get_world()

client.load_world('Town02')
spawn_points = world.get_map().get_spawn_points()
blueprint_library = world.get_blueprint_library()
car = blueprint_library.find('vehicle.citroen.c3')
citroen = world.spawn_actor(car, random.choice(spawn_points))