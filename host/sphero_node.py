from sphero_sprk import Sphero
import rospy
from geometry_msgs.msg import Point, Twist, Vector3Stamped, PointStamped
from std_msgs.msg import Bool, Int16, ColorRGBA

class SpheroNode(object):

    def __init__(self, name = "sphero", addr=None):
        self._name = name
        self._addr = addr

        self._orb = Sphero(addr)
        self._connected = False

    def connect(self, addr):
        self._orb.connect(addr)
        orb = self._orb.get_device_name()
        print("Connected to: " + orb['name'])
        rospy.loginfo("Connected to: " + orb['name'])

        version = self._orb.version()
        print("Model: " + str(version['MDL']) + " HW Version: "+str(version['HW']))
        print("App Version: " + str(version['MSA-ver']) + "." + str(version['MSA-rev']))
        print("Firmware Version: " + str(version['BL']))

        rospy.loginfo("Model: " + str(version['MDL']) + " HW Version: " + str(version['HW']))
        rospy.loginfo("App Version: " + str(version['MSA-ver']) + "." + str(version['MSA-rev']))
        rospy.loginfo("Firmware Version: " + str(version['BL']))

        self._connected = True

    def cmd_vel(self, twist):
        if(not self._connected):
            return

        self._orb.roll(int(twist.linear.x), int(twist.angular.z))

    def set_color(self, color):
        if(not self._connected):
            return

        self._orb.set_rgb_led(int(color.r), int(color.g), int(color.b))

    def set_heading(self, heading):
        if(not self._connected):
            return

        self._orb.set_heading(heading.data)

    def init_ros(self):
        rospy.init_node(self._name, anonymous=True)

        topic_root = '/'+self._name

        # Subscriptions
        sub_cmd_vel = rospy.Subscriber(topic_root + '/cmd_vel', Twist, self.cmd_vel, queue_size=1)
        sub_color   = rospy.Subscriber(topic_root + '/set_color', ColorRGBA, self.set_color, queue_size=1)
        sub_heading = rospy.Subscriber(topic_root + '/set_heading', Int16, self.set_heading, queue_size=1)

        # Publishables
        self.pub_odometry = rospy.Publisher(topic_root + '/odometry', PointStamped, queue_size=1)
        self.pub_accel = rospy.Publisher(topic_root + '/accel', PointStamped, queue_size=1)
        self.pub_imu = rospy.Publisher(topic_root + '/imu', PointStamped, queue_size=1)
        self.pub_gyro = rospy.Publisher(topic_root + '/gyro', PointStamped, queue_size=1)

    def pub_accel_data(self, data):
        ps = PointStamped()
        ps.header.stamp = rospy.Time.now()
        ps.point.x = data['x']
        ps.point.y = data['y']
        ps.point.z = data['z']
        self.pub_accel.publish(ps)


    def pub_imu_data(self, data):
        ps = PointStamped()
        ps.header.stamp = rospy.Time.now()
        ps.point.x = data['x']
        ps.point.y = data['y']
        ps.point.z = data['z']
        self.pub_imu.publish(ps)

    def pub_gyro_data(self, data):
        ps = PointStamped()
        ps.header.stamp = rospy.Time.now()
        ps.point.x = data['x']
        ps.point.y = data['y']
        ps.point.z = data['z']
        self.pub_gyro.publish(ps)

    def pub_odom_data(self, data):
        ps = PointStamped()
        ps.header.stamp = rospy.Time.now()
        ps.point.x = data['x']
        ps.point.y = data['y']
        self.pub_odometry.publish(ps)

    def setup_publishables(self):
        self._orb.start_accel_callback(rate=10, callback=self.pub_accel_data)
        #self._orb.start_IMU_callback(rate=10, callback=self.pub_imu_data)
        #self._orb.start_gyro_callback(rate=10, callback=self.pub_gyro_data)
        self._orb.start_odometry_callback(rate=10, callback=self.pub_odom_data)

    def my_ping(self, last_call):
        self._orb.ping()

    def main(self):
        self.connect(self._addr)
        self.init_ros()

        self.setup_publishables()

        heartbeat = rospy.Timer(rospy.Duration(10), self.my_ping)

        rate = rospy.Rate(40)  # Hz
        while not rospy.is_shutdown():
            rate.sleep()

if(__name__ == "__main__"):
    #s = SpheroNode(addr="E7:D7:34:B0:4B:DB")
    s = SpheroNode(addr="DC:79:91:5A:9B:92")
    s.main()