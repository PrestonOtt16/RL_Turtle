from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution, LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory
import os
import xacro


def generate_launch_description():
	
	
	rosbag_sim = ExecuteProcess(
        	cmd=['ros2', 'bag', 'record','--use-sim-time','/diff_drive_base_controller/odom'],
        	output='screen'
    		)
    		
	#rosbag_real = ExecuteProcess(
        #	cmd=['ros2', 'bag', 'record', '/odom'],
        #	output='screen'
    	#	)
    		
    	
	n1 = Node(
    		package = 'plotjuggler',
    		executable = 'plotjuggler',
    		output = 'screen'
    		)
    		
		
		
	ld = LaunchDescription()
	ld.add_action(rosbag_sim)
	#ld.add_action(rosbag_real)
	
	return ld
			
