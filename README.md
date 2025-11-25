# IoT Autonomous Mobile Robot (AMR) with Digital Twin Simulation


## 📖 Project Overview

This project implements a **Distributed Autonomous Mobile Robot System** that integrates a physical differential-drive robot with a PC-based **Digital Twin simulation**.

The system utilizes **Breadth-First Search (BFS)** algorithms to calculate optimal paths in a dynamic environment. It establishes a real-time **TCP/IP Wi-Fi control loop**, synchronizing the virtual simulation (Python Turtle) with the physical hardware (ESP32) via JSON telemetry.

**Academic Context:**
* **Course:** Advanced Programming in Measurement and Control
* **Institution:** VNU University of Engineering and Technology (UET)
* **Advisors:** Dr. Do Tran Thang, M.Sc. Le Duy Minh
* **Authors:** Le Cong Viet Anh, Nguyen Thanh Dat

---

## ⚙️ System Architecture

The architecture follows a **Client-Server model** operating over a dedicated Wi-Fi SoftAP network:

1.  **PC Simulation (Client):**
    * Generates a 6x6 grid map with random static obstacles.
    * Computes the shortest path using **BFS**.
    * Visualizes the trajectory using **Turtle Graphics**.
    * Sends navigation commands via **TCP Sockets**.

2.  **Physical Robot (Server/Edge):**
    * **MCU:** ESP32 acting as a Wi-Fi Access Point (`192.168.4.1`).
    * **Control:** Parses JSON payloads to drive DC motors via L298N.
    * **Feedback:** Uses interrupt-based **Encoder Odometry** to correct heading and distance.
    * **HMI:** Displays real-time coordinates (Row, Col) and Heading ($\theta$) on an LCD.

---

## 🛠 Hardware Specifications

| Component | Model / Specs | Function |
| :--- | :--- | :--- |
| **Microcontroller** | ESP32 DevKit V1 | Central processing & Wi-Fi Host |
| **Motor Driver** | L298N Module | H-Bridge control for 2 motors |
| **Motors** | DC Geared (Ratio 1:100) | High torque drive |
| **Encoders** | Optical (AB Phase) | **1400 pulses/rev** precision odometry |
| **Display** | LCD 1602 (I2C) | Real-time debugging interface |
| **Power** | 3x 18650 Li-ion (12V) | Power supply |
| **Chassis** | Differential Drive | **Track Width:** 12cm, **Wheel Dia:** 4.3cm |

---

## 🚀 Installation & Setup

### 1. Firmware Setup (ESP32)
1.  Install [Thonny IDE](https://thonny.org/) or VS Code (with Pymakr).
2.  Flash the **MicroPython** firmware onto your ESP32.
3.  Upload the contents of the `firmware_esp32/` folder to the board:
    * `boot.py`, `main.py` (Entry points)
    * `xe_config.py` (Kinematics configuration)
    * `motor.py`, `encoder.py`, `lcd.py` (Drivers)
4.  Reset the board. The LCD should light up.

### 2. Software Setup (PC)
1.  Ensure you have **Python 3.x** installed.
2.  No external pip libraries are required (uses standard `socket`, `json`, `turtle`, `math`).

---

## 🎮 Usage Guide (How to Run)

### Step 1: Power the Robot
Switch on the robot's power supply. The ESP32 will initialize and create a Wi-Fi Access Point.
* **SSID:** `ESP32_Robot`
* **Password:** `123456789`
* *LCD Status:* "Waiting for connection..."

### Step 2: Connect PC to Robot Network
On your laptop/PC, disconnect from your current internet and connect to the **`ESP32_Robot`** Wi-Fi network using the password above.

### Step 3: Launch Simulation
Open a terminal in the `simulation_pc` folder and run the script


## 📂 Repository Structure
``` text
├── firmware_esp32/             # SOURCE CODE FOR ROBOT
│   ├── boot.py                 # Bootloader
│   ├── main.py                 # TCP Server & Logic Loop
│   ├── xe_config.py            # Robot Kinematics (Wheel size, PID)
│   ├── encoder.py              # Interrupt-based counting
│   ├── motor.py                # PWM Motor Control
│   └── lcd.py                  # I2C Display Driver
├── simulation_pc/              # SOURCE CODE FOR COMPUTER
│   └── simulation_pc.py         # Main Simulation, BFS & TCP Client
├── docs/                       # DOCUMENTATION
└── README.md                   # Project Documentation
