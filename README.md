# 3ID - Future Engineer 
## Performance Video in National Round (Cambodia)
Open Round Video: **https://youtube.com/shorts/tUXS3P6ZWww**

Obstacle Round Video: **https://youtube.com/shorts/n_JYVOY8L6s**
## Team Members
* Chea Vitou, 6023010001@camtech.edu.kh
* Saroeun Norakvitou, 6023030003@camtech.edu.kh
* Visal Phumint, Phumint1969@gmail.com 
## Coach
* Sea Sokchamroeun, 6023010027@camtech.edu.kh
---
# Hardware
<table>
  <tr>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/robot_iso.jpg" width="200" alt="Ackermann Steering Mechanism"/>
      <br>
      Robot Iso View
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/robot_bottom.jpg" width="200" alt="Differential Gearbox"/>
      <br>
      Robot Bottom View
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/robot_top.jpg" width="200" alt="Differential Gearbox"/>
      <br>
      Robot Top View
    </td>
  </tr>
</table>

## Mobility Management - Rear-wheel drive system with Ackermann steering

+ Drivetrain: The robot uses a rear-wheel drive system powered by a single geared DC motor.
+ Differential: Power is transmitted through a central differential gearbox to the rear wheels, allowing them to spin at different speeds during turns.
+ Steering: An Ackermann steering system, actuated by a single hobby servo, controls the front wheels.
+ Motion: This combination mimics car-like motion for smooth, precise turns and reduced tire slip.
+ Chassis: The chassis is a custom 3D-printed structure designed for optimal stability, weight distribution, and component mounting.
+ Documentation: The project documentation covers motor selection, implementation, chassis design, engineering principles (speed, torque, power), assembly instructions, and includes references to 3D CAD files.

<table>
  <tr>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/ackermann_turning.png" width="200" alt="Ackermann Steering Mechanism"/>
      <br>
      Ackerman Steering Mechanism
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/diff_gearbox.jpg" width="200" alt="Differential Gearbox"/>
      <br>
      Differential Gearbox
    </td>
  </tr>
</table>

## Chassis Design and Selection - 3D Printing

The chassis is a custom 3D-printed structure, designed to support the Ackerman steering and differential drive system. It is lightweight yet rigid. 
The chassis and parts are printed mostly with PLA  but parts that require high durability, like motor shaft, are printed with ABS.

Google Drive Link to CAD Models and Parts STLS: https://drive.google.com/drive/folders/1KM2BjuHMXqjhYWxJgh39tXH3upUK1R4r

## Component Selection
+ Microprocessor: Raspberry Pi4
  * This is a powerful, low-cost computer perfect for running the robot's control system and processing camera data for tasks like object detection.
+ Rear Drive: JGB37-520 encoder gear motor
  * The motor's gearbox provides the torque needed to move the robot. Though not used for this project at the moment, the encoder allows for precise speed and position control.
+ Steering: SG92R Steering Servo Motor
  * This small, affordable servo provides the precise angular control required for the Ackermann steering mechanism. Initially we used the infamous sg90s but the plastic gear broke so we switched to a more durable servo.
+ Sensor: 8 MP Autofocus USB 2.0 Camera
  * The high-resolution camera with autofocus is ideal for computer vision tasks, such as navigation and object recognition. However, this camera FOV is too narrow, limiting robot's capabilities :(.

## Power and Sense Management Overview

The autonomous robot is designed to navigate various challenges using a Raspberry Pi 4B as the central processing unit, powered by a 3S LiPo battery (11.1 V, 2200 mAh). The system integrates a camera for vision-based navigation, a DC motor with an encoder for locomotion, a servo for actuation, and a motor driver for motor control. A buck converter steps down the battery voltage to meet the power requirements of various components. This section details the power distribution, sensor selection, their integration, and power consumption considerations, along with a professional wiring diagram and Bill of Materials (BOM).

---

## Power Management

The power system is designed to efficiently distribute power from a single 3S LiPo battery (11.1 V, 2200 mAh) to all components while ensuring voltage compatibility and minimizing power loss. The key components and their power requirements are:

- Raspberry Pi 4B: Requires 5 V at 3 A for stable operation. Powered via a buck converter to step down the 11.1 V battery voltage to 5 V.  
- Servo: Operates at 6 V, typically drawing 0.5–1 A under load. Powered through the same buck converter with an adjusted output or a separate regulator to provide 6 V.  
- DC Motor and Motor Driver: Requires 12 V, with the motor driver handling currents up to 5 A (depending on load). Directly powered from the 11.1 V battery, as it is within the operational range of the motor driver.  
- Camera: Operates at 5 V, drawing 160–260 mA. Powered directly from the Raspberry Pi’s USB port, leveraging the Pi’s 5 V rail.  
- Button: A simple push-button switch for power control or emergency stop, negligible power consumption.  

---

## Power Distribution

A buck converter is used to step down the 11.1 V battery voltage to 5 V and 6 V to meet the requirements of the Raspberry Pi and servo, respectively. The motor driver and DC motor are powered directly from the battery, as their voltage requirements align closely with the 11.1 V nominal voltage of the 3S LiPo battery. To ensure safety and efficiency:

