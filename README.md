# esp32-autonomous-mobile-robot
Autonomous Mobile Robot (AMR) system featuring ESP32 MicroPython firmware, BFS pathfinding simulation, and Digital Twin synchronization via TCP/IP.
# IoT Autonomous Mobile Robot (AMR) System with Digital Twin

## 🚀 Project Overview
This project involves the engineering of a distributed autonomous mobile robot system. It integrates a physical **differential drive robot** (powered by ESP32) with a **PC-based simulation** (Digital Twin). The system utilizes **Breadth-First Search (BFS)** algorithms for pathfinding and synchronizes telemetry data in real-time over a local Wi-Fi network.

## 🛠 Tech Stack
* **Firmware:** MicroPython (ESP32), OOP-based Driver Architecture.
* **Simulation & Host:** Python 3, Turtle Graphics, Socket Programming.
* **Communication:** TCP/IP over Wi-Fi (SoftAP Mode), JSON Serialization.
* **Hardware:** ESP32 SoC, DC Motors (H-Bridge), Optical Encoders (1400 PPR), I2C LCD 1602.

## ✨ Key Features
* **Path Planning:** Implements BFS algorithm on a 6x6 grid to calculate collision-free paths dynamically.
* **Real-Time Telemetry:** Bi-directional communication with sub-100ms latency to visualize robot state (Position, Heading) on the PC simulation.
* **Precision Control:** Closed-loop motion control using interrupt-based quadrature encoder feedback for precise odometry and kinematic correction.
* **Hardware Abstraction:** Modular driver implementation for Motors, LCDs, and Encoders.

## 📂 Project Structure
```text
├── pc_simulation/
│   ├── Bai_thi_2025.py   # Main simulation & BFS logic
├── esp32_firmware/
│   ├── main.py           # Main control loop & TCP Server
│   ├── xe_config.py      # Robot kinematics & PID settings
│   ├── encoder.py        # Interrupt-based encoder driver
│   ├── motor.py          # PWM motor control
│   └── lcd.py            # I2C display driver
└── README.md
