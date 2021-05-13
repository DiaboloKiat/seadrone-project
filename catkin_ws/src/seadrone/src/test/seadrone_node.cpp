#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Joy.h"

// udpUser
#include "CUDPCommUser.hpp"
#include <iostream>
#include <math.h>
using namespace std;

bool motor = false;
bool power_off = false;
bool flag_run_ = true;

//LED
int led_brightness_top = 0;
int led_brightness_bot = 0;

//Camera
float gimbal_Pitch = 0.314;

//motor
float c_forces_moments_[2]={0};
double max_motor = 3;  //max 1~12
int depth_flag = 0;
int last_depth_flag = 0;
double delta_depth = 0;
double yaw = 0;   //z axis

void joycallback(const sensor_msgs::Joy::ConstPtr& msg)
{
	//ROS_INFO("callback triggered");
  /*
  //button: Start(7)
  if (msg->buttons[7])
  {
    arm_flag = -arm_flag;
    if (arm_flag==1)
      ROS_INFO("rotors armed");
    else
      ROS_INFO("rotors disarmed");
  }
  */
  //button: RB(5)
  if(msg->buttons[5]==1)
  {
    motor = true;
    ROS_INFO("motor start!!!");
  }
  else if(msg->buttons[5]==0)
  {
    motor = false;
    ROS_INFO("motor stop!!!");
  }


  //button: Logitech/Power(8)
  if (msg->buttons[8])
  {
    power_off = true;
    flag_run_ = false;
    ROS_INFO("Power off");
  }

  /*
  //joy.axes: (1)joystick L_y -1~1
  if (msg->axes[1]==-1) //(msg->axes[1]==-1 && gimbal_Pitch<1.57)
    gimbal_Pitch+=0.314;
  if (msg->axes[1]==1 && gimbal_Pitch>0)
    gimbal_Pitch-=0.314;
  //joy.axes: (0)joystick L_x -1~1
  if (msg->axes[0]==-1) //(msg->axes[0]==-1 && led_brightness_top<100)
    led_brightness_top+=10;
  if (msg->axes[0]==1 && led_brightness_top>0)
    led_brightness_top-=10;
  */

  //button: Y(3) A(0)
  if (msg->buttons[0]==1 && gimbal_Pitch<1.5) //(msg->axes[1]==-1 && gimbal_Pitch<1.57)
    gimbal_Pitch+=0.157;
  if (msg->buttons[3]==1 && gimbal_Pitch>-0.7)
    gimbal_Pitch-=0.157;

  //button: X(2) B(1)
  if (msg->buttons[1]==1 && led_brightness_top<100)
  {
    led_brightness_top+=5;
    //led_brightness_bot+=5;
  } 
  if (msg->buttons[2]==1 && led_brightness_top>0)
  {
    led_brightness_top-=5;
    //led_brightness_bot-=5;
  }

  //button: LB(4)
  if(msg->buttons[4]==1)
  {
    led_brightness_bot = 100;
  }
  else if(msg->buttons[4]==0)
  {
    led_brightness_bot = 0;
  }
    
  //motor
  //joy.axes: (3)joystick R_x -1~1  (4)joystick R_y -1~1
  c_forces_moments_[1] = (msg->axes[3])*max_motor;
  c_forces_moments_[0] = (msg->axes[4])*max_motor;
  //cout << c_forces_moments_[0] << endl;
  
  /*
  //joy.axes: (5)RT -1~1  (2)LT -1~1
  if(msg->axes[5]!=1 && msg->axes[2]==1)
  {
    delta_depth=(msg->axes[5]-1); 
    delta_depth=abs(delta_depth);
    depth_flag=1;
  }
  else if(msg->axes[2]!=1 && msg->axes[5]==1)
  {   
    delta_depth=(msg->axes[2]-1);   
    depth_flag=1;  
  }
  else
  {
    delta_depth=0;
    depth_flag=0;
  }
  */
  //joy.axes: (7)x+ U=1~D=-1
  if(msg->axes[7]==1)
  { 
    delta_depth=1;
    depth_flag=1;
  }
  else if(msg->axes[7]==-1)
  {   
    delta_depth=-1;   
    depth_flag=1;  
  }
  else
  {
    delta_depth=0;
    depth_flag=0;
  }



  //joy.axes: (６)x+ L=1~R=-1
  if(msg->axes[6]==-1)
  {
    yaw-=30;
  }
  if(msg->axes[6]==1)
  {
    yaw+=30;
  }
  cout << delta_depth << " " << yaw << endl;
}


