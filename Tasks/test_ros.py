#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix, Imu
import time
from haversine import haversine
import pyproj
from tf.transformations import euler_from_quaternion
import numpy as np
from geometry_msgs.msg import Twist

class Robot():
    def __init__(self):
        self.gps_int = 0
        self.gps_int_longitude = 0
        self.gps_int_latitude = 0
        self.imu_int = 0
        self.imu_int_x = 0
        self.imu_int_y = 0
        self.imu_int_z = 0
        self.imu_int_w = 0
        self.az12_new = 0
        self.yaw_new = 0
        self.yaw_current = 0
        self.rate = 0
        self.distance = 0
        self.current_distance = 0
        self.latitude_goal = 49.9001340641 #49.8998445724
        self.longitude_goal = 8.9000669039 #8.90010067972 
        self.sub_gps = rospy.Subscriber('/group_task2/fix', NavSatFix, self.gps)
        self.sub_imu = rospy.Subscriber('/group_task2/imu', Imu, self.imu)
        
    
    def gps(self, data_current):
        self.gps_int = data_current
        self.gps_int_latitude = data_current.latitude
        self.gps_int_longitude = data_current.longitude
        self.sub_gps.unregister()

    def imu(self,data_current):
        self.imu_int = data_current
        self.imu_int_x = data_current.orientation.x
        self.imu_int_y = data_current.orientation.y
        self.imu_int_z = data_current.orientation.z
        self.imu_int_w = data_current.orientation.w
        imu  = np.array([self.imu_int_x, self.imu_int_y, self.imu_int_z, self.imu_int_w])
        self.sub_imu.unregister()
        imu_euler = euler_from_quaternion(imu)
        yaw = imu_euler[2]
        yaw = np.degrees(yaw)
        
        #calculating azimuth angles and distance
        x = self.calc_az()
        az12 = x[0]
        az21 = x[1]
        self.distance = x[2]
        print self.distance
     
        
        #changing range of yaw and azimuth to 0 to 360 degrees
        az12 = self.change_range(az12)
        yaw = self.change_range(yaw)

        self.az12_new = az12
        self.yaw_new = yaw
    
        print self.yaw_new, self.az12_new

        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10) 
        vel = Twist()

        #orientation 
        if self.az12_new > self.yaw_new: #if az>yaw
            #case1: if difference between yaw and az > 180, move anticlockwise to cover shortest angle
            if self.az12_new-self.yaw_new > 180:
                
                vel.angular.z = -1
                while not rospy.is_shutdown():
                    self.yaw_current = self.yaw_new
                    while (360-(self.az12_new-self.yaw_current)>5):
                        print self.yaw_current
                        pub.publish(vel)
                        sub = rospy.Subscriber('/group_task2/imu', Imu, self.case)
                        self.rate.sleep()
                    vel.angular.z = 0
                    pub.publish(vel)
                    break

            #case2: if difference between yaw and az < 180, move clockwise to cover shortest angle
      
            elif self.az12_new-self.yaw_new < 180:
                
                vel.angular.z = 1
                while not rospy.is_shutdown():
                    self.yaw_current = self.yaw_new

                    while (self.az12_new-self.yaw_current>5):
                        print self.yaw_current
                        pub.publish(vel)
                        sub = rospy.Subscriber('/group_task2/imu', Imu, self.case)
                        self.rate.sleep()
                    vel.angular.z = 0
                    pub.publish(vel)
                    break

   
        if self.yaw_new > self.az12_new: #if yaw>az
           #case3: if difference between yaw and az > 180, move clockwise to cover shortest angle
            if self.yaw_new-self.az12_new > 180:
                
                vel.angular.z = 1
                while not rospy.is_shutdown():
                    self.yaw_current = self.yaw_new
                    while (360-(self.yaw_current-self.az12_new)>5):
                        print self.yaw_current
                        pub.publish(vel)
                        sub = rospy.Subscriber('/group_task2/imu', Imu, self.case)
                        self.rate.sleep()
                        
                    vel.angular.z = 0
                    pub.publish(vel)
                    break
            #case4: if difference between yaw and az < 180, move anticlockwise to cover shortest angle
  
            elif self.yaw_new-self.az12_new < 180:
                
                vel.angular.z = -1
                while not rospy.is_shutdown():
                    self.yaw_current = self.yaw_new
                    while (self.yaw_current-self.az12_new>5):
                        print self.yaw_current
                        pub.publish(vel)
                        sub = rospy.Subscriber('/group_task2/imu', Imu, self.case)
                        self.rate.sleep()
                        
                    vel.angular.z = 0
                    pub.publish(vel)
                    break

        #linear movement
        pub1 = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        vel1 = Twist()
        vel1.linear.x = 1
        while not rospy.is_shutdown():
            self.current_distance = self.distance 
            while (self.current_distance<=self.distance):
                pub1.publish(vel1)
                sub_dist = rospy.Subscriber('/group_task2/fix', NavSatFix, self.case_dist)
                if self.current_distance <= 5:
                    break
                print self.current_distance
                self.rate.sleep()
            vel.linear.x = 0
            pub1.publish(vel1)
            break

    def calc_az(self):
        g = pyproj.Geod(ellps='WGS84')
        x = g.inv(self.gps_int_longitude, self.gps_int_latitude, self.longitude_goal, self.latitude_goal)
        return x
    
    def change_range(self, y):
        if y<0:
            y = y + 360 
            return y
        else: 
            return y
   
        
    def case(self, data_current):
        x = data_current.orientation.x
        y = data_current.orientation.y
        z = data_current.orientation.z
        w = data_current.orientation.w
        imu_current  = np.array([x, y, z, w])

        imu_euler_current = euler_from_quaternion(imu_current)
        self.yaw_current = np.degrees(imu_euler_current[2])
        self.yaw_current = self.change_range(self.yaw_current)

 
    def case_dist(self, data_dist):
        self.current_lat = data_dist.latitude
        self.current_long = data_dist.longitude
        g = pyproj.Geod(ellps='WGS84')
        x = g.inv(self.longitude_goal, self.latitude_goal, self.current_long, self.current_lat)
        self.current_distance = x[2]
        print self.current_distance

        
if __name__ == "__main__":
    rospy.init_node('listener')
    Robot()
    rospy.spin()