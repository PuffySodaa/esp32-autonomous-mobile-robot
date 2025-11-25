from machine import Pin, PWM

class Motor:
    def __init__(self, in1, in2, en, pwm_freq=1000):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.en = PWM(Pin(en), freq=pwm_freq)
        self.en.duty(0)  # Đảm bảo rằng động cơ bắt đầu với tốc độ 0

    def set_speed(self, speed):
        """Điều khiển động cơ với tốc độ từ -100 đến 100"""
        if speed > 0:
            self.in1.on()
            self.in2.off()
        elif speed < 0:
            self.in1.off()
            self.in2.on()
        else:
            self.stop()

        self.en.duty(int(min(abs(speed), 100) * 10.23))

    def stop(self):
        self.in1.off()
        self.in2.off()
        self.en.duty(0)
