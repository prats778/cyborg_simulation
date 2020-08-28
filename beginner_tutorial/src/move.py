import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import cv2 as cv

class Listener:
    def __init__(self):
        rospy.init_node('listener')
        self.sub = rospy.Subscriber('/camera/image_raw',Image,self.callback)
        self.pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate = rospy.Rate(1)
        self.msg=Twist()
        self.bridge=CvBridge()
    
    def callback(self,data):
        try:
            cv_image=self.bridge.imgmsg_to_cv2(data, 'bgr8')
            self.perform(cv_image)
            k=cv.waitKey()
            self.msg.linear.x=0
            self.msg.linear.y=0
            self.msg.linear.z=0

            self.msg.angular.x=0
            self.msg.angular.y=0
            self.msg.angular.z=0
            #to move bot in forward direction
            if k==ord('w'):
                self.msg.linear.x=self.msg.linear.x+0.5
            #to rotate the bot
            if k==ord('d'):
                self.msg.angular.z=self.msg.angular.z+1

            self.pub.publish(self.msg)
            self.rate.sleep()
        except CvBridgeError as e:
            print(e)

    def perform(self,img):
        cv.imshow('img_receive',img)
        cv.waitKey(1)
           
if __name__ == '__main__':
    listener=Listener()
    try:
        #Testing our function
        rospy.spin()

    except rospy.ROSInterruptException as e:
        print(e)