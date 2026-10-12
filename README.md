# Introduction to Robotics – ROS2 Labs

Lab material for the **Introduction to Robotics** course, Department of Electrical and Computer Engineering, University of Patras. Over five labs, students go from their first ROS2 node to controlling a real robotic arm.

The labs use **ROS2** (Python, `rclpy`) with RViz2/RQT, the MuJoCo physics simulator, and real hardware: an Elephant Robotics **myArm 300 Pi** (7-DOF arm with a Raspberry Pi 4), a Logitech C270 USB camera and an RPLIDAR A1M8.

## Labs

Each lab folder contains a `Handout.md` (the step-by-step guide students follow), the code or workspaces it uses, and a LaTeX Beamer deck with the slides.

| Lab | Topic | What students do | Folder |
|---|---|---|---|
| **1** | **Introduction to ROS2** | Theory of workspaces, packages, nodes, interfaces, parameters and launch files. Build the *Luna* rover project from scratch, then make a real LED blink and react to a button on the Raspberry Pi. | [lab1/](lab1/) |
| **2** | **RViz2 & Visualization Tools** | RViz2, RQT plugins, URDF modeling, TF and `robot_state_publisher`. Visualize a double pendulum and the myArm 300 Pi. | [lab2/](lab2/) |
| **3** | **Sensor Data Visualization** | Camera model and calibration, ArUco pose estimation, LIDAR scanning, `visualization_msgs/Marker` in RViz2. | [lab3/](lab3/) |
| **4** | **MuJoCo Simulation & Control** | Gazebo vs MuJoCo; velocity (Jacobian pseudoinverse) and torque control of a KUKA LBR iiwa 14 tracking circles and Lissajous curves. | [lab4/](lab4/) |
| **5** | **All-In-One: LIDAR Obstacle Following** | Full perception-to-action pipeline: LIDAR obstacle detection, TF2 frames, inverse kinematics and control of the real myArm. | [lab5/](lab5/) |

Labs build on each other, so they are meant to be done in order. `labs_reports/` holds the homework reports from the previous edition.

## Requirements

- **Ubuntu** with a matching **ROS2** distribution (the material was developed with **Jazzy** on Ubuntu 24.04) and `colcon`.
- **Python 3**; Lab 4 also needs `mujoco`, Lab 1 uses `RPi.GPIO` on the Raspberry Pi.
- Labs 1, 3 and 5 need the hardware listed above.

## Working with the ROS2 workspaces

Every lab with code uses a standard ROS2 workspace (`*_workspace/` or `*_ws/`). From inside one:

```bash
source /opt/ros/<distro>/setup.bash
colcon build
source install/setup.bash        # re-source after every build
```

`build/`, `install/` and `log/` are generated and git-ignored. The handouts show the code in full and mark the parts students write as *Student TODO*; the code in the repo is the complete solution.

## Slides

The slides are LaTeX Beamer decks and are not pre-built. To build one:

```bash
cd lab1/ros2_basics_slides
latexmk -pdf ros2_basics_intro.tex
```

## Resources

See [usefull_resources.md](usefull_resources.md) for documentation, tutorials and datasheets used across the labs.

## Authors

Konstantinos Asimakopoulos (k_asimakopoulos@ac.upatras.gr) and Lampros Printzios (printzios_lampros@ac.upatras.gr).
