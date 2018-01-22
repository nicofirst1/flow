"""
Used to test whether sumo lane changing is working as intended
"""
import logging

from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.vehicles import Vehicles
from flow.controllers.routing_controllers import *
from flow.controllers.lane_change_controllers import *
from flow.controllers.car_following_models import *
from flow.core.experiment import SumoExperiment
from flow.scenarios.loop.gen import CircleGenerator
from flow.envs.loop_accel import AccelEnv
from flow.scenarios.loop.loop_scenario import LoopScenario

logging.basicConfig(level=logging.INFO)

sumo_params = SumoParams(sim_step=0.1, sumo_binary="sumo-gui")

vehicles = Vehicles()
vehicles.add(veh_id="idm",
             acceleration_controller=(IDMController, {}),
             routing_controller=(ContinuousRouter, {}),
             num_vehicles=20,
             lane_change_mode="strategic")

env_params = EnvParams(additional_params={"target_velocity": 20})

additional_net_params = {"length": 200, "lanes": 2, "speed_limit": 35,
                         "resolution": 40}
net_params = NetParams(additional_params=additional_net_params)

initial_config = InitialConfig()

scenario = LoopScenario(name="two-lane-one-contr",
                        generator_class=CircleGenerator,
                        vehicles=vehicles,
                        net_params=net_params,
                        initial_config=initial_config)

env = AccelEnv(env_params, sumo_params, scenario)

exp = SumoExperiment(env, scenario)

logging.info("Experiment Set Up complete")

exp.run(2, 1000)

exp.env.terminate()