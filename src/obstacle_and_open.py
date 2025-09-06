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
