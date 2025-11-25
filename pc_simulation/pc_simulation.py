'''
1. Chương trình mô phỏng một amr hoạt động với các chức năng chính sau:
    - Hoạt động dựa trên bản đồ được xây dựng trước
    - Tránh vật cản tĩnh và tường trên bản đồ
2. Mô tả chuyển động của 01 amr:
    - Mỗi chu kỳ chuyển động: tìm kiếm tập hợp hướng đi -> chọn hướng đi phù hợp với tập hợp các yêu cầu -> tiến một bước -> quay lại chọn hướng đi
    - Tại một chu kỳ chuyển động amr có thể quay 1 trong 4 hướng (90/đi lên, 180/trái, 0/phải, 270/xuống dưới) ứng với hệ toạ độ oxy
    - Trong một chu kỳ chuyển động amr dịch chuyển một đoạn step theo 1 trong 2 trục x hoặc y
4. Thiết kế chương trình:
4.1. Ý tưởng: 
Mô phỏng hoạt động của một amr trên cùng một bản đồ trong không gian 2D. Thế giới thực là: bản đồ 2D và xe amr theo lập trình thủ tục.
Xe amr là một hệ thống Cơ điện tử gồm:
- Phần cứng: bộ não (máy tính) + cơ cấu chuyển động (xe + bánh).
- Phần mềm: Chương trình phần mềm trong bộ não (máy tính) để điều khiển xe hoạt động.
4.2. Cơ sở dữ liệu:
- Bản đồ thực: hệ tọa độ 2D, vật cản tĩnh tại các tọa độ 2D (tường là trường hợp đặc biệt của vật cản tĩnh và là kích thước của bản đồ).
- Bản đồ ảo trong bộ não (máy tính): Bản đồ ảo được biểu diễn bằng ma trận có các phần tử ứng với các vị trí trên bản đồ thật.
- Các phương thức của bản đồ và chuyển đổi giữa hai bản đồ.
- Cơ sở dữ liệu về amr: thuộc tính và phương thức.
- Tập hợp vị trí và hướng tức thời của amr trên bản đồ ảo.
'''

import turtle
from random import *
from queue import Queue
import socket
import json
import sys

# Địa chỉ IP và cổng của ESP32
HOST = '192.168.4.1'
PORT = 1234

# Tạo socket và kiểm tra kết nối ngay lập tức
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # timeout ngắn để tránh bị treo
    s.connect((HOST, PORT))
    print("Da ket noi voi ESP32.")
except (socket.timeout, socket.error):
    print("Hay ket noi WiFi voi ESP32 truoc khi chay chuong trinh.")
    print("id: ESP32_Robot - pass: 123456789")
    print("Nhan chuot vao cua so de thoat...")
    turtle.Screen().exitonclick()
    sys.exit()
s.settimeout(5)

#Xay dung kien thuc ve ban do
#Hàm khởi tạo bản đồ
def map_init(node_row, node_column):
    map = []
    for row in range(node_row):
            new_row = []
            for col in range(node_column):
                if (row == 0)|(row == node_row - 1)|(col == 0)|(col == node_column - 1):
                    new_node = 1
                else:
                    new_node = 0
                new_row.append(new_node)
            map.append(new_row)
    return map

#Hàm in bản đồ ra terminal (text)
def print_map(map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            print(f' {map[row][col]} ', end='')
        print(f'\n')    

#Hàm vẽ bản đồ trên màn hình turtle (pixel)
def draw_map(map, color, pen, width_half, height_half):
    pen.color(color)
    for row in range(len(map)):
        pen.seth(0)
        pen.up()
        pen.goto(turn2pixel(map, height_half, width_half, row, 0))
        pen.down()
        pen.goto(turn2pixel(map, height_half, width_half, row, len(map[row]) - 1))
    for col in range(len(map[0])):
        pen.seth(-90)
        pen.up()
        pen.goto(turn2pixel(map, height_half, width_half, 0, col))
        pen.down()
        pen.goto(turn2pixel(map, height_half, width_half, len(map) - 1, col))
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] != 0:
                pen.up()
                pen.goto(turn2pixel(map, height_half, width_half, row, col))
                pen.down()
                pen.dot(5, "red")

