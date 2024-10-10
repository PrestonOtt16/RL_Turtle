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
	
	pkg_gazebo_sims = get_package_share_directory('rl_turtle')
	world_file = os.path.join(pkg_gazebo_sims, 'world','empty_world.sdf')
	urdf_file = os.path.join(pkg_gazebo_sims,'urdf','turtle.xacro.urdf')
	
	
	#Nodes for controlling turtlebot with ps4 controller, and plotting turtlebot odometry data
	n1 = Node(
		package = 'joy',
		executable = 'game_controller_node',
		output = 'screen'
		)
	
	n2 = Node(
		package = 'teleop_twist_joy',
		executable = 'teleop_node',
		arguments = ['cmd_vel:=/commands/velocity'],
		parameters = [{
    		'scale_linear.x': 0.5,
    		'scale_angular.yaw': 1.0,
		}],
		output = 'screen'
		)
		
	
		
	ld = LaunchDescription()
	ld.add_action(n1)
	ld.add_action(n2)
	
	return ld
			
