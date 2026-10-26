import numpy as np
import time


# mc is a pymycobot arm instance

def calibrate_servos(mc):
    mc = MyArm(port = '/dev/ttyAMA0', baudrate = 115200, timeout = 1.0)

    print("Releasing all servos ...")
    time.sleep(1.0)
    print("NOW!")
    mc.release_all_servos()
    time.sleep(0.5)
    print("Calibation process just started! Adjust all the servos manually to their zero (0) position!")
    wait_for_enter = input("Whenever you are ready press ENTER ... ")
    if wait_for_enter == "":
        print("Calibrating ...")
        for j in range(1, get_joints_num(mc) + 1):
            mc.set_servo_calibration(j)
            time.sleep(0.1)
        mc.send_angles([0,0,0,0,0,0,0], 50)
        blink_leds(mc, 1, 2)
        time.sleep(2)
        print("Calibration process finished successfully!")
        set_leds_color(mc, "#00ff00")
    else:
        print("Calibration process was NOT completed! Try again!")
        set_leds_color(mc, "#ff0000")

def set_leds_color(mc, color = "00ff00", mode = "hex"):
    color = color.lstrip("#")
    if mode == "hex":
        if len(color) != 6:
            raise ValueError("HEX color must have 6 chars (for example '00ff00' for (r, g, b) = (0, 255, 0))!")
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
    elif mode == "rgb":
        if len(color) != 9:
            raise ValueError("RGB color must have 9 chars (for example '255001077' for (r, g, b) = (255, 1, 77))!")
        r = int(color[0:3], 10)
        g = int(color[3:6], 10)
        b = int(color[6:9], 10)
    else:
        r, g, b = (0, 255, 0)
    mc.set_color(r, g, b)

def blink_leds(mc, iter, delay):
    for _ in range(iter):
        set_leds_color(mc, "ff0000")
        time.sleep(delay/3)
        set_leds_color(mc, "0000ff")
        time.sleep(delay/3)
        set_leds_color(mc, "00ff00")
        time.sleep(delay/3)

def get_joints_num(mc):
    angles = mc.get_angles()
    return len(angles)

def send_joints_angles(mc, joints_angles, speed = 30, offset_angles = np.zeros(7,)):
    mc.send_angles((np.array(joints_angles) + np.array(offset_angles)).tolist(), speed)
    while mc.is_moving(): pass

def get_joints_angles(mc):
    return np.array(mc.get_angles())

def get_joints_limits(mc):
    min_angles = []
    max_angles = []
    for i in range(7):
        min_angles.append(mc.get_joint_min_angle(i + 1))
        max_angles.append(mc.get_joint_max_angle(i + 1))
    return min_angles, max_angles
