#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix, Imu
import time
from haversine import haversine
import pyproj
from tf.transformations import euler_from_quaternion
import numpy as np
from geometry_msgs.msg import Twist
import math 
# latitude: 49.8998895568
# longitude: 8.89995254825
class Robot:
    def __init__(self):
        self.lat = 0
        self.long = 0
        self.lat_goal =  49.8999263921 #49.8998895568  #49.9001340641 #49.8999839496 
        self.long_goal =  8.89986112816 #8.89995254825 #8.9000669039 #8.900031216 
        self.yaw = 0
        self.distance = 0
        self.az = 0 
        self.linear = False
        self.rate = rospy.Rate(1)
        rospy.Subscriber('/group_task2/fix', NavSatFix, self.calc_geod)
        self.rate.sleep()
        rospy.Subscriber('/group_task2/imu', Imu, self.calc_yaw)
        self.rate.sleep()
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.rate.sleep()
  
    def calc_geod(self, data1):
        self.lat = data1.latitude
        self.long = data1.longitude
        g = pyproj.Geod(ellps='WGS84')
        x = g.inv(self.long, self.lat, self.long_goal, self.lat_goal)
        self.az = x[0]
        self.az = self.change_range(self.az)
        self.distance = x[2]
        print "az:", self.az

    def calc_yaw(self, data2):
        orient = data2.orientation
        orient_array = np.array([orient.x, orient.y, orient.z, orient.w]) 
        orient_array_euler = euler_from_quaternion(orient_array)
        self.yaw = orient_array_euler[2]
        self.yaw = self.yaw * 180 /math.pi
        self.yaw = -self.yaw
        self.yaw = self.change_range(self.yaw)
        print "yaw: ", self.yaw
    

    def change_range(self, y):
        if y<0:
            y = y + 360 
            return y
        else: 
            return y

    def orientation_rover(self):
       
        vel = Twist()
        while not rospy.is_shutdown(): 
                    
            if self.az > self.yaw:
                
                if self.az-self.yaw > 180:
                    self.yaw = self.yaw + 360
                    vel.angular.z = -0.2
                    self.pub.publish(vel)
                    print self.az - self.yaw, "case 1"
                    print self.yaw
                
                elif self.az-self.yaw < 180:
                    
                    if self.az-self.yaw <=1:
                        self.linear = True
                        vel.angular.z = 0
                        self.pub.publish(vel)
                        print "end"
                        break
                        
                    else:
                        vel.angular.z = 0.2
                        self.pub.publish(vel)
                        print self.az - self.yaw, "case 2"
                        print self.yaw
                
                        
            
            elif self.yaw > self.az:

                if self.yaw-self.az > 180:
                    vel.angular.z = 0.2
                    self.pub.publish(vel)
                    print self.yaw - self.az, "case 3"
                    print self.yaw
                    
                elif self.yaw-self.az < 180:

                    if self.yaw-self.az<=1:
                        self.linear = True
                        vel.angular.z = 0
                        self.pub.publish(vel)
                        print "end"
                        break
                       
                    else:
                        vel.angular.z = -0.2
                        self.pub.publish(vel)
                        print self.yaw - self.az, "case 4"
                        print self.yaw
                   


        if self.linear:
            self.linear_rover()

    def linear_rover(self):
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        vel = Twist()
        while not rospy.is_shutdown():
            if(self.distance>0.8):
                vel.linear.x = 0.3
                self.pub.publish(vel)
            else:
                vel.linear.x = 0
                self.pub.publish(vel)
                break
            print self.distance
          

if __name__ == "__main__":
    rospy.init_node('listener')
    robot = Robot()
    robot.orientation_rover()
    rospy.spin()