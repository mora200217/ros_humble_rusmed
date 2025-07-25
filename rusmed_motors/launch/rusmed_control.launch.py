from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
import launch_ros.descriptions
import os, xacro

def generate_launch_description():
    

    pkg_dir_description = get_package_share_directory('rusmed_motors') # Get pkgs 

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare("rusmed_motors"),
                    "description",
                    "rusmed_robot.xacro.urdf",
                ]
            ),
        ]
    )
    robot_description = {"robot_description": launch_ros.descriptions.ParameterValue(robot_description_content,  value_type=str)}

    # startup_controllers

    # rviz = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz',  
    #      arguments=["-d", os.path.join(pkg_dir_description, 'config', 'rviz_viz.rviz')]
    #     )
    

    robot_state_pub = Node(
        package='robot_state_publisher', 
        executable='robot_state_publisher', 
        parameters=[robot_description]
    )

    joint_state_pub = Node(
        package='joint_state_publisher', 
        executable='joint_state_publisher'
        # parameters=[params]
    )


    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("rusmed_motors"),
            "config",
            "rusmed_motors_controllers.yaml",
        ]
    )



    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers],
        output="both",
        remappings=[
            ("~/robot_description", "/robot_description"),
        ],
    )

    # Delay 
    # delay_control_node_until_coppeliasim = ExecuteProcess([

    # ])

    position_controller_node = Node(
        package='controller_manager', 
        executable="spawner", 
        arguments=["position_controller", "--controller-manager", "/controller_manager"], 
        parameters=[""]
    )

    joint_broadcaster_node = Node(
        package='controller_manager', 
        executable="spawner", 
        arguments=["joint_state_broadcaster" , "--controller-manager", "/controller_manager"], 
        parameters=[""]
    )

    
   
    return LaunchDescription([
        # coppelia,
        # rviz,
        joint_state_pub,
        robot_state_pub,
        control_node,
        # control_node,
        position_controller_node,
        joint_broadcaster_node
        ])