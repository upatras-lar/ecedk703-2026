# ROS2 Laboratory 2 - Visualization Tools and Robot Description

In the previous lab, we learned about building ROS2 packages from scratch, including nodes, topics, services, parameters, and launch files. In this third lab we'll explore the visualization side of ROS2, learning how to describe robots visually and display them in 3D environments. We will work with URDF files, RViz2, and RQT tools to visualize and debug robotic systems.

We will explain these visualization concepts by working with two different systems: a double pendulum system and the myArm 300 Pi robotic arm. This means that the time we have for this lab will be split in two; you will spend half of the time working with the pendulum and the other half working with the arm.

## The Double Pendulum

Our first visualization subject is a **double pendulum**, a classic physics system consisting of two connected pendulums. This system is perfect for learning visualization because:

- It has multiple joints that move in real-time
- It demonstrates the relationship between joint states and visual representation
- It's simple enough to understand but complex enough to be interesting

### Understanding URDF Files

Before we can visualize anything, we need to describe our robot. We do this by using **URDF** files. **URDF** (Unified Robot Description Format) is an XML format that specifies the physical properties of a robot. A URDF file contains:

- **Links** - The rigid bodies of the robot (like the pendulum rods)
- **Joints** - The connections between links (how they can move relative to each other)
- **Visual elements** - How the robot looks (colors, shapes, meshes)
- **Collision elements** - How the robot interacts physically with the world
- **Inertial properties** - Mass and inertia characteristics

Let's examine the double pendulum URDF! We first need to enter our double pendulum workspace and then use the `cat` command to view the urdf file on the command line:

```bash
cd pendulum_workspace
cat src/pendu_control_pkg/urdf/double_pendulum.urdf
```

> **Student TODO**: Look at the URDF file structure. Can you identify the links and joints? What type of joints are used?

### Creating the Double Pendulum Node

We are now going to create a node for our double pendulum. The design we are trying to implement is a bit different than the ones we are used to from the previous labs. We will have one `publisher` that publishes the current state (position & velocity) of the double pendulum in the topic `/joint_states`. This is where Rviz will be listening (through the pre-built `robot_state_publisher`). This means that we will see a live visualization of our pendulum:

`double_pendulum_node` ===> `robot_state_publisher_node` ===> `Rviz`

> **Important!** The `robot_state_publisher` is a generic, pre-built node that listens to the `/joint_states` topic to read the state of the robot that we are publishing from our own custom node (in this case `double_pendulum_node`), and then publishes it to the `/tf` topic; which is the one that Rviz is listening to.

We also want to be able to control the double pendulum. We know that the double pendulum has four equilibrium points. We can create a `subscriber` that will listen to a topic called `/equilibrium`. Then, depending on the number that it received, it will try to reach that specific equilibrium point.

With this design in mind, let's write our `double_pendulum_node`:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32
import pyCandle
import sys
import math