#Hàm chuyển vị trí phần tử trên bản đồ ma trận thành tọa độ pixel trên bản đồ turtle
def turn2pixel(map, height_half, width_half, row_position, col_position):
    row_segment = len(map) - 1
    col_segment = len(map[0]) - 1
    row_distance = 2 * height_half/row_segment
    col_distance = 2 * width_half/col_segment
    x_pixel = -width_half + col_position * col_distance
    y_pixel = height_half - row_position * row_distance
    return [x_pixel, y_pixel]

#Hàm chuyển vị trí amr trên bản đồ turtle sang vị trí phần tử trên bản đồ ma trận
def turn2node(map, width_half, height_half, x_pixel, y_pixel):
    row_segment = len(map) - 1
    col_segment = len(map[0]) - 1
    row_distance = 2 * height_half/row_segment
    col_distance = 2 * width_half/col_segment
    row_pos = round((height_half - y_pixel)/row_distance)
    col_pos = round((x_pixel + width_half)/col_distance)
    return [row_pos, col_pos]

#Hàm tạo ngẫu nhiên vật cản trên bản đồ ma trận
def map_random(map):
    for row in range(1, len(map) - 1):
        for col in range(1, len(map[row]) - 1):
            obstacle = choice((0, 0, 0, 0, 1 , 1, 0, 0, 0, 0, 0, 0, 0))
            map[row][col] = obstacle

#Hàm chọn ngẫu nhiên 4 điểm không phải tường hoặc vật cản và quy đổi sang vị trí pixel
def select_random_points(map, width_half, height_half):
    valid_points = []
    for row in range(1, len(map) - 1):
        for col in range(1, len(map[row]) - 1):
            if map[row][col] == 0:  # Nếu không phải tường hoặc vật cản
                valid_points.append((row, col))

    # Chọn ngẫu nhiên 4 điểm từ danh sách các điểm hợp lệ
    selected_points = sample(valid_points, 4)
    
    # Quy đổi điểm ma trận thành pixel
    pixel_points = [turn2pixel(map, height_half, width_half, point[0], point[1]) for point in selected_points]
    
    return selected_points, pixel_points

# Hàm vẽ các điểm start, 1, 2 và 3
def draw_points_with_numbers(pixel_points, pen):
    # Vẽ điểm Start
    pen.up()
    pen.goto(pixel_points[0])
    pen.down()
    pen.dot(15, "blue")
    pen.up()
    pen.goto(pixel_points[0][0], pixel_points[0][1] - 10)
    pen.write("Start", align="center", font=("Arial", 14, "bold", "normal"))
    
    # Màu nút 1, 2, 3
    colors = ["red", "green", "yellow"]
    
    # Vẽ các điểm 1, 2, 3
    for i in range(1, len(pixel_points)):
        point = pixel_points[i]
        pen.up()
        pen.goto(point)
        pen.down()
        pen.dot(20, colors[i-1])
        pen.up()
        pen.goto(point[0], point[1] - 5)
        pen.write(str(i), align="center", font=("Arial", 12, "bold"))


#Cơ sở kiến thức về amr
#Vẽ amr trên bản đồ turtle
def draw_amr(map, amr, width_half, height_half, current_ppos):
    amr.up()
    amr.goto(current_ppos)
    current_mpos = turn2node(map, width_half=width_half, height_half=height_half, x_pixel=current_ppos[0], y_pixel=current_ppos[1])
    return current_mpos

