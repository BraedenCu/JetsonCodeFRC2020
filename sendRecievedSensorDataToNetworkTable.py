import rospy
from std_msgs.msg import String
import threading
from networktables import NetworkTables

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.80.29.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

print('connected')

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

    rospy.init_node('sendDataToNetworkTable', anonymous=True)

    rospy.Subscriber("ULTRASONIC1", String, callback)
    rospy.Subscriber("ULTRASONIC2", String, callback)
    rospy.Subscriber("ULTRASONIC3", String, callback)

    rospy.Subscriber("IMU", String, callback)

	table = NetworkTables.getTable('datatable')

    table.putNumber('IMU', 3)
    table.putNumber('ULTRASONIC1', 1)
    table.putNumber('ULTRASONIC2', 2)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
