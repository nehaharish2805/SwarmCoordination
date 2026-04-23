import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class Follower(Node):
    def __init__(self):
        super().__init__('follower')

        # Leader pose
        self.leader_x = 0.0
        self.leader_y = 0.0
        self.leader_yaw = 0.0

        # Robot 2 pose
        self.r2_x = 0.0
        self.r2_y = 0.0
        self.r2_yaw = 0.0

        # Robot 3 pose
        self.r3_x = 0.0
        self.r3_y = 0.0
        self.r3_yaw = 0.0

        # Subscribers
        self.create_subscription(Odometry, '/robot1/odom', self.leader_cb, 10)
        self.create_subscription(Odometry, '/robot2/odom', self.r2_cb, 10)
        self.create_subscription(Odometry, '/robot3/odom', self.r3_cb, 10)

        # Publishers
        self.pub2 = self.create_publisher(Twist, '/robot2/cmd_vel', 10)
        self.pub3 = self.create_publisher(Twist, '/robot3/cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.control_loop)

    # -------------------------
    # Quaternion → yaw
    # -------------------------
    def get_yaw(self, q):
        siny = 2 * (q.w * q.z + q.x * q.y)
        cosy = 1 - 2 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny, cosy)

    def wrap_angle(self, a):
        return math.atan2(math.sin(a), math.cos(a))

    # -------------------------
    # Callbacks
    # -------------------------
    def leader_cb(self, msg):
        self.leader_x = msg.pose.pose.position.x
        self.leader_y = msg.pose.pose.position.y
        self.leader_yaw = self.get_yaw(msg.pose.pose.orientation)

    def r2_cb(self, msg):
        self.r2_x = msg.pose.pose.position.x
        self.r2_y = msg.pose.pose.position.y
        self.r2_yaw = self.get_yaw(msg.pose.pose.orientation)

    def r3_cb(self, msg):
        self.r3_x = msg.pose.pose.position.x
        self.r3_y = msg.pose.pose.position.y
        self.r3_yaw = self.get_yaw(msg.pose.pose.orientation)

    # -------------------------
    # FOLLOW LOGIC (STABLE VERSION)
    # -------------------------
    def follow(self, fx, fy, fyaw, offset_x, offset_y):

        # Transform offset from leader frame → world frame
        target_x = self.leader_x + offset_x * math.cos(self.leader_yaw) - offset_y * math.sin(self.leader_yaw)
        target_y = self.leader_y + offset_x * math.sin(self.leader_yaw) + offset_y * math.cos(self.leader_yaw)

        dx = target_x - fx
        dy = target_y - fy

        distance = math.sqrt(dx * dx + dy * dy)
        desired_angle = math.atan2(dy, dx)

        angle_error = self.wrap_angle(desired_angle - fyaw)

        msg = Twist()

        # -------------------------
        # SIMPLE STABLE CONTROL
        # -------------------------

        # Step 1: rotate toward target
        if abs(angle_error) > 0.3:
           msg.angular.z = 0.6 if angle_error > 0 else -0.6
           msg.linear.x = 0.0

        # Step 2: move forward (fast)
        elif distance > 0.5:
           msg.linear.x = 0.12
           msg.angular.z = 0.0

        # Step 3: fine adjustment (slow)
        elif distance > 0.3:
           msg.linear.x = 0.05
           msg.angular.z = 0.0   # 🔥 IMPORTANT ADD

        # Step 4: stop
        else:
           msg.linear.x = 0.0
           msg.angular.z = 0.0
        
        return msg
    # -------------------------
    def control_loop(self):

        msg2 = self.follow(self.r2_x, self.r2_y, self.r2_yaw, -0.7, 0.0)
        msg3 = self.follow(self.r3_x, self.r3_y, self.r3_yaw, -1.4, 0.0)

        self.pub2.publish(msg2)
        self.pub3.publish(msg3)


def main():
    rclpy.init()
    node = Follower()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
