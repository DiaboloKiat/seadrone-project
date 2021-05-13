#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Joy.h"
#include <apriltags2_ros/AprilTagDetectionArray.h>
#include <apriltags2_ros/AprilTagDetection.h>
#include "CUDPCommUser.hpp"
#include <iostream>
#include <math.h>
using namespace std;

int led_brightness_top=0;
float gimbal_Pitch=0;		//camera move (don't really need)
float c_forces_moments_[2]={0};
double max_rotor=3;
int depth_flag=0;
int last_depth_flag=0;
double delta_depth=0;
double yaw=0;			//seadrone turn

double x=0;		//put the x y z of detection result
double y=0;
double z=0;
int see_nothing = 1;	 //if see nothing

void detectrun(){	//put the msg from camera
    //armed or not
     
    //seadrone should turn if see nothing
    while(see_nothing){
	yaw += 10;
	if(x!=0 || y!=0 || z!=0)     //if see the tag, then see_nothing should become false
    	    see_nothing=0;
	usleep(50);
	}
    //led brightness turn on
    led_brightness_top = 50;

    //motor move
    if(x>=10)			//must move right
	c_forces_moments_[1] = 0.1*max_rotor;	//chech for right or left
    else if(x<=-10)		//move left
	c_forces_moments_[1] = (-0.1*max_rotor);

    if(z>=50)			//too far away from the ring, so move forward
	c_forces_moments_[0]= 0.1*max_rotor;
    else if(z<30)		//too close, so move backward
	c_forces_moments_[0]=(-0.1)*max_rotor;

    if(y>=10){
	delta_depth -=10;		//check for depth
	depth_flag=1;
    }
    else if(y<=-10){
	delta_depth +=10;
	depth_flag=1;
    }
    else{
	delta_depth=0;
	depth_flag=0;
    }	
}

void apriltag_cb(const apriltags2_ros::AprilTagDetectionArray::ConstPtr& data){
    if (sizeof(data->detections) == NULL)
        cout << "no apriltags detected" << endl;
    else{
        apriltags2_ros::AprilTagDetection atd = data->detections[0];
        x = atd.pose.pose.pose.position.x;
        y = atd.pose.pose.pose.position.y;
        z = atd.pose.pose.pose.position.z;
        cout << "x:" << " " << x << " " << "y:" << " " << y << "z:" << " " << z << endl;
    }
    detectrun();
}


int main(int argc, char **argv){
    ros::init(argc, argv, "sea");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe("/seadrone/tag_detections", 1000, apriltag_cb);

    //udp communication
    orobotix::CUDPCommUser udpUser_;
    orobotix::SRobotDataUser robotData;

    //initialize the flag
    robotData.flag_enable_camera_[0]=1;
    robotData.flag_enable_camera_[1]=0;
    robotData.flag_enable_camera_[2]=0;
    robotData.flag_enable_individual_control_=false;
    robotData.flag_enable_thruster_=false;
    //
    bool flag_run_=true;

    //set communication
    robotData.droneIP_="192.168.0.122";
    robotData.dronePort_=8090;
    robotData.config_id_=1;

    robotData.initThrusterInfo(5);
   
    udpUser_.init(&robotData);

    int count=0;
    while(flag_run_){
	robotData.gimbal_Pitch_ = gimbal_Pitch;
	robotData.led_brightness_top_ = led_brightness_top;
    int arm_flag = 1;
	if(arm_flag==1){
	    robotData.flag_enable_thruster_ =true;
	    robotData.c_forces_moments_[0]=c_forces_moments_[0];
	    robotData.c_forces_moments_[1]=c_forces_moments_[1];
	    robotData.c_forces_moments_[2]=delta_depth/200;

            robotData.goal_Eular_[0]=yaw;

	    if(depth_flag==0 && last_depth_flag==1){
		robotData.flag_enable_thruster_ = false;
	    };
     	    last_depth_flag = depth_flag;
	}
	else{
	    robotData.flag_enable_thruster_ = false;
	}
	udpUser_.thread_communication_send();
	udpUser_.thread_communication_rev();

	ros::spinOnce();
	usleep(50);
    }
    printf("\nMain: udpUser_.closeConnection() called!");
    printf("\nTerminated robotDemo app!\n");
    return EXIT_SUCCESS;
}
