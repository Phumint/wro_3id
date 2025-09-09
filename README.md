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
      <img src="src/images/robot_iso.jpg" width="200" alt="Robot Iso View"/>
      <br>
      Robot Iso View
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/robot_bottom.jpg" width="200" alt="Robot Bot View"/>
      <br>
      Robot Bottom View
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/robot_top.jpg" width="200" alt="Robot Top View"/>
      <br>
      Robot Top View
    </td>
  </tr>
</table>

## Mobility Management - Rear-wheel drive system with Ackermann steering

+ **Drivetrain**: The robot uses a rear-wheel drive system powered by a single geared DC motor.
+ **Differential**: Power is transmitted through a central differential gearbox to the rear wheels, allowing them to spin at different speeds during turns.
+ **Steering**: An Ackermann steering system, actuated by a single hobby servo, controls the front wheels.
+ **Motion**: This combination mimics car-like motion for smooth, precise turns and reduced tire slip.
+ **Chassis**: The chassis is a custom 3D-printed structure designed for optimal stability, weight distribution, and component mounting.

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
+ **Microprocessor**: Raspberry Pi4
  * This is a powerful, low-cost computer perfect for running the robot's control system and processing camera data for tasks like object detection.
+ **Rear Drive**: JGB37-520 encoder gear motor
  * The motor's gearbox provides the torque needed to move the robot. Though not used for this project at the moment, the encoder allows for precise speed and position control.
+ **Steering**: SG92R Steering Servo Motor
  * This small, affordable servo provides the precise angular control required for the Ackermann steering mechanism. Initially we used the infamous sg90s but the plastic gear broke so we switched to a more durable servo.
+ **Sensor**: 8 MP Autofocus USB 2.0 Camera
  * The high-resolution camera with autofocus is ideal for computer vision tasks, such as navigation and object recognition. However, **this camera FOV is too narrow**, limiting robot's capabilities in obstacle maneuvering :cry:.

<table>
  <tr>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/rppi4.jpg" width="200" alt="rppi4"/>
      <br>
      Raspberry Pi 4
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/motor.jpg" width="200" alt="dc motor"/>
      <br>
      JGB37-520 encoder gear motor
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/new_servo.jpg" width="200" alt="servo"/>
      <br>
      SG92R Steering Servo Motor
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/camera.jpg" width="200" alt="camera"/>
      <br>
       8 MP Autofocus USB 2.0 Camera
    </td>
  </tr>
</table>

## Electrical Components

+ **Main Power Source**: 3S LiPo Battery
  * A 3S LiPo battery provides a nominal voltage of 11.1 V (3 cells in series) and a capacity of 2200 mAh. Its high C-rating of 25C allows it to safely deliver a high current (up to 55A), which is necessary for the motor's peak power demands without damaging the battery.
+ **Voltage Regulation**: LM2596S Buck Converter
  * The LM2596S buck converter efficiently steps down the 11.1 V from the LiPo battery to the required voltage for the Raspberry Pi and other low-power electronics, such as the servo. With a 3A output, it provides a stable power supply, preventing damage to sensitive components from over-voltage.
+ **Motor Driver**: BTS7960 Driver
  * The BTS7960 driver is used to control the DC motor. We initally used the infamous L298N motor driver but because it features a big voltage drop of 2V, we decided to go with the BTS.

<table>
  <tr>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/battery.jpg" width="200" alt="battery"/>
      <br>
      3S LiPo Battery
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/buck.jpg" width="200" alt="buck"/>
      <br>
      LM2596S Buck Converter
    </td>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/bts.jpg" width="200" alt="driver"/>
      <br>
      BTS7960 Motor Driver
    </td>
  </tr>
</table>

## Power Management and Distribution

<table>
  <tr>
    <td align="center" style="vertical-align: top;">
      <img src="src/images/wiring.jpg" width="200" alt="schematic, kinda"/>
      <br>
      Simple Wiring Diagram
    </td>
  </tr>
</table>

The robot's power system uses a 3S LiPo battery (11.1 V, 2200 mAh) as the main power source. This single battery efficiently powers all components.

+ **Motor and Driver**: The JGB37-520 motor is powered directly by the 11.1 V battery. The BTS7960 motor driver can handle this voltage without issue, providing ample power to the drive system.
+ **Electronics (Raspberry Pi & Servo)**: The buck converter steps down the 11.1 V battery voltage to power the electronics with 5V.
+ **Raspberry Pi 4**: The buck converter is wired to a USB-C cable to power the Pi, which is a more stable method than using the 5V GPIO pin.
+ **Servo**: The SG92R servo operates at 5V and is also powered by the buck converter.
+ **Camera**: The USB camera is powered directly through the Raspberry Pi's USB port, drawing its power from the Pi's regulated 5V rail.