class DoublePendulumNode(Node):
    def __init__(self):
        super().__init__("double_pendulum_node")
        
        # Initialize the double pendulum
        candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True, pyCandle.USB)

        # Check if motors are available
        motor_ids = candle.ping(pyCandle.CAN_BAUD_1M)
        self.get_logger().info(f"Motor ids: {motor_ids}")
        if len(motor_ids) == 0: sys.exit("EXIT FAILURE")

        # Add all found motor drives to the update list
        for id in motor_ids:  
            candle.addMd80(id)

        # Reset all encoders at 0 and enable the motor drives
        for id in motor_ids:
            candle.controlMd80SetEncoderZero(id)
            candle.controlMd80Mode(id, pyCandle.IMPEDANCE)
            candle.controlMd80Enable(id, True)
        
        # Begin auto-update loop for the data in candle.md80s vector
        candle.begin()

        self.shoulder_motor = candle.md80s[1]
        self.elbow_motor = candle.md80s[0]

        # Set the PD Controller gains for each motor
        self.shoulder_motor.setImpedanceControllerParams(0.2, 0.02)
        self.elbow_motor.setImpedanceControllerParams(0.2, 0.02)

        # Create publisher for the joint states (position and velocity)
        ############ ENTER CODE HERE ###############


        ############################################

        # Create subscription for the equilibrium point
        ############ ENTER CODE HERE ###############


        ############################################

    def timer_callback(self) -> None:
        """
        This function is periodically called by the timer. It publishes the current state (position and velocity)
        of the pendulum to the /joint_states topic.
        """

        # Create the message with the time stamp
        state_msg = JointState()
        state_msg.header.stamp = self.get_clock().now().to_msg()

        # Set the joint names (joint1: shoulder joint, joint2: elbow joint)
        state_msg.name = ["joint1", "joint2"]

        # Set the joint positions
        state_msg.position = [float(self.shoulder_motor.getPosition()), float(self.elbow_motor.getPosition())]

        # Set the velocity positions
        ############ ENTER CODE HERE ###############


        ############################################

        # Publish the message
        self.state_publisher.publish(state_msg)

        # Print the current position and velocity of the joints
        self.get_logger().info(f"{state_msg.name[0]}: Position {state_msg.position[0]}, Velocity: {state_msg.velocity[0]} \n{state_msg.name[1]}: Position {state_msg.position[1]}, Velocity: {state_msg.velocity[1]}")

    def subscriber_callback(self, msg: Int32) -> None:
        """
        This function is called by the control subscriber. Whenever it receives a command message, it uses the controllers to reach
        the desired equilibrium position.

        Equilibrium Point 1 --> shoulder = 0 rad, elbow = 0 rad
        Equilibrium Point 2 --> shoulder = 0 rad, elbow = pi rad
        Equilibrium Point 3 --> shoulder = pi rad, elbow = pi rad
        Equilibrium Point 4 --> shoulder = pi rad, elbow = 0 rad
        """

        # Read the command message
        equilibrium_point = msg.data

        # Give the appropriate motor command (depending on the message)
        if equilibrium_point == 1:
            self.shoulder_motor.setTargetPosition(0.0)
            self.elbow_motor.setTargetPosition(0.0)
        elif equilibrium_point == 2:
        ############ ENTER CODE HERE (delete pass) ################
            pass

        ###########################################################
        elif equilibrium_point == 3:
        ############ ENTER CODE HERE  (delete pass) ###############
            pass

        ##########################################################
        elif equilibrium_point == 4:
        ############ ENTER CODE HERE (delete pass) ###############
            pass

        ##########################################################
        else:
            pass

def main(args = None):
    try:
        rclpy.init(args = args)
        node = DoublePendulumNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
```

> **Student TODO I**: Create a publisher that uses a timer to publish `JointState` messages every 0.01 seconds on the `/joint_states` topic.

> **Student TODO II**: Create a subscriber that listens to the `/equilibrium` topic. Whenever a message arrives, it calls the `subscriber_callback` function.

> **Student TODO III**: The `timer_callback` function publishes the state of the pendulum (aka the position and velocity of the joints). We can see how we use the `getPosition()` method on the motors to get their position. Let's do the same for the velocities with the `getVelocity()` method.

> **Student TODO IV**: The subscriber listens to the `/equilibrium` topic. This is basically `int` type message. We match `int` type commands to different equilibrium points of the pendulum. Complete the `if - elif - else` statement for the rest of the equilibrium points according to the guide in the comments of the function.

### The Robot State Publisher

As we mentioned before, the `robot_state_publisher` node is a crucial component that bridges the gap between our URDF file and visual representation. It:

1. Loads the URDF file from the `robot_description` parameter
2. Listens to `/joint_states` topic for current joint positions
3. Publishes the complete robot state to the `/tf` and `/tf_static` topics
4. Makes the robot's current configuration available to visualization tools

### Creating the Double Pendulum Launch File

Let's write a launch file to start all the necessary nodes for double pendulum visualization:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = FindPackageShare("pendu_control_pkg").find("pendu_control_pkg")

    urdf_file = PathJoinSubstitution([pkg_share, "urdf", "double_pendulum.urdf"])
    rviz_config_file = PathJoinSubstitution([pkg_share, "config", "display_double_pendulum.rviz"])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": ParameterValue(Command(["cat ", urdf_file]), value_type=str)
            }],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_file],
            output="screen",
        ),
        ############ ENTER CODE HERE ###############


        ############################################
    ])
```

