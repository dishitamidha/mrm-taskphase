#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math
def circle():
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
    rospy.init_node('circle', anonymous = True)
    print "Turtlesim moving in a circle"
    move = Twist()
    speed_l = 2
    speed_a = 1
    radius = speed_l/speed_a
    move.linear.x = speed_l
    move.linear.y = 0
    move.linear.z = 0
    move.angular.x = 0
    move.angular.y = 0
    move.angular.z = speed_a

    circumference = 2 * math.pi * (radius)

    

    rate = rospy.Rate(1000)
    

    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()

        current = 0

        while(current < circumference):

             pub.publish(move)
             t1 = rospy.Time.now().to_sec()
             current = radius * (t1-t0) * speed_a
             
            
    
        move.linear.x = 0
        move.angular.z = 0
        pub.publish(move)

        rate.sleep()
       



if __name__ == '__main__':
    try:
        circle()
    except rospy.ROSInterruptException:
        pass

    




    
    
    


