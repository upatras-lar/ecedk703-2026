from pymycobot.myarm import MyArm
import time
import utils


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
    for j in range(1, utils.get_joints_num(mc) + 1):
        mc.set_servo_calibration(j)
        time.sleep(0.1)
    mc.send_angles([0,0,0,0,0,0,0], 50)
    utils.blink_leds(mc, 1, 2)
    time.sleep(2)
    print("Calibration process finished successfully!")
    utils.set_leds_color(mc, "#00ff00")
else:
    print("Calibration process was NOT completed! Try again!")
    utils.set_leds_color(mc, "#ff0000")
