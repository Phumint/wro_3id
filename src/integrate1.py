import cv2
import numpy as np
import time
import RPi.GPIO as GPIO

# Import custom servo and motor control
from steering_motor_control import setup_servo, set_steering_angle, cleanup_servo
from dc_motor_control import setup_motor, set_motor_speed, cleanup_motor
import config

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

def calculate_steering_angle(left_pixels, right_pixels, max_pixels):
    """
    Calculates the steering angle based on the difference in white pixels.
    Convention:
        -30° = right turn
        +30° = left turn
    NOTE: Flipped left ↔ right mapping.
    """
    error = right_pixels - left_pixels
    normalized_error = error / max_pixels

    # Flipped mapping (no minus sign)
    steering_angle = normalized_error * config.SERVO_MAX_ANGLE

    clamped_angle = max(config.SERVO_MIN_ANGLE, min(config.SERVO_MAX_ANGLE, steering_angle))
    return clamped_angle


def main_loop():
    """The main loop for video processing, steering, and motor control."""

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # HSV bounds for the wall
    lower_bound = np.array([0, 54, 0])
    upper_bound = np.array([37, 255, 170])

    # Define ROIs
    roi_left_x1, roi_left_y1 = 4, 325
    roi_left_x2, roi_left_y2 = 87, 365
    roi_right_x1, roi_right_y1 = 640 - roi_left_x2, 325
    roi_right_x2, roi_right_y2 = 640 - roi_left_x1, 365

    max_roi_pixels = (roi_left_x2 - roi_left_x1) * (roi_left_y2 - roi_left_y1)

    try:
        # Setup servo + motor
        setup_servo()
        setup_motor()

        # Start driving forward at 50% speed
        set_motor_speed(50)

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # --- Image processing ---
            blurred_frame = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

            kernel = np.ones((5, 5), np.uint8)
            closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            noise_mask = cv2.subtract(closed_mask, mask)
            inpainted_frame = cv2.inpaint(frame, noise_mask, 3, cv2.INPAINT_TELEA)

            hsv_inpainted = cv2.cvtColor(inpainted_frame, cv2.COLOR_BGR2HSV)
            final_mask = cv2.inRange(hsv_inpainted, lower_bound, upper_bound)

            kernel_final = np.ones((7, 7), np.uint8)
            final_mask_cleaned = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel_final)

            # --- ROI extraction ---
            roi_mask_left = final_mask_cleaned[roi_left_y1:roi_left_y2, roi_left_x1:roi_left_x2]
            roi_mask_right = final_mask_cleaned[roi_right_y1:roi_right_y2, roi_right_x1:roi_right_x2]

            white_pixels_left = cv2.countNonZero(roi_mask_left)
            white_pixels_right = cv2.countNonZero(roi_mask_right)

            # --- Steering calculation ---
            steering_angle = calculate_steering_angle(white_pixels_left, white_pixels_right, max_roi_pixels)
            set_steering_angle(steering_angle)

            # --- Debug output ---
            print(f"Left: {white_pixels_left:4d}, Right: {white_pixels_right:4d}, Steering: {steering_angle:6.2f} deg")

            # Save one debug frame every ~3 seconds
            frame_count += 1
            if frame_count % 90 == 0:  # assuming ~30 FPS
                filename = f"debug_frame_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"[INFO] Saved debug frame: {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cap.release()
        cleanup_servo()
        cleanup_motor()
        GPIO.cleanup()
        print("Resources cleaned up. Exiting.")


if __name__ == "__main__":
    main_loop()
