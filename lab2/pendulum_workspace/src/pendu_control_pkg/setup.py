from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'pendu_control_pkg'

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
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.urdf'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grog Strongjaw',
    maintainer_email='grog_strongjaw@vm.com',
    description='This is a very cool double pendulum control package',
    license='Sure, I have a licecne for this',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'double_pendulum_node=pendu_control_pkg.double_pendulum_node:main',
        ],
    },
)
