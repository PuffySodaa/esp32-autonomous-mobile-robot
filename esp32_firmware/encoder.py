from machine import Pin

class Encoder:
    def __init__(self, pin_a, pin_b):
        self.pinA = Pin(pin_a, Pin.IN)
        self.pinB = Pin(pin_b, Pin.IN)
        self.position = 0

        self.lastA = self.pinA.value()
        self.lastB = self.pinB.value()

        # Ngắt trên cả A và B để tránh lỡ xung
        self.pinA.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)
        self.pinB.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)

    def callback(self, pin):
        a_state = self.pinA.value()
        b_state = self.pinB.value()

        delta = (self.lastA ^ b_state) - (self.lastB ^ a_state)
        self.position += delta

        self.lastA = a_state
        self.lastB = b_state

    def get_position(self):
        return self.position

    def reset(self):
        self.position = 0
