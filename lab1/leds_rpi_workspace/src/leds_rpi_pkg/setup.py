import os
from glob import glob
from setuptools import setup

package_name = 'leds_rpi_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grog Strongjaw',
    maintainer_email='grog_strongjaw@mymail.com',
    description='This is also a very cool project.',
    license='I certainly have a licence for this.',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
	    'pub_blink_node = leds_rpi_pkg.blink_led_pub_node:main',
        'pub_button_node = leds_rpi_pkg.button_pub_node:main',
	    'sub_led_node = leds_rpi_pkg.led_sub_node:main'
        ],
    },
)