# Hàm tìm đường đi ngắn nhất giữa hai điểm bằng BFS với điều kiện không đi qua các điểm bị cấm
def find_path_bfs(map, start, goal, restricted_points=[]):
    # Kích thước bản đồ
    rows, cols = len(map), len(map[0])
    
    # Các hướng di chuyển: Lên, Xuống, Trái, Phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Tạo mảng đánh dấu các ô đã được thăm
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Tạo từ điển để lưu cha của mỗi ô (dùng để truy vết đường đi)
    parent = {}
    
    # Hàng đợi để thực hiện BFS
    queue = Queue()
    queue.put(start)  # Thêm điểm bắt đầu vào hàng đợi
    visited[start[0]][start[1]] = True  # Đánh dấu điểm bắt đầu là đã thăm

    # Thực hiện BFS
    while not queue.empty():
        current = queue.get()  # Lấy ô hiện tại từ hàng đợi
        
        # Nếu đã đến đích, dừng tìm kiếm
        if current == goal:
            break
        
        # Duyệt qua các hướng di chuyển
        for d in directions:
            next_row = current[0] + d[0]
            next_col = current[1] + d[1]
            
            # Kiểm tra xem ô tiếp theo có hợp lệ không
            if (0 <= next_row < rows and 0 <= next_col < cols  # Nằm trong bản đồ
                and not visited[next_row][next_col]            # Chưa được thăm
                and map[next_row][next_col] == 0               # Không phải vật cản
                
                and (next_row, next_col) not in restricted_points):     # Không nằm trong danh sách bị cấm
                queue.put((next_row, next_col))                         # Thêm ô tiếp theo vào hàng đợi
                visited[next_row][next_col] = True                      # Đánh dấu ô này là đã thăm
                parent[(next_row, next_col)] = current                  # Lưu cha của ô này

    # Truy vết đường đi từ đích về điểm bắt đầu
    path = []
    current = goal
    while current != start:
        if current not in parent:  # Nếu không tìm được đường, trả về rỗng
            return []
        path.append(current)
        current = parent[current]
    path.append(start)  # Thêm điểm bắt đầu vào đường đi
    path.reverse()  # Đảo ngược đường đi để có thứ tự từ start -> goal
    return path

# Hàm di chuyển AMR theo đường đi tìm được và quay đầu theo hướng di chuyển
def move_amr_with_path(amr, map, path, width_half, height_half, trajectory, current_state):
    amr.color("green")
    amr.pensize(3)
    amr.down()
    for i in range(len(path) - 1):
        
        print("Vi tri: ", current_state["position"])
        print("Huong: ", current_state["heading"]) 
        
        # Lấy tọa độ nút hiện tại và nút tiếp theo
        current_node = path[i]
        next_node = path[i + 1]
        
        # Tính toán hướng di chuyển
        delta_row = next_node[0] - current_node[0]
        delta_col = next_node[1] - current_node[1]
        
        # Xác định lệnh điều khiển và hướng di chuyển
        if delta_row == -1 and delta_col == 0:  # Đi lên
            amr.setheading(90)
            current_state["heading"] = 90
            command = "turn 90"
        elif delta_row == 1 and delta_col == 0:  # Đi xuống
            amr.setheading(270)
            current_state["heading"] = 270
            command = "turn 270"
        elif delta_row == 0 and delta_col == -1:  # Đi trái
            amr.setheading(180)
            current_state["heading"] = 180
            command = "turn 180"
        elif delta_row == 0 and delta_col == 1:  # Đi phải
            amr.setheading(0)
            current_state["heading"] = 0
            command = "turn 0"
        
        # Gửi lệnh quay đầu
        data = {'Row': current_state["position"][0],
                'Col': current_state["position"][1],
                'Theta': current_state["heading"],
                'Command': command}
        message = json.dumps(data)
        s.send(message.encode())
        
        # Đợi phản hồi từ ESP32
        response = s.recv(1024).decode()
        if response != "done":
            print("ESP32 khong phan hoi dung, dung chuong trinh.")
            exit()
        
        # Cập nhật vị trí hiện tại
        current_state["position"] = next_node
        
        # Di chuyển đến nút tiếp theo
        pixel_pos = turn2pixel(map, height_half, width_half, next_node[0], next_node[1])
        amr.goto(pixel_pos[0], pixel_pos[1])
        
        # Gửi lệnh đi thẳng
        command = "forward"
        data = {'Row': current_state["position"][0], 'Col': current_state["position"][1], 'Theta': current_state["heading"], 'Command': command}
        message = json.dumps(data)
        s.send(message.encode())
        
        # Đợi phản hồi từ ESP32
        response = s.recv(1024).decode()
        if response != "done":
            print("ESP32 khong phan hoi dung, dung chuong trinh.")
            exit()
        
        # Lưu điểm hiện tại vào quỹ đạo
        trajectory.append(next_node)
        
           
