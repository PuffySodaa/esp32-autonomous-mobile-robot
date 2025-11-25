import network
import socket
import time
import json
from xe_config import XeTuHanh

xe = XeTuHanh()
xe.set_motor_speed(0, 0)

# Khởi tạo Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32_Robot', password='123456789')
print("Dang phat WiFi...")

ip_address = ap.ifconfig()[0]
print("Dia chi IP cua ESP32:", ip_address)

# Khởi tạo server socket
HOST = ip_address
PORT = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
s.settimeout(None)

print("Dang cho ket noi tu may tinh...")

def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Ngắt kết nối
            try:
                decoded_data = data.decode().strip()
                data_dict = json.loads(decoded_data)

                # Hiển thị lên LCD
                xe.lcd.clear()
                xe.lcd.move_to(0, 0)
                xe.lcd.putstr("Row: " + str(data_dict["Row"]) + " Col: " + str(data_dict["Col"]))
                xe.lcd.move_to(0, 1)
                xe.lcd.putstr("Theta: " + str(data_dict["Theta"]))

                # Xử lý lệnh
                cmd = data_dict["Command"]
                if cmd == "forward":
                    xe.move_forward(20)
                elif cmd.startswith("turn"):
                    target_angle = int(cmd.split()[1])
                    xe.rotate(target_angle)

                conn.send("done".encode())
            except Exception as e:
                print("Loi xu ly du lieu:", e)
            time.sleep(0.1)
    except Exception as e:
        print("Loi ket noi:", e)
    finally:
        conn.close()
        print("Mat ket noi voi may tinh.")

while True:
    try:
        conn, addr = s.accept()
        print("Da ket noi tu:", addr)
        handle_client(conn)
    except Exception as e:
        print("Loi khi chap nhan ket noi:", e)
