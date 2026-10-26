import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'myarm_300_pi'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml')) + glob(os.path.join('config', '*.rviz'))),
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.urdf')) + glob(os.path.join('urdf', '*.xacro')) + glob(os.path.join('urdf', '*.urdf.xacro'))),
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*.dae')) + glob(os.path.join('meshes', '*.stl'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grog Strongjaw',
    maintainer_email='grog_strongjaw@vm.com',
    description='This is a very cool robotics project',
    license='Sure, here is my licence',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_control_node = myarm_300_pi.simple_control_node:main', 
        ],
    },
)
