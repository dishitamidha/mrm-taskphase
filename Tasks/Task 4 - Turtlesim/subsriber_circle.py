#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x = 0
y = 0
theta = 0

def callback(data):
    global x, y, theta
    x = data.x
    y = data.y
    theta = data.theta
 
    print "Here are the coordinates of this instance"
    print "x:", x
    print "y:", y
    print "theta:", theta
    print "--------"

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/turtle1/pose', Pose, callback)
    
    rospy.spin()

if __name__ == '__main__':
    listener()