This design ensures all components receive the correct voltage while minimizing the number of batteries required.

---

# Software

**Both open and obstacle round uses the same script.** The script contains wall following for the open round and a pillar avoidance state when conditions are met.

## Pseudocode of the whole program

```
import cv2
import numpy as np
import RPi.GPIO as GPIO

from steering_motor_control import setup_servo, set_steering_angle, cleanup_servo
from BTSdc_motor_control import setup_motor, set_motor_speed, cleanup_motor
import config

GPIO.setmode(GPIO.BCM)

# --- Pin definitions ---
BUTTON_PIN = 26  # Button between GPIO26 and GND

# --- Tunable constants ---
RED_TARGET = 10
GREEN_TARGET = 640 - RED_TARGET
KP_PILLAR = 0.5
KD_PILLAR = 0.1
KP_WALL = 0.005
KD_WALL = 0.002
y_boundary = 380
ignore_line = 250
alpha = 0.1

# --- HSV bounds ---
lower_wall = np.array([0, 0, 0])
upper_wall = np.array([179, 153, 144])
lower_green = np.array([40, 50, 50])
upper_green = np.array([85, 255, 255])
lower_red1 = np.array([0, 150, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 150, 70])
upper_red2 = np.array([180, 255, 255])
lower_orange = np.array([0, 0, 180])
upper_orange = np.array([89, 255, 255])
lower_blue = np.array([86, 40, 0])
upper_blue = np.array([150, 255, 255])

# --- ROI coordinates ---
roi_left_x1, roi_left_y1 = 0, 360
roi_left_x2, roi_left_y2 = 86, 470
roi_right_x1, roi_right_y1 = 640 - roi_left_x2, 360
roi_right_x2, roi_right_y2 = 640 - roi_left_x1, 470
roi_mid_x1, roi_mid_y1 = 215, 434
roi_mid_x2, roi_mid_y2 = 411, 464
mid_threshold = 50

red_target = RED_TARGET
green_target = GREEN_TARGET
kernel = np.ones((5, 5), np.uint8)

# --- Functions --- #
def wait_for_button():
    print("[INFO] Waiting for button press to start...")
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        pass
    print("[INFO] Button pressed! Starting loop...")

def find_max_contour_area(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0
    return max(cv2.contourArea(c) for c in contours)

def calculate_steering_angle(left_area, right_area, prev_error):
    error = right_area - left_area
    derivative = error - prev_error
    Kp, Kd = KP_WALL, KD_WALL
    steering_angle = Kp * error + Kd * derivative
    clamped_angle = max(config.SERVO_MIN_ANGLE,
                        min(config.SERVO_MAX_ANGLE, steering_angle))
    return clamped_angle, error

def calculate_pillar_angle(pillar_x, target_x, prev_error):
    error = pillar_x - target_x
    derivative = error - prev_error
    steering_angle = -(KP_PILLAR * error + KD_PILLAR * derivative)
    clamped_angle = max(config.SERVO_MIN_ANGLE,
                        min(config.SERVO_MAX_ANGLE, steering_angle))
    return clamped_angle, error

def is_pillar_contour(contour):
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = h / w if w > 0 else 0
    area = cv2.contourArea(contour)
    rect_area = w * h
    solidity = area / rect_area if rect_area > 0 else 0
    return (h > 50) and (aspect_ratio > 1.2) and (solidity > 0.7)

# --- Main loop --- #
def main_loop():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        setup_servo()
        setup_motor()
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        wait_for_button()
        set_motor_speed(-100)  # Negative = forward

        prev_error_wall = 0.0
        prev_error_pillar = 0.0
        prev_angle = 0.0
        orange_seen = False
        blue_seen = False
        ready_to_count = False
        encoder_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # --- Red and Green pillar detection ---
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)

            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

            contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Select the closest pillar based on bottom y-coordinate
            closest_pillar = None
            closest_pillar_x = None
            max_y = 0

            for c in contours_red + contours_green:
                if is_pillar_contour(c):
                    x, y, w, h = cv2.boundingRect(c)
                    bottom_y = y + h
                    if bottom_y > y_boundary and bottom_y > ignore_line and bottom_y > max_y:
                        max_y = bottom_y
                        closest_pillar_x = x + w // 2
                        if any(np.array_equal(c, cr) for cr in contours_red):
                            closest_pillar = "red"
                        else:
                            closest_pillar = "green"

            # --- Steering ---
            if closest_pillar is not None and closest_pillar_x is not None:
                target_x = red_target if closest_pillar == "red" else green_target
                angle, prev_error_pillar = calculate_pillar_angle(closest_pillar_x, target_x, prev_error_pillar)
                smoothed_angle = alpha * angle + (1 - alpha) * prev_angle
                prev_angle = smoothed_angle
                set_steering_angle(smoothed_angle)
            else:
                # Wall following fallback
                mask_wall = cv2.inRange(hsv, lower_wall, upper_wall)
                mask_wall = cv2.morphologyEx(mask_wall, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
                mask_wall = cv2.morphologyEx(mask_wall, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8))
                roi_left = mask_wall[roi_left_y1:roi_left_y2, roi_left_x1:roi_left_x2]
                roi_right = mask_wall[roi_right_y1:roi_right_y2, roi_right_x1:roi_right_x2]
                left_area = find_max_contour_area(roi_left)
                right_area = find_max_contour_area(roi_right)
                print(f"[DEBUG] Left contour area: {left_area}, Right contour area: {right_area}")
                angle, prev_error_wall = calculate_steering_angle(left_area, right_area, prev_error_wall)
                set_steering_angle(angle)

            # --- Mid ROI encoder ---
            roi_mid = hsv[roi_mid_y1:roi_mid_y2, roi_mid_x1:roi_mid_x2]
            mask_orange = cv2.inRange(roi_mid, lower_orange, upper_orange)
            mask_blue = cv2.inRange(roi_mid, lower_blue, upper_blue)
            orange_detected = cv2.countNonZero(mask_orange) > mid_threshold
            blue_detected = cv2.countNonZero(mask_blue) > mid_threshold

            if orange_detected:
                orange_seen = True
            if blue_detected:
                blue_seen = True
            if orange_seen and blue_seen:
                ready_to_count = True
            if ready_to_count and not orange_detected and not blue_detected:
                encoder_count += 1
                print(f"[ENCODER] Count: {encoder_count}")
                orange_seen = False
                blue_seen = False
                ready_to_count = False

            # --- Stop after 12 counts ---
            if encoder_count >= 13:
                print("[INFO] Encoder reached 12, stopping robot.")
                set_motor_speed(0)
                break

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl+C).")
    finally:
        cap.release()
        cleanup_servo()
        cleanup_motor()
        GPIO.cleanup()
        print("Resources cleaned up. Exiting.")

if __name__ == "__main__":
    main_loop()
```

