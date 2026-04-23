from launch import LaunchDescription
from launch_ros.actions import Node

MODEL_PATH = "/opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf"

def generate_launch_description():
    return LaunchDescription([

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            namespace='robot1',
            arguments=[
                '-entity', 'robot1',
                '-file', MODEL_PATH,
                '-robot_namespace', 'robot1',
                '-x', '0', '-y', '0', '-z', '0.01'
            ],
            output='screen'
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            namespace='robot2',
            arguments=[
                '-entity', 'robot2',
                '-file', MODEL_PATH,
                '-robot_namespace', 'robot2',
                '-x', '5', '-y', '0', '-z', '0.01'
            ],
            output='screen'
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            namespace='robot3',
            arguments=[
                '-entity', 'robot3',
                '-file', MODEL_PATH,
                '-robot_namespace', 'robot3',
                '-x', '-5', '-y', '0', '-z', '0.01'
            ],
            output='screen'
        ),

    ])
