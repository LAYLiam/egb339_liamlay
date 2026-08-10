"""
This file contains the CoppeliaRobot class, which is a wrapper around the CoppeliaSim API.
There is no need for you to touch or understand this file.
"""

import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

from genericRobotAPI import GenericRobotAPI


class CoppeliaRobot(GenericRobotAPI):
    def __init__(self, host="localhost", port=23000):
        self.host = host
        self.port = port
        self.nDoF = 3
        self.robot_name = "/Dobot"
        self.motor_control_mode = "position"

        print("[CoppeliaRobot] Connecting to remote API server...", end="", flush=True)
        self.client = RemoteAPIClient(host=self.host, port=self.port)
        if self.client is not None:
            print(" Connected")
        else:
            print(" Failed!")
            exit(0)

        print(
            "[CoppeliaRobot] Trying to get sim object... make sure the ZMQ connection is enabled!",
            end="",
            flush=True,
        )
        self.sim = self.client.getObject("sim")
        if self.sim is None:
            print(' Could not get "sim" object; exit')
            exit(0)
        else:
            print(" Got it!")
        # ensure sim is stopped if reconnecting
        self.sim.stopSimulation()
        while self.sim.getSimulationState() != self.sim.simulation_stopped:
            time.sleep(0.01)
        self.robot = self.sim.getObject(self.robot_name)
        if self.robot is None:
            print(f"[CoppeliaRobot] Could not get {self.robot} object")

        # waist, shoulder, elbow
        self.joints = [
            self.sim.getObject(f"/Dobot/motor{idx}") for idx in range(1, self.nDoF + 1)
        ]

        self.end_effector = self.sim.getObject("/Dobot/suctionCup/DummyA")

        self.sim.addLog(
            self.sim.verbosity_scriptinfos, "Python connected to EGB339 Prac Simulator!"
        )

        self.start_sim()

    def move_arm(self, j1: float, j2: float, j3: float):
        if not all(isinstance(x, (int, float)) for x in [j1, j2, j3]):
            raise Exception(
                "[CoppeliaRobot] All parameters for move_arm() must be integers or floats"
            )

        # set robot's joint angles in units of radians
        # theta is the angles: waist, shoulder, elbow
        theta = [j1, j2, j3]

        if self.motor_control_mode != "position":
            # change motor control mode for each joint
            for idx in range(1, self.nDoF + 1):
                self.sim.setObjectInt32Parameter(
                    self.joints[idx], self.sim.jointintparam_ctrl_enabled, 1
                )
            self.motor_control_mode = "position"

        if len(theta) == self.nDoF:
            for i in range(self.nDoF):
                # TODO: need to add some error checking here
                self.sim.setJointTargetPosition(self.joints[i], theta[i])
        else:
            raise ValueError(
                "[CoppeliaRobot] theta not the same size as number of joints"
            )

    def home(self):
        self.move_arm(0, 0, 0)

    def get_joint_config(self) -> list:
        return [self.sim.getJointPosition(joint) for joint in self.joints][0:3]

    def get_end_effector_pose(self):
        # TODO: Double check whether it should be w.r.t. world frame or Dobot frame
        pose = self.sim.getObjectPose(self.end_effector, self.sim.handle_world)
        return pose

    def set_suction_cup(self, signal):
        self.sim.setInt32Signal("/Dobot/suctionCup", int(signal))

    def load_scene(self, scene_path: str):
        # scene_path needs to be full path to scene, scene name is not sufficient
        print(f"[CoppeliaRobot] Loading scene {scene_path}")
        self.sim.loadScene(scene_path)

    def close_scene(self):
        print("[CoppeliaRobot] Closing scene")
        self.sim.closeScene()

    def start_sim(self, sync=False):
        if sync:
            self.client.setStepping(True)
        print("[CoppeliaRobot] Starting simulation")
        self.sim.startSimulation()
        # startSimulation is just a request, wait till it actually started here
        print(self.sim.getSimulationState())
        while (
            self.sim.getSimulationTime() == 0
            or self.sim.getSimulationState() == self.sim.simulation_stopped
        ):
            print("waiting")
            time.sleep(0.01)

    def step_sim(self):
        self.client.step(wait=True)

    def stop_sim(self):
        print("[CoppeliaRobot] Stopping simulation")
        self.sim.stopSimulation()


if __name__ == "__main__":
    dobot = CoppeliaRobot()
    curr_angles = dobot.get_joint_config()
    print(curr_angles)
    target_angles = curr_angles.copy()
    target_angles[0] = 0.4
    while (t := dobot.sim.getSimulationTime()) < 3:
        s = f"[CoppeliaRobot] Simulation time: {t:.2f} [s]"
        print(s)
        dobot.client.step()

        dobot.move_arm(target_angles[0], target_angles[1], target_angles[2])
        print(dobot.get_joint_config())
    dobot.stop_sim()
    print("[CoppeliaRobot] Bye!")