int main(int argc, char **argv) 
{
  ros::init(argc, argv, "seadrone_node");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("joy", 1000, joycallback);
  printf("Started\n");

  /** udp communication */
  orobotix::CUDPCommUser udpUser_;
  orobotix::SRobotDataUser robotData;

  // initialize the flag
  robotData.flag_enable_camera_[0] = 1;
  robotData.flag_enable_camera_[1] = 0;
  robotData.flag_enable_camera_[2] = 0;
  robotData.flag_enable_individual_control_ = false;
  robotData.flag_enable_thruster_ = false;
  //robotData.flag_change_control_gain_ = true;

  // set communication
  robotData.droneIP_ = "192.168.0.122";
  //robotData.droneIP_ = "192.168.1.122";
  robotData.dronePort_ = 8090;
  robotData.config_id_ = 1;

  robotData.drone_please_power_off = power_off;

  
  //robotData.ctr_kp_[0] = 1;
  //robotData.ctr_kv_[0] = 1;
  //robotData.ctr_ki_[0] = 1;

  //robotData.goal_depth_ = -0.5;		//depth
  //robotData.depth_vel_ = 0.05;
  //robotData.gimbal_Pitch_ = 0;

  //robotData.ctr_kp_[1] = 1;
  //robotData.ctr_kp_[2] = 1;
  //robotData.ctr_kp_[3] = 1;
  //robotData.ctr_kp_[4] = 1;
  
  //robotData.led_brightness_top_ = 10;
  //robotData.led_brightness_bot_ = 10;

  // thruster
  robotData.initThrusterInfo(5);
  
  //robotData.c_forces_moments_[0] = 10;
  //robotData.goal_depth_ = 0;

  //robotData.goal_Eular_[0] = 90;		//right angle degree
  
  // initialize the udp communication
  udpUser_.init(&robotData);
  //robotData.flag_change_control_gain_ = true;
  //robotData.ctr_kp_[0] = 0.1;
  
  while (flag_run_) 
  {
    robotData.gimbal_Pitch_ = gimbal_Pitch;
    robotData.led_brightness_top_ = led_brightness_top;
    robotData.led_brightness_bot_ = led_brightness_bot;
    
    if(motor)
    {
      robotData.flag_enable_thruster_ = true;
      robotData.c_forces_moments_[0]=c_forces_moments_[0];
      robotData.c_forces_moments_[1]=c_forces_moments_[1]; 
      robotData.c_forces_moments_[2] = delta_depth/200;

      robotData.goal_Eular_[0] = yaw;
      //robotData.goal_depth; 
      
      if(depth_flag == 0 && last_depth_flag == 1)
      {
        robotData.flag_enable_thruster_ = false;
      }
      last_depth_flag = depth_flag;
    }
    else
    {
      robotData.flag_enable_thruster_ = false;
    }
    //cout << robotData.depth_ << endl;
    
    udpUser_.thread_communication_send();
    udpUser_.thread_communication_rev();

    ros::spinOnce();
    usleep(10); // wrong sleeping interval may cause rotors to fail
  }
  
  printf("\nMain: udpUser_.closeConnection() called!");
  //udpUser_.closeSocket();

  printf("\nTerminated robotDemo app!\n");
  return EXIT_SUCCESS;
}