> **Student TODO**: In order to be able to visualize our pendulum correclty, we need to launch three nodes: the `rviz2` (which launches rviz), `robot_state_publisher` (to bridge our node with rviz) and of course our own node. Add our `double_pendulum_node` in the `LaunchDescription` section like we did in the previous lab.

### Launch the Double Pendulum Visualization

We are ready to launch everything and see our double pendulum! As we have learned, we need to `build` and `source` first:

```bash
colcon build
source install/setup.bash
```

and now we can launch:

```bash
ros2 launch pendu_control_pkg pendulum_launch.py
```

**Remember!** This launch file starts several nodes:

- `robot_state_publisher` - Processes the URDF and joint states
- `rviz2` - The 3D visualization tool
- `double_pendulum_node` - The actual pendulum controller (our node)

---

### Exploring RViz2

**RViz2** (ROS Visualization) is the primary 3D visualization tool in ROS2. When you launch the double pendulum, you should see:

1. **3D View Panel** - Shows the robot model in 3D space
2. **Displays Panel** - Lists all active visualization elements
3. **Tools Panel** - Contains interaction tools (camera controls, etc.)
4. **Views Panel** - Different camera perspectives

Key display types you'll see:

- **RobotModel** - Renders the URDF model
- **TF** - Shows the coordinate frame tree
- **JointState** - Visualizes joint positions (if enabled)

### What is being published?

The double pendulum node publishes joint states on the `/joint_states` topic. Let's check what's being published (in another terminal of course):

```bash
ros2 topic echo /joint_states
```

You should see messages containing:

- `header.stamp` - Timestamp of the measurement
- `name` - List of joint names (["joint1", "joint2"])
- `position` - Current joint angles in radians
- `velocity` - Current joint angular velocities

The pre-built `robot_state_publisher` that we used, subscribes to this topic and updates the robot's visual representation accordingly.

### Controlling the Double Pendulum

The double pendulum node listens to equilibrium point commands on the `/equilibrium` topic. If you remember, we have four equilibrium points. This means that the equilibrium point commands are basically `Int32` messages. So we could create a publisher on a different node that publishes `Int32` commands on the `/equilibrium` topic.

For the sake of brevity, we will not do that. We are going to use the CLI `ros2 topic pub` command to directly publish the command that we want from another terminal. Then our `double_pendulum_node` will see it and execute it. And because the state of the pedulum's joints are periodically being published to the `joint_states` topic, we should see the pedulum move both in the real world and Rviz.

```bash
# Send equilibrium point 1 (both joints at 0 rad)
ros2 topic pub /equilibrium std_msgs/msg/Int32 "data: 1"

# Send equilibrium point 2 (joint1 at 0 rad, joint2 at π rad)
ros2 topic pub /equilibrium std_msgs/msg/Int32 "data: 2"

# Send equilibrium point 3 (both joints at π rad)
ros2 topic pub /equilibrium std_msgs/msg/Int32 "data: 3"

# Send equilibrium point 4 (joint1 at π rad, joint2 at 0 rad)
ros2 topic pub /equilibrium std_msgs/msg/Int32 "data: 4"
```

>Watch how the pendulum moves in RViz2 and how the joint states change in your terminal windows.

---

### Using RQT Tools for Debugging

**RQT** (ROS Qt Framework) provides various GUI tools for debugging and monitoring ROS2 systems. Let's explore some useful ones:

#### RQT Graph

Visualize the ROS2 computation graph. This shows how nodes are connected through topics:

```bash
ros2 run rqt_graph rqt_graph
```

#### RQT Topic Monitor

Monitor topic activity and message content:

```bash
ros2 run rqt_topic rqt_topic
```

