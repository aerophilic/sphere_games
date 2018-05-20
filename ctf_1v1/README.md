# ctf_1v1
## Capture the Flag - 1 versus 1

ROS/Gazebo simulation of sphere robots for reinforcement learning activities

Designed in Ubuntu 16.04 using ROS Kinetic and Gazebo 7.

## Installation
Make sure the following commands have been added to your .bashrc file or ran in the terminal used to launch rosrun:
```
source /opt/ros/kinetic/setup.bash
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:[INSERT_PATH_TO_REPO]/ctf_1v1/build
```

Create and configure a virtual environment for managing Python packages:
```
sudo apt install virtualenv python-opencv
mkdir python2_env
virtualenv python2_env --python=python2.7
source python2_env/bin/activate
pip install --upgrade pip
pip install numpy pyyaml rospkg catkin_pkg
```

## Build
In a terminal, 
```
cd [REPO_PATH]/ctf_1v1/
mkdir build
cd build
cmake ../
make
```

## Execution
In a terminal, run `roscore`

In a second terminal, 
```
cd [REPO_PATH]/ctf_1v1/
source /usr/share/gazebo/setup.sh
rosrun gazebo_ros gazebo ctf_1v1_arena.world
```

In a third terminal, run the sphere tracker python script:
```
source ~/python2_env/bin/activate
cd [repo_path]/ctf_1v1/
python sphere_tracker.py
```

In a fourth terminal, run the simple reinforcement learning agent script:
```
source ~/python2_env/bin/activate
cd [repo_path]/ctf_1v1/
python two_agent_Q-learning.py
```

The red and blue spheres will both attempt to reach the other teams 'flag' and return to their own base as quickly as possible.
