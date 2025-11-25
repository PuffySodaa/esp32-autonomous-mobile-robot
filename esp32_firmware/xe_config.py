import math
from motor import Motor
from encoder import Encoder
import time
from lcd import LCD

# Định nghĩa cấu hình xe
class XeTuHanh:
    def __init__(self):
        # Khởi tạo các động cơ, encoder và cảm biến
        self.left_motor = Motor(in1=22, in2=21, en=23)
        self.right_motor = Motor(in1=25, in2=26, en=32)
        self.left_encoder = Encoder(pin_a=17, pin_b=16)
        self.right_encoder = Encoder(pin_a=35, pin_b=34)
        self.lcd = LCD(sda=18,scl=19)
        
        # Khởi tạo các thông tin vị trí và trạng thái
        self.x = 0  # Vị trí X
        self.y = 0  # Vị trí Y
        self.theta = 0  # Góc quay (hướng xe)
        self.speed = 25  # Tốc độ mặc định
                    
        # Thông số vật lý của động học xe
        self.track_width_cm = 12  # khoảng cách 2 bánh xe (cm)
        self.pulses_per_revolution = 1400  # số xung của encoder cho 1 vòng quay
        self.wheel_diameter_cm = 4.3 # (cm)

    # Đặt tốc độ
    def set_motor_speed(self, left_speed, right_speed):
        """Điều khiển tốc độ của hai động cơ"""
        self.left_motor.set_speed(left_speed*0.95)
        self.right_motor.set_speed(right_speed*1.05)

    
    def reset_encoders(self):
        """Đặt lại giá trị encoder"""
        self.left_encoder.reset()
        self.right_encoder.reset()


    def get_average_encoder_pulses(self):
        """Lấy số xung trung bình từ hai encoder"""
        left_pulses = self.left_encoder.get_position()
        right_pulses = self.right_encoder.get_position()
        return ((abs(left_pulses) + abs(right_pulses)) / 2)


    def move_forward(self, distance):
        pulses_needed = int((distance / (self.wheel_diameter_cm * 3.14159)) * self.pulses_per_revolution)
        self.reset_encoders()
        self.set_motor_speed(self.speed, self.speed)

        while self.get_average_encoder_pulses() < pulses_needed:
            time.sleep(0.01)

        self.set_motor_speed(-10, -10)
        time.sleep(0.1)
        self.set_motor_speed(0, 0)

    # Quay tới góc mục tiêu
    def rotate(self, target_angle):
        """
        Quay xe tới góc mục tiêu (target_angle).
        Góc mục tiêu được tính theo hệ tọa độ 0-360 độ.
        """
        # Tính toán góc cần quay
        delta_angle = (target_angle - self.theta) % 360
        if delta_angle > 180:
            delta_angle -= 360  # Chọn góc quay ngắn hơn (quay ngược chiều kim đồng hồ)

        # Tính toán khoảng cách bánh xe cần di chuyển
        wheel_circumference = self.track_width_cm * 3.14159
        distance_per_wheel = (delta_angle / 360) * wheel_circumference
        pulses_needed = int((distance_per_wheel / (self.wheel_diameter_cm * 3.14159)) * self.pulses_per_revolution)

        # Đặt lại encoder và bắt đầu quay
        self.reset_encoders()
        if delta_angle < 0:
            self.set_motor_speed(self.speed, -self.speed)  # Quay phải
        else:
            self.set_motor_speed(-self.speed, self.speed)  # Quay trái

        # Quay cho đến khi đạt đủ số xung cần thiết
        while self.get_average_encoder_pulses() < abs(pulses_needed):
            time.sleep(0.01)

        # Dừng động cơ
        self.left_motor.stop()
        self.right_motor.stop()

        # Cập nhật góc quay hiện tại
        self.theta = target_angle % 360