#### RQT Plot

Plot numerical data over time:

```bash
ros2 run rqt_plot rqt_plot
```

Add the joint positions to plot: `/joint_states/position[0]` and `/joint_states/position[1]`

## The myArm 300 Pi

Now that we understand the basics with a simple system, let's work with a more complex robot - the **myArm 300 Pi**, a 7-DOF robotic arm with various gripper options.

This robotic arm demonstrates:

- Multiple degrees of freedom (7 joints)
- Different end-effector configurations
- More complex URDF structure
- Real-world robot control integration

### Understanding URDF Files

Before we can visualize anything, we need to describe our robot. We do this by using **URDF** files. **URDF** (Unified Robot Description Format) is an XML format that specifies the physical properties of a robot. A URDF file contains:

- **Links** - The rigid bodies of the robot (like the different arm parts)
- **Joints** - The connections between links (how they can move relative to each other)
- **Visual elements** - How the robot looks (colors, shapes, meshes)
- **Collision elements** - How the robot interacts physically with the world
- **Inertial properties** - Mass and inertia characteristics

Let's examine the arm URDF! We first need to enter our arm workspace and then use the `cat` command to view the urdf file on the command line:

```bash
cd myarm_workspace
cat src/myarm_300_pi/urdf/myarm_300_pi.urdf
```

> **Student TODO**: Look at the URDF file structure. Can you identify the links and joints? What type of joints are used?

### Creating the myArm Control Node

In this exercise, we want to be able to visualize our robotic arm live. If we move the arm, we should be able to see it move in Rviz also. We also need an easy way to control the arm. We are going to use a simple pre-built node, that lets us control the arm through a GUI by moving a slider for each joint.

We will have to create a node to bridge all these together.

It will need one `publisher` that publishes the current state (position) of the robotic arm in the topic `/joint_states`. This is where Rviz will be listening (through the pre-built `robot_state_publisher`). This means that we will see a live visualization of our arm:

`simple_control_node` ===> `robot_state_publisher_node` ===> `Rviz`

> **Important!** The `robot_state_publisher` is a generic, pre-built node that listens to the `/joint_states` topic to read the state of the robot that we are publishing from our own custom node (in this case `double_pendulum_node`), and then publishes it to the `/tf` topic; which is the one that Rviz is listening to.

We also said that we want to be able to control the arm using some GUI sliders. We can do that by using the pre-built node `joint_state_publisher_gui`. This node make a gui window appear with one slider for each joint. It also publishes the value that each slider currently has on the `joint_states_targets` topic. So we are also going to need a `subscriber` that will be listening to the topic `/joint_states_targets`. There it wil receive the desired angle position of the joints.

With this design in mind, let's write our `simple_control_node`:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from pymycobot.myarm import MyArm
import math
import time

