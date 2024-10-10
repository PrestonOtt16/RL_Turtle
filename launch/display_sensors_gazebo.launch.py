from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution, LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory
from launch.event_handlers import OnProcessExit
import os
import xacro


def generate_launch_description():
	
	pkg_gazebo_sims = get_package_share_directory('rl_turtle')
	world_file = os.path.join(pkg_gazebo_sims, 'world','empty_world.sdf')
	urdf_file = os.path.join(pkg_gazebo_sims,'urdf','turtle_sensors.xacro.urdf')
	
	#setting environment varible so gazebo can find my mesh files
	os.environ["GAZEBO_MODEL_PATH"] = os.path.join(get_package_share_directory('rl_turtle'), 'meshes')
	
	#print(pkg_gazebo_sims)
	#with open(urdf_file, 'r') as infp:
		#robot_desc = infp.read()
		
	#print(pkg_gazebo_sims)
	
	xacro_file = os.path.join(pkg_gazebo_sims,
                              'urdf',
                              'turtle_sensors.xacro.urdf')

	doc = xacro.parse(open(xacro_file))
	xacro.process_doc(doc)
	params = {'robot_description': doc.toxml()}
		
	
	
	declare_world_cmd = DeclareLaunchArgument(
		'world',
		default_value = world_file,
		description = 'empty world SDF')
		
	n3 = Node(
		package = 'joy',
		executable = 'game_controller_node',
		output = 'screen'
		)
	
	n4 = Node(
		package = 'teleop_twist_joy',
		executable = 'teleop_node',
		arguments = ['cmd_vel:=/diff_drive_base_controller/cmd_vel_unstamped'],
		parameters = [{
    		'scale_linear.x': 0.5,
    		'scale_angular.yaw': 1.0,
		}],
		output = 'screen'
		)
		
		
	n2 = Node(
		package = 'gazebo_ros',
		executable = 'spawn_entity.py',
		arguments = ['-topic','robot_description','-entity','turtle','-x','0','-y','0','-z','0.10'],
		output = 'screen'
		)
	
	n1 = Node(
		package = 'robot_state_publisher',
		executable = 'robot_state_publisher',
		name = 'robot_state_publisher',
		parameters = [params],
		#parameters = [{'robot_description': params, 'use_sim_time': True}],
		output = 'screen'
		)
	
	load_joint_state_broadcaster = ExecuteProcess(
        	cmd=['ros2', 'control', 'load_controller', '--set-state', 'active','joint_state_broadcaster'],
        	output='screen'
    		)
    		
	load_diff_drive_base_controller = ExecuteProcess(
        	cmd=['ros2', 'control', 'load_controller', '--set-state', 'active','diff_drive_base_controller'],
        	output='screen'
    	)
		
	
	lf1 = IncludeLaunchDescription(
		PythonLaunchDescriptionSource([
			PathJoinSubstitution([
				FindPackageShare('gazebo_ros'),
					'launch',
					'gazebo.launch.py'
				])
			])
		,launch_arguments = {'world' : LaunchConfiguration('world')}.items())
	
		
	ld = LaunchDescription()
	
	ld.add_action(declare_world_cmd)
	ld.add_action(n1)
	ld.add_action(lf1)
	ld.add_action(n2)
	ld.add_action(load_joint_state_broadcaster)
	ld.add_action(load_diff_drive_base_controller)
	ld.add_action(n3)
	ld.add_action(n4)
	
	return ld
			
