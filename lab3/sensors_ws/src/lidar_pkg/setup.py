import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'lidar_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.rviz'))),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grog Strongjaw',
    maintainer_email='grog_strongjaw@vm.com',
    description='Hi there, hello! Look at my cool lidar package!',
    license='Yep, here is my licence',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "closest_obstacle = lidar_pkg.radar:main",
        ],
    },
)
