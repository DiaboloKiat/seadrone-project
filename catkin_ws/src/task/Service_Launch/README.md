# Tutorial
## [AprilTag](https://ieeexplore.ieee.org/document/5979561) and [AprilTag 2](https://ieeexplore.ieee.org/document/7759617)
- **Paper**
    - E. Olson, “Apriltag: A robust and flexible visual fiducial system,” in Robotics and Automation (ICRA), 2011 IEEE International Conference on. IEEE, 2011, pp. 3400–3407.
    - J. Wang and E. Olson, “AprilTag 2: Efficient and robust fiducial detection,” in Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), October 2016.
- **Github**
    - [apriltags_ros](https://github.com/RIVeR-Lab/apriltags_ros)
    - [apriltags2_ros](https://github.com/ChalmersRobotPostman/apriltags2_ros)
    - [apriltag](https://github.com/AprilRobotics/apriltag)

- **Tags**
    - [Tag36h11](https://introlab.3it.usherbrooke.ca/mediawiki-introlab/images/7/72/Tags2x2.pdf)

## [roslaunch](http://wiki.ros.org/roslaunch)



## [rosservice](http://wiki.ros.org/Services)



## **How to run**
### **Face Detection Server**
#### Open a terminal (T1)
> Start Seadrone
```
laptop $ cd ~/Seadrone
laptop $ source environment.sh
laptop $ roslaunch seadrone seadrone_start.launch rviz:=false
```
#### Open seconde terminal (T2)
```
laptop $ cd ~/Seadrone
laptop $ source environment.sh
laptop $ rosrun apriltag service_server
```
#### Open another terminal (T3)
> We can call the service from command line directly, then you might see the result and an image named test_YYYYMMDDHHmmss.jpg shown in ```~/Seadrone/catkin_ws/src/task/Service_Launch/apriltag/image```.
```
laptop $ cd ~/Seadrone
laptop $ source environment.sh
laptop $ rosservice call /my_service "filename: test"
```
> Other than calling from command line, we can also call the service from our node, the source code is available at ```~/Seadrone/catkin_ws/src/task/Service_Launch/apriltag/src/client_call.cpp```.
```
laptop $ rosrun apriltag call_from_client
```
#### Open a terminal (T1)
> So far, we use one terminal to start a ROS master, one to turn on your webcam, one to run the service and the last to call the service, what a messy! Is there any easier way to get the same result? Of course YES! But we need the help of ```roslaunch``` command and a ```.launch``` file. 

> ```.launch``` is a XML format file that help you start up the master, launch multiple nodes locally and remotely via SSH, as well as set parameters on the parameter server. 

> Though there are many tags you can refer from [here](http://wiki.ros.org/roslaunch/XML), the following is a simple example teaching you how to write a launch file.
```
laptop $ roslaunch tutorial face_detection_server.launch
```
> Since ```call_from_client``` node is required, and we use default ```one_shot``` argument, whole processes will be killed after it finished.
```
laptop $ roslaunch tutorial face_detection_server.launch one_shot:=false
```

### **AprilTag Detection Server**
#### Open a terminal (T1)
```
laptop $ cd ~/Seadrone
laptop $ source environment.sh
laptop $ roslaunch tutorial topic2.launch
```

#### Open a terminal (T1)
> Distance Between Tags Service
```
laptop $ cd ~/Seadrone
laptop $ source environment.sh
laptop $ roslaunch tutorial assignment.launch
```
#### Open another terminal (T2)
```
laptop $ cd ~/Seadrone
laptop $ source environment.sh
laptop $ rosservice call /assignment "tag1_id: 12 tag2_id: 13"
```
