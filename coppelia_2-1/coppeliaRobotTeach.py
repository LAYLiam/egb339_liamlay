'''
This script allows you to control the CoppeliaSim robot using sliders.
Simply run it in a terminal using: `python coppeliaRobotTeach.py`
'''

import math
import time

import tkinter as tk
from tkinter import Scale, Button, Label, Text, HORIZONTAL
from coppeliaRobot import CoppeliaRobot


def deg2rad(list_deg):
    return [math.radians(deg) for deg in list_deg]

def rad2deg(list_rad):
    return [math.degrees(rad) for rad in list_rad]


class GUI(object):
    def __init__(self, robot):
        self.robot = robot
        self.root = tk.Tk()
        self.root.title('Dobot Magician controller')
        self.sliders = []
        self.limits = [(-90, 90), (0, 85), (-10, 75), (-90, 90)]  # limits for each slider
        self.theta = deg2rad([0]*3)

        for idx in range(3):
            lbl = Label(self.root, text=f'θ{idx+1}')
            lbl.pack()
            slider = Scale(self.root, from_=self.limits[idx][0], to=self.limits[idx][1], length=600, orient=HORIZONTAL, command=self.joint_change(idx))
            slider.pack()
            self.sliders.append(slider)

        pose_lbl = Label(self.root, text='end effector position')
        pose_lbl.pack()
        self.pose_text = Text(self.root)
        self.pose_text.pack()
        home_btn = Button(self.root, text='Home', command=self.robot.home)
        home_btn.pack()

        # wait till the robot is in position
        time.sleep(2)
        # update sliders with current joint angles
        joint_angles = rad2deg(self.robot.get_joint_config())
        for angle, slider in zip(joint_angles, self.sliders):
            slider.set(angle)

        self.root.after(100, self.update_gui)

    def joint_change(self, idx):
        def slider_update(val):
            self.theta[idx] = float(val)
            theta_rad = deg2rad(self.theta)
            self.robot.move_arm(theta_rad[0], theta_rad[1], theta_rad[2])  # assuming this function takes a list of angles
            self.display_fk()
            # update joint angles on the robot
            theta_rad = deg2rad(self.theta)
            self.robot.move_arm(theta_rad[0], theta_rad[1], theta_rad[2])
        return slider_update

    def display_fk(self):
        # replace with your method of computing FK
        endeffector_pose = self.robot.get_end_effector_pose()
        fk_str = f'x: {endeffector_pose[0]:.3f}, y: {endeffector_pose[1]:.3f}, z: {endeffector_pose[2]:.3f}'
        self.pose_text.delete('1.0', tk.END)
        self.pose_text.insert(tk.END, fk_str)

    def update_gui(self):
        # # update sliders with current joint angles
        # joint_angles = self.robot.get_joint_config()
        # for angle, slider in zip(joint_angles, self.sliders):
        #     slider.set(angle)
        self.root.after(100, self.update_gui)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    gui = GUI(CoppeliaRobot())
    gui.run()
