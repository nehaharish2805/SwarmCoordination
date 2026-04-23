from setuptools import find_packages, setup

package_name = 'swarm_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/swarm_pkg']),
    ('share/swarm_pkg', ['package.xml']),
    ('share/swarm_pkg/launch', ['launch/multi_robot.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='neha',
    maintainer_email='neha@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
    'follower = swarm_pkg.follower:main',
    ],
    },
)
