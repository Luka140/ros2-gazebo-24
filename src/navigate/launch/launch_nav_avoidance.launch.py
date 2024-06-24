import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('navigate'),
        'config',
        'params.yaml'
        )
        
    nav_pose_server=Node(
        package = 'navigate',
        name = 'nav_pose_avoidance_server',
        executable = 'nav_pose_avoidance_server',
        parameters = [config],
        output = 'log',
        remappings=[
            ('/input/odom', '/diff_cont/odom'),
            ('/output/reference', '/nav/goal_pose'),
            ('/input/point_cloud', '/cloud')
        ]
    )

    nav_pose_client=Node(
        package = 'navigate',
        name = 'nav_pose_client',
        executable = 'nav_pose_client',
        output = 'log',
        remappings=[
            ('/input/goal_pose', '/goal_pose')
        ]
    )

    nav_controller=Node(
        package = 'navigate',
        name = 'nav_controller',
        executable = 'nav_controller',
        output = 'screen',
        remappings=[
            ('/input/pose', '/nav/goal_pose'),
            ('/input/odom', '/diff_cont/odom'),
            ('/output/cmd_vel', '/diff_cont/cmd_vel'),
        ]
    )

    return LaunchDescription([
        nav_pose_server,
        nav_pose_client,
        nav_controller
    ])