import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'camera_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
        (os.path.join('share', package_name, 'config', 'rviz'), glob(os.path.join('config', 'rviz', '*.rviz'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grog Strongjaw',
    maintainer_email='grog_strongjaw@vm.com',
    description='Lights, cameras and go!',
    license='I definetely have a licence for this.',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "aruco_detection = camera_pkg.aruco_detection:main",
        ],
    },
)