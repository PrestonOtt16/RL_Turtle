from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'rl_turtle'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    	(os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    	(os.path.join('share', package_name, 'config'), glob(os.path.join('config', 'turtle.yaml'))),
    	('share/' + package_name + '/meshes', glob('meshes/*')),
    	(os.path.join('share', package_name, 'urdf'), glob('urdf/*.[uU][rR][dD][fF]')),
    	(os.path.join('share',package_name,'world'), glob(os.path.join('world','empty_world.sdf'))),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*'))
        
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='preston',
    maintainer_email='prestonottsuperluminal@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
