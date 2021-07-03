    #include "ros/ros.h"
    #include "beginner_tutorials/task.h"
    
    bool add(beginner_tutorials::task::Request  &req,
             beginner_tutorials::task::Response &res)
    {
    
      if (res.num1 > req.num2){
        res.greater = req.num1;
      }
      else{
        res.greater = req.num2;
      }
      ROS_INFO("request: x=%f, y=%f", (float)req.num1, (float)req.num2);
      ROS_INFO("sending back response: [%f]", (float)res.greater);
     return true;
   }
   
   int main(int argc, char **argv)
   {
     ros::init(argc, argv, "greater_num");
     ros::NodeHandle n;
   
     ros::ServiceServer service = n.advertiseService("greater_num", add);
     ROS_INFO("Dsiplaying greater no");
     ros::spin();
   
     return 0;
   }
