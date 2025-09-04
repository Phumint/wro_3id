import cv2
import numpy as np
import RPi.GPIO as GPIO

# Import custom servo and motor control
from steering_motor_control import setup_servo, set_steering_angle, cleanup_servo
from dc_motor_control import setup_motor, set_motor_speed, cleanup_motor
import config

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# --- Tunable constants ---
RED_TARGET = 1
GREEN_TARGET = 640 - RED_TARGET
KP_PILLAR = 0.5
KD_PILLAR = 0.1
y_boundary = 340       # Consider pillars only if their bottom is below this line
ignore_line = 250      # Skip pillars with bottom above this line

# --- HSV bounds ---
lower_wall = np.array([0, 50, 0])
upper_wall = np.array([33, 255, 194])
lower_green = np.array([40, 50, 50])
upper_green = np.array([85, 255, 255])
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# --- ROI coordinates ---
roi_left_x1, roi_left_y1 = 1, 378
roi_left_x2, roi_left_y2 = 86, 441
roi_right_x1, roi_right_y1 = 640 - roi_left_x2, 378
roi_right_x2, roi_right_y2 = 640 - roi_left_x1, 441
max_roi_pixels = (roi_left_x2 - roi_left_x1) * (roi_left_y2 - roi_left_y1)


def calculate_steering_angle(left_pixels, right_pixels, max_pixels, prev_error):
    """PD control for wall following."""
    error = right_pixels - left_pixels
    normalized_error = error / max_pixels
    derivative = normalized_error - prev_error
    Kp, Kd = 50.0, 15.0
    steering_angle = Kp * normalized_error + Kd * derivative
    clamped_angle = max(config.SERVO_MIN_ANGLE,
                        min(config.SERVO_MAX_ANGLE, steering_angle))
    return clamped_angle, normalized_error


def calculate_pillar_angle(pillar_x, target_x, prev_error):
    """PD control for pillar avoidance."""
    error = pillar_x - target_x
    derivative = error - prev_error
    steering_angle = -(KP_PILLAR * error + KD_PILLAR * derivative)
    clamped_angle = max(config.SERVO_MIN_ANGLE,
                        min(config.SERVO_MAX_ANGLE, steering_angle))
    return clamped_angle, error


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
        set_motor_speed(-100)

        prev_error_wall = 0.0
        prev_error_pillar = 0.0
        prev_pillar = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # --- Red pillar detection ---
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            closest_pillar, closest_pillar_x = None, None
            if contours_red:
                largest = max(contours_red, key=cv2.contourArea)
                if cv2.contourArea(largest) > 100:
                    x, y, w, h = cv2.boundingRect(largest)
                    if y + h > y_boundary and y + h > ignore_line:
                        closest_pillar = "red"
                        closest_pillar_x = x + w // 2

            # --- Green pillar detection ---
            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours_green:
                largest = max(contours_green, key=cv2.contourArea)
                if cv2.contourArea(largest) > 100:
                    x, y, w, h = cv2.boundingRect(largest)
                    if y + h > y_boundary and y + h > ignore_line and closest_pillar is None:
                        closest_pillar = "green"
                        closest_pillar_x = x + w // 2

            # --- Control logic ---
            if closest_pillar is not None and closest_pillar_x is not None and prev_pillar != closest_pillar:
                target_x = RED_TARGET if closest_pillar == "red" else GREEN_TARGET
                angle, prev_error_pillar = calculate_pillar_angle(closest_pillar_x, target_x, prev_error_pillar)
                set_steering_angle(angle)
                prev_pillar = closest_pillar
                print(f"[PILLAR] {closest_pillar} at X={closest_pillar_x}, Steering={angle:.2f}")
            else:
                prev_pillar = None
                # Wall following
                mask_wall = cv2.inRange(hsv, lower_wall, upper_wall)
                mask_wall = cv2.morphologyEx(mask_wall, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
                roi_left = mask_wall[roi_left_y1:roi_left_y2, roi_left_x1:roi_left_x2]
                roi_right = mask_wall[roi_right_y1:roi_right_y2, roi_right_x1:roi_right_x2]
                left_count = cv2.countNonZero(roi_left)
                right_count = cv2.countNonZero(roi_right)
                angle, prev_error_wall = calculate_steering_angle(left_count, right_count, max_roi_pixels, prev_error_wall)
                set_steering_angle(angle)
                print(f"[WALL] L={left_count}, R={right_count}, Steering={angle:.2f}")

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
