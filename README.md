# Swarm Coordination of Ground Robots (ROS 2 + Gazebo)

---

## Overview 🚀
This project implements swarm coordination using a leader–follower approach in a simulated environment. Multiple TurtleBot3 robots are deployed in Gazebo, where one robot acts as the leader and the others act as followers. The followers maintain a fixed formation relative to the leader using odometry-based feedback and control logic.

---

## Objective 🎯
The objective of this project is to demonstrate multi-robot coordination where:
- Robots interact using local information  
- Followers maintain a desired formation  
- Motion is controlled using odometry feedback  

---

## Key Concepts 🧠
- Leader–Follower Model  
- Formation Control  
- Odometry-based Feedback  
- Proportional Control  
- ROS 2 Publisher–Subscriber Communication  

---

## System Architecture ⚙️

The leader robot is controlled manually using keyboard input.  
The follower node subscribes to odometry data, computes motion, and publishes velocity commands.

Keyboard Input
      ↓
/robot1/cmd_vel  (Leader)
      ↓
/robot1/odom
      ↓
Follower Node (follower.py)
      ↓
/robot2/cmd_vel, /robot3/cmd_vel
      ↓
Follower Robots

---

## Technologies Used 🛠️
- ROS 2 (Humble)  
- Gazebo Simulator  
- TurtleBot3  
- Python (rclpy)  

---

## Robot Roles 🤖

| Robot  | Role |
|--------|------|
| robot1 | Leader (manual control) |
| robot2 | Follower |
| robot3 | Follower |

---

## Project Structure 📂

swarm_ws/
├── src/
│   └── swarm_pkg/
│       ├── follower.py
│       ├── launch/
│       │   └── multi_robot.launch.py
│       ├── package.xml
│       ├── setup.py
│       └── __init__.py

---

## Working Principle 🔄

### Target Position Calculation
Each follower computes a target position relative to the leader:

target = leader_position + rotated_offset

Offsets define the formation:
- robot2: (-0.7, 0)  
- robot3: (-1.4, 0)  

---

### Error Computation

dx = target_x - fx  
dy = target_y - fy  

distance = sqrt(dx² + dy²)  
desired_angle = atan2(dy, dx)  

angle_error = desired_angle - current_yaw  

---

### Control Strategy

- Rotate toward target  
- Move forward when aligned  
- Slow down near the target  
- Stop when close enough  

---

### Velocity Commands

- linear.x controls forward motion  
- angular.z controls rotation  

---

## How to Run ▶️

### 1. Build workspace
cd ~/swarm_ws  
colcon build  
source install/setup.bash  

---

### 2. Launch Gazebo
ros2 launch turtlebot3_gazebo empty_world.launch.py  

---

### 3. Spawn robots
ros2 launch swarm_pkg multi_robot.launch.py  

---

### 4. Run follower node
ros2 run swarm_pkg follower  

---

### 5. Control leader
ros2 run teleop_twist_keyboard teleop_twist_keyboard  

---

## Output Behavior 📊
- Followers maintain line formation behind the leader  
- Formation moves and rotates with the leader  
- Followers stop at predefined distances  
- Stable and smooth motion  

---

## Algorithm Used 📌
- Leader–Follower Formation Control  
- Closed-loop Feedback Control  
- Proportional Control  

---

## Limitations ⚠️
- No obstacle avoidance  
- No inter-robot communication  
- Fixed formation only  

---

## Future Improvements 🔮
- Add obstacle avoidance using LiDAR  
- Implement dynamic formation control  
- Enable communication between robots  
- Extend to multi-leader swarm systems  

---

## Contribution 👨‍💻
- Implemented follower control logic  
- Designed formation algorithm  
- Configured multi-robot simulation  

---

## Conclusion 📍
This project demonstrates a working swarm coordination system where multiple robots maintain formation using real-time feedback and control logic in a ROS 2 simulation environment.
