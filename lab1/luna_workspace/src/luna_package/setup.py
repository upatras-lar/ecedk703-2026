from setuptools import find_packages, setup

package_name = 'luna_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grog Strongjaw',
    maintainer_email='grog_strongjaw@mymail.com',
    description='This is a very cool project.',
    license='I certainly have a licence for this.',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'luna_commander = luna_package.luna_commander_node:main',
            ### ENTER CODE #########
    
    
            ########################
        ],
    },
)