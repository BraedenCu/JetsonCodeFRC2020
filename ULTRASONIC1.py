import time
import board
import busio
import adafruit_vcnl4010
import rospy
from std_msgs.msg import String
 
# Initialize I2C bus and VCNL4010 module.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vcnl4010.VCNL4010(i2c)
 
# You can also adjust the measurement frequency for the sensor.  The default
# is 390.625 khz, but these values are possible to set too:
# - FREQUENCY_3M125: 3.125 Mhz
# - FREQUENCY_1M5625: 1.5625 Mhz
# - FREQUENCY_781K25: 781.25 Khz
# - FREQUENCY_390K625: 390.625 Khz (default)
#sensor.frequency = adafruit_vcnl4010.FREQUENCY_3M125  # 3.125 Mhz

def findDistance1():

    pub = rospy.Publisher('sendDataToNetworkTable', String, queue_size=10)
    rospy.init_node('ULTRASONIC1', anonymous=True)

    proximity = sensor.proximity  
    #print('Proximity: {0}'.format(proximity))
    ambient_lux = sensor.ambient_lux
    #print('Ambient light: {0} lux'.format(ambient_lux))

    rate = rospy.Rate(10) # 10hz

    rospy.loginfo(proximity)
    pub.publish(proximity)
    rate.sleep()


if __name__ == '__main__':
    try:
        findDistance1()
    except rospy.ROSInterruptException:
        pass