class SliderControlNode(Node):
    def __init__(self):
        super().__init__("slider_control")

        # Connection port as configurable parameter
        self.declare_parameter('port', '/dev/ttyAMA0')
        port = self.get_parameter('port').value

        # Connection baud rate as configurable parameter
        self.declare_parameter('baudrate', 115200)
        baudrate = self.get_parameter('baudrate').value

        # Print the connection settings
        self.get_logger().info(f"Connecting to port: {port}, with baudrate: {baudrate}")

        # Joint speed as configurable parameter (0-100)
        self.declare_parameter('joint_speed', 80)
        joint_speed = self.get_parameter('joint_speed').value

        # Create arm object
        self.mc = MyArm(port = port, baudrate = baudrate, timeout = 1.0)
        time.sleep(0.1)

        # Set mode: 1 always execute latest command first, 0 to execute in a queue
        self.mc.set_fresh_mode(mode = 1)
        time.sleep(0.1)

        # Set the arm to zero configuration
        self.mc.set_encoders([2048, 2048, 2048, 2048, 2048, 2048, 2048], joint_speed) 

        # Create publisher and timer for the joint states
        ############ ENTER CODE HERE ###############


        ############################################

        # Create subscriber to read the joint states targets from the GUI sliders
        ############ ENTER CODE HERE ###############


        ############################################
    
    def publish_states(self) -> None:
        """
        This function is periodically called by the timer. It publishes the current state (joint angles)
        of the arm's joints to the /joint_states topic.
        """

        # Create the message with the time stamp
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        # Set the joint names
        msg.name = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]

        # Read the current positions of th joints (in degrees)
        joint_angles_list = self.mc.get_angles()
       
       # Convert the joint angles to radians
        positions = []
        for angle_deg in joint_angles_list:
            angle_rad = round(math.radians(angle_deg), 3)
            positions.append(angle_rad)

        # Set joint positions
        msg.position = positions

        # Publish the message
        ############ ENTER CODE HERE ###############


        ############################################

    def move_arm(self, msg: JointState) -> None:
        """
        This function is used to move the arm to the desired position by reading JointState messages
        from the GUI sliders.
        """

        # Read the desired positions from the message
        joint_angles_list = []
        for angle_rad in msg.position:
            angle_deg = round(math.degrees(angle_rad), 3)
            joint_angles_list.append(angle_deg)

        # Read the desired speed (parameter value)
        joint_speed = max(1, min(int(self.get_parameter('joint_speed').value), 100))

        # Move the arm to the desired position at the desired speed
        ############ ENTER CODE HERE ###############


        ############################################

def main(args = None):
    try:
        rclpy.init(args = args)
        node = SliderControlNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
```

> **Student TODO I**: We need to create a `publisher` that sends `JointState` type messages in the `/joint_states` topic. We also need to create a timer, who every 0.01 seconds calls the `publish_states` function.

> **Student TODO II**: We also need to create a `subscriber` that receives `JointState` type messages in the `/joint_states_targets` topic and then calls the `move_arm` function.

> **Student TODO III**: The `publish_states` function creates a `JointState` type message that contains the current state of the robots joints. We need to use our publisher to publish this message.

> **Student TODO IV**: The `move_arm` function reads the desired target position message from the GUI. We want to move the arm to that desired position. We can use the `send_angles(angles, speed)` method on our `self.mc` object (our arm object).

---

### Creating the myArm Launch File

Let's create a launch file to start the myArm visualization with joint control:

The launch file can be found in `myarm_300_pi/launch/myarm_launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = FindPackageShare("myarm_300_pi").find("myarm_300_pi")

    urdf_file = PathJoinSubstitution([pkg_share, "urdf", "myarm_300_pi.urdf"])
    rviz_config_file = PathJoinSubstitution([pkg_share, "config", "display_myarm_300_pi.rviz"])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": ParameterValue(Command(["cat ", urdf_file]), value_type = str)
            }],
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            output="screen",
            remappings=[("/joint_states", "/joint_states_targets")],
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_file],
            output="screen",
        ),
        
        ############ ENTER CODE HERE ###############


        ############################################
    ])
```

> **Student TODO**: In order to be able to visualize our arm correclty, we need to launch four nodes: the `rviz2` (which launches rviz), `robot_state_publisher` (to bridge our node with rviz), `joint_state_publisher_gui` (for the GUI sliders) and of course our own node. Add our `simple_control_node` in the `LaunchDescription` section like we did in the previous lab.
---

### Launching the myArm Visualization

We are ready to launch everything and see our robotic arm! As we have learned, we need to `build` and `source` first:

```bash
colcon build
source install/setup.bash
```

and now we can launch!

> **BE VERY CAREFUL WHEN LAUNCHING THE ROBOT!** It will configure itself to the zero position, which is the upright position. Make sure there is enough space before you try it.

```bash
ros2 launch myarm_300_pi myarm_launch.py
```

---

### Using the Joint State Publisher GUI

The myArm launch includes the `joint_state_publisher_gui`, which provides sliders to manually control each joint:

1. Look for the joint state publisher GUI window
2. Use the sliders to move each joint
3. Watch the arm move in real-time in RViz2

> **Student TODO**: Try to move the arm into different poses. Can you make the end-effector reach different positions in space?