if __name__ == '__main__':
    turtle.mode("world")
    turtle.setworldcoordinates(-410, -710, 410, 710)
    turtle.setup(0.5, 0.5, 100, 100)
    window = turtle.Screen()
    map = map_init(6, 6)  # Tăng kích thước bản đồ
    map_random(map)
    
    one_amr = turtle.Turtle('turtle')
    one_amr.speed(10)
    
    # Vẽ bản đồ
    draw_map(map, 'pink', one_amr, 400, 700)
    
    # Chọn 4 điểm ngẫu nhiên
    selected_points, pixel_points = select_random_points(map, 400, 700)
    
    # Vẽ các điểm trên bản đồ
    draw_points_with_numbers(pixel_points, one_amr)
    
    # Lấy các điểm start, 1, 2, 3
    start, point1, point2, point3 = selected_points
    one_amr.up()
    one_amr.goto(turn2pixel(map, 700, 400, row_position=start[0], col_position=start[1]))
    one_amr.setheading(0)  # Đặt hướng ban đầu (nếu cần)
    
    # Danh sách lưu quỹ đạo đã đi qua
    trajectory = [start]
    
    # Biến lưu trạng thái hiện tại của turtle
    current_state = {
        "position": start,  # Vị trí hiện tại theo ma trận
        "heading": 0        # Hướng hiện tại (0: phải, 90: lên, 180: trái, 270: xuống)
    }
        
    # Tìm đường đi từ start -> 1 -> 2 -> 3
    path1 = find_path_bfs(map, start, point1, restricted_points=[point2, point3])
    if not path1:
        print("Khong tim duoc duong tu Start đen 1")
        # In thông báo trên bản đồ
        one_amr.up()
        one_amr.speed(10)
        one_amr.goto(0, 750)  # Vị trí phía trên bản đồ
        one_amr.color("black")
        one_amr.write("Không tìm được đường từ Start đến 1", align="center", font=("Arial", 16, "bold"))
        window.exitonclick()
        exit()
    one_amr.speed(1)
    move_amr_with_path(one_amr, map, path1, 400, 700, trajectory, current_state)
    
    path2 = find_path_bfs(map, point1, point2, restricted_points=[point3])
    if not path2:
        print("Khong tim duoc duong tu 1 đen 2")
        # In thông báo trên bản đồ
        one_amr.up()
        one_amr.speed(10)
        one_amr.goto(0, 750)  # Vị trí phía trên bản đồ
        one_amr.color("black")
        one_amr.write("Không tìm được đường từ 1 đến 2", align="center", font=("Arial", 16, "bold"))
        window.exitonclick()
        exit()
        
    one_amr.speed(1)
    move_amr_with_path(one_amr, map, path2, 400, 700, trajectory, current_state)
    
    path3 = find_path_bfs(map, point2, point3, restricted_points=[point1])
    if not path3:
        print("Khong tim duoc duong tu 2 đen 3")
        # In thông báo trên bản đồ
        one_amr.up()
        one_amr.speed(10)
        one_amr.goto(0, 750)  # Vị trí phía trên bản đồ
        one_amr.color("black")
        one_amr.write("Không tìm được đường từ 2 đến 3", align="center", font=("Arial", 16, "bold"))
        window.exitonclick()
        exit()

    one_amr.speed(1)
    move_amr_with_path(one_amr, map, path3, 400, 700, trajectory, current_state)
    
    # In quỹ đạo đã đi qua ra terminal
    print("Quy dao da di qua:")
    for point in trajectory:
        print(point)
    
    # In trạng thái cuối cùng của turtle
    print(f"Vi tri cuoi cung cua turtle: {current_state['position']}")
    print(f"Huong cuoi cung cua turtle: {current_state['heading']} do")
    # Gửi dữ liệu
    data = {'Row': current_state["position"][0], 'Col': current_state["position"][1], 'Theta': current_state["heading"]}
    message = json.dumps(data)
    s.send(message.encode())
    
    # Hiển thị quỹ đạo trên bản đồ
    one_amr.up()
    one_amr.speed(10) 
    one_amr.goto(0, 750)  # Vị trí phía trên bản đồ
    one_amr.color("black")
    one_amr.write(f"Quỹ đạo: {trajectory}", align="center", font=("Arial", 12, "bold"))
    one_amr.goto(turn2pixel(map, 700, 400, row_position=current_state["position"][0], col_position=current_state["position"][1]))

    window.exitonclick()
    # Đóng kết nối
    s.close()