### Attempted LiDAR Integration

- Type: Repurposed Cleaning Robot LiDAR module, interfaced via an ESP32.  
- Purpose: Intended for precise distance mapping and obstacle avoidance.  
- Challenges:  
  - Lack of an LDS2USB adapter, requiring custom interfacing with an ESP32.  
  - Inaccurate sensor data due to hard-coded implementation, leading to unreliable performance.  
  - High development time and complexity outweighed benefits given the camera’s sufficiency for basic navigation.  
- Outcome: The LiDAR was abandoned in favor of the camera, which provided adequate sensing for the robot’s requirements within the project’s constraints.  

## Bill of Materials (BOM)

The BOM lists all components used in the mobile robot.  

## Components On Robot

| Itemized Expenses                                         | Picture                                                                                              | Unit Price | Quantity | Description                                                    | Subtotal   |
|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------|------------|----------|----------------------------------------------------------------|------------|
| 1. LM2596S 3A buck module                                 | ![LM2596S Buck Module](src/images/buck.jpg)                                              | $1.50      | 1 pcs    | Steps down 11.1 V to 5 V/6 V, 5 A capacity                      | $1.50      |
| 2. JGB37-520 encoder gear motor (530 RPM)                 | ![JGB37-520 Motor](src/images/motor.jpg)                                                       | $8.00      | 1 pcs    | DC motor with incremental encoder                              | $8.00      |
| 3. SG92R Steering Servo Motor                            | ![SG92R Servo](src/images/new_servo.jpg)                                                               | $2.00      | 1 pcs    | Actuator for mechanical tasks                                  | $2.00      |
| 4. Raspberry Pi 4                                         | ![Raspberry Pi 4](src/images/rppi4.jpg)                                                          | $75.00     | 1 pcs    | Central processing unit                                        | $75.00     |
| 5. BTS7960 Driver                              | ![BTS7960 Driver](src/images/bts.jpg)                                                             | $4.00      | 1 pcs    | Controls DC motor, supports encoder input                      | $4.00      |
| 6. 3S LiPo Battery 25C (11.1 V, 2200 mAh)                 | ![3S LiPo Battery](src/images/battery.jpg)                                                       | $23.00     | 1 pcs    | High-capacity LiPo battery                                     | $23.00     |
| 7. 8 MP Autofocus USB 2.0 Camera                          | ![8MP USB Camera](src/images/camera.jpg)                                                         | $40.00     | 1 pcs    | Vision sensor for navigation                                   | $40.00     |
| **Total**                                                 |                                                                                                      |            |          |                                                                | **$153.50** |
