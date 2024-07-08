"""
Gas Station Refueling example

Covers:

- Resources: Resource
- Resources: Container
- Waiting for other processes

Scenario:
  An airport gas station has a limited number of gas pumps that share a common
  fuel reservoir. Planes randomly arrive at the gas station, request one
  of the fuel pumps and start refueling from that reservoir.

  A gas station control process observes the gas station's fuel level
  and calls a tank truck for refueling if the station's level drops
  below a threshold.

"""
import itertools
import random
import logging
import simpy
import pandas as pd

# Parameters
RANDOM_SEED = 42
STATION_TANK_SIZE = 700000              # Size of the gas station tank (liters)
THRESHOLD = 25                          # Station tank minimum level (% of full)
PLANE_TANK_SIZE = 150000                # Size of plane fuel tanks (liters)
PLANE_TANK_LEVEL = [30000, 100000]      # Min/max levels of plane fuel tanks (liters)
REFUELING_SPEED = 1600                  # Rate of refuelling plane fuel tank (liters / second)
TANK_TRUCK_TIME = 1000                  # Time it takes tank truck to arrive (seconds)
T_INTER = [4000, 8000]                  # Interval between plane arrivals [min, max] (seconds)
SIM_TIME = 1000000                      # Simulation time (seconds)


times = []

def plane(name, env, gas_station, station_tank):
    """A plane arrives at the gas station for refueling.

    It requests one of the gas station's fuel pumps and tries to get the
    desired amount of fuel from it. If the station's fuel tank is
    depleted, the plane has to wait for the tank truck to arrive.

    """
    plane_tank_level = random.randint(*PLANE_TANK_LEVEL)
    logging.debug(f'{env.now:6.1f} s: {name} arrived at gas station')

    start_time = env.now

    with gas_station.request() as req:
        # Request one of the gas pumps
        yield req

        # Get the required amount of fuel
        fuel_required = PLANE_TANK_SIZE - plane_tank_level
        yield station_tank.get(fuel_required)

        # The "actual" refueling process takes some time
        yield env.timeout(fuel_required / REFUELING_SPEED)

        times.append((env.now, env.now - start_time, fuel_required))

        logging.debug(f'{env.now:6.1f} s: {name} refueled with {fuel_required:.1f}L')


def gas_station_control(env, station_tank):
    """Periodically check the level of the gas station tank and call the tank
    truck if the level falls below a threshold."""
    while True:
        if station_tank.level / station_tank.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            logging.debug(f'{env.now:6.1f} s: Calling tank truck')
            # Wait for the tank truck to arrive and refuel the station tank
            yield env.process(tank_truck(env, station_tank))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, station_tank):
    """Arrives at the gas station after a certain delay and refuels it."""
    yield env.timeout(TANK_TRUCK_TIME)
    amount = station_tank.capacity - station_tank.level
    station_tank.put(amount)
    logging.debug(
        f'{env.now:6.1f} s: Tank truck arrived and refuelled station with {amount:.1f}L'
    )

def plane_generator(env, gas_station, station_tank):
    """Generate new planes that arrive at the gas station."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(plane(f'Plane {i}', env, gas_station, station_tank))

# Setup and start the simulation
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
station_tank = simpy.Container(env, STATION_TANK_SIZE, init=STATION_TANK_SIZE)
env.process(gas_station_control(env, station_tank))
env.process(plane_generator(env, gas_station, station_tank))

# Execute!
env.run(until=SIM_TIME)

pd.DataFrame(times, columns=['entry_time', 'duration', 'fuel_litres']).to_csv('sim.csv', index=False)
