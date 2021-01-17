#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math
def circle():
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
    rospy.init_node('circle', anonymous = True)
    print "Turtlesim moving in a circle"
    move = Twist()
    speed_l = 4
    speed_a = 2
    radius = speed_l/speed_a
    move.linear.x = speed_l
    move.linear.y = 0
    move.linear.z = 0
    move.angular.x = 0
    move.angular.y = 0
    move.angular.z = speed_a
    

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        pub.publish(move)
        rate.sleep()



if __name__ == '__main__':
    try:
        circle()
    except rospy.ROSInterruptException:
        pass

    




    
    
    