- The buck converter is selected for high efficiency (> 90 %) to minimize energy loss.  
- A fuse (e.g., 10 A) is included at the battery output to protect against short circuits or overcurrent conditions.  
- Proper wire gauges (e.g., AWG 18 for high-current paths to the motor driver, AWG 22 for low-current paths like the camera) are used to minimize voltage drops and heat generation.  

---

## Sensor Selection and Usage

The robot relies primarily on a camera for environmental sensing, with an attempted integration of a LiDAR module that was ultimately abandoned due to integration challenges.

### Camera

- Type: USB camera (Operating Voltage: 5 V, Current: 160–260 mA).  
- Purpose: Provides visual data for navigation, obstacle detection, and path planning.  
- Rationale for Selection:  
  - Cost-Effectiveness: Available in lab storage, reducing project costs.  
  - Compatibility: Easily interfaces with the Raspberry Pi via USB, leveraging libraries like OpenCV for image processing.  
  - Versatility: Capable of detecting obstacles, recognizing patterns, or following lines, depending on the software implementation.  
- Usage: The camera captures real-time video or images, which are processed by the Raspberry Pi to detect obstacles, navigate paths, or identify specific targets (e.g., markers or objects). The power draw is minimal, and the USB connection simplifies wiring and data transfer.  

### Attempted LiDAR Integration

- Type: Repurposed Cleaning Robot LiDAR module, interfaced via an ESP32.  
- Purpose: Intended for precise distance mapping and obstacle avoidance.  
- Challenges:  
  - Lack of an LDS2USB adapter, requiring custom interfacing with an ESP32.  
  - Inaccurate sensor data due to hard-coded implementation, leading to unreliable performance.  
  - High development time and complexity outweighed benefits given the camera’s sufficiency for basic navigation.  
- Outcome: The LiDAR was abandoned in favor of the camera, which provided adequate sensing for the robot’s requirements within the project’s constraints.  

### DC Motor Encoder

- Type: Incremental encoder attached to the DC motor.  
- Purpose: Provides feedback on motor speed and position for precise control.  
- Rationale for Selection:  
  - Available in lab storage, reducing costs.  
  - Enables closed-loop control, improving navigation accuracy (e.g., maintaining consistent speed or distance traveled).  
- Usage: The encoder sends pulse signals to the Raspberry Pi (via GPIO or the motor driver’s interface), allowing the system to monitor wheel rotation and adjust motor commands for accurate movement.  

---

## Wiring Diagram

The wiring diagram illustrates the power and signal connections between components, ensuring clarity and professionalism. Key features include:

- Color Coding: Red for positive power lines, black for ground, and other colors (e.g., blue, yellow) for signal lines.  
- Connectors: JST or XT60 connectors for high-current paths (battery to motor driver), and pin headers for low-current signal connections.  
- Labels: Each wire and component is labeled for easy identification.  
- Safety Features: A fuse at the battery output and proper grounding to prevent electrical issues.  

---

## Bill of Materials (BOM)

The BOM lists all components used in the power and sense management system, sourced from lab storage.  

## Components On Robot

| Itemized Expenses                                         | Picture                                                                                              | Unit Price | Quantity | Description                                                    | Subtotal   |
|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------|------------|----------|----------------------------------------------------------------|------------|
| 1. LM2596S 3A buck module                                 | ![LM2596S Buck Module](src/images/buck.jpg)                                              | $1.50      | 1 pcs    | Steps down 11.1 V to 5 V/6 V, 5 A capacity                      | $1.50      |
| 2. JGB37-520 encoder gear motor (530 RPM)                 | ![JGB37-520 Motor](src/images/motor.jpg)                                                       | $8.00      | 1 pcs    | DC motor with incremental encoder                              | $8.00      |
| 3. MG90S servo motor (90–180°)                            | ![MG90S Servo](src/images/servo.jpg)                                                               | $1.50      | 1 pcs    | Actuator for mechanical tasks                                  | $4.50      |
| 4. Raspberry Pi 4                                         | ![Raspberry Pi 4](src/images/rppi4.jpg)                                                          | $75.00     | 1 pcs    | Central processing unit                                        | $75.00     |
| 5. L298N motor driver module                              | ![L298N Driver](src/images/driver.jpg)                                                             | $1.50      | 1 pcs    | Controls DC motor, supports encoder input                      | $1.50      |
| 6. 3S LiPo Battery 25C (11.1 V, 2200 mAh)                 | ![3S LiPo Battery](src/images/battery.jpg)                                                       | $23.00     | 1 pcs    | High-capacity LiPo battery                                     | $23.00     |
| 7. 8 MP Autofocus USB 2.0 Camera                          | ![8MP USB Camera](src/images/camera.jpg)                                                         | $40.00     | 1 pcs    | Vision sensor for navigation                                   | $40.00     |
| **Total**                                                 |                                                                                                      |            |          |                                                                | **$153.50** |
