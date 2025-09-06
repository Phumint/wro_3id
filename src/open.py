import cv2
import numpy as np
import RPi.GPIO as GPIO

# Import custom servo and motor control
from steering_motor_control import setup_servo, set_steering_angle, cleanup_servo
from dc_motor_control import setup_motor, set_motor_speed, cleanup_motor
import config

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)


def calculate_steering_angle(left_pixels, right_pixels, max_pixels, prev_error):
    """
    PD control for steering.
    - P term: proportional to pixel imbalance.
    - D term: change in imbalance across frames.
    """
    # Error: pixel imbalance (positive = more right pixels)
    error = right_pixels - left_pixels
    normalized_error = error / max_pixels  # range ~ [-1, 1]

    # Derivative (rate of change of error)
    derivative = normalized_error - prev_error

    # --- Tunable gains ---
    Kp = 50.0   # proportional gain
    Kd = 15.0   # derivative gain

    # PD control law
    steering_angle = (Kp * normalized_error) + (Kd * derivative)

    # Clamp to servo limits
    clamped_angle = max(config.SERVO_MIN_ANGLE,
                        min(config.SERVO_MAX_ANGLE, steering_angle))

    return clamped_angle, normalized_error


def main_loop():
    """Main loop: video, steering, motor control."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # HSV bounds for brownish-yellow wall
    lower_bound = np.array([0, 50, 0])
    upper_bound = np.array([33, 255, 149])

    # Define ROIs (tuned for 640x480 frame)
    # roi_left_x1, roi_left_y1 = 4, 325
    # roi_left_x2, roi_left_y2 = 87, 365
    # roi_right_x1, roi_right_y1 = 640 - roi_left_x2, 325
    # roi_right_x2, roi_right_y2 = 640 - roi_left_x1, 365

    roi_left_x1, roi_left_y1 = 1, 378
    roi_left_x2, roi_left_y2 = 86, 441
    roi_right_x1, roi_right_y1 = 640 - roi_left_x2, 378
    roi_right_x2, roi_right_y2 = 640 - roi_left_x1, 441

    max_roi_pixels = (roi_left_x2 - roi_left_x1) * (roi_left_y2 - roi_left_y1)

    try:
        # Setup hardware
        setup_servo()
        setup_motor()

        # Start forward motion at 50% speed
        set_motor_speed(-100)

        prev_error = 0.0  # initialize error memory

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

            # --- Steering calculation (PD control) ---
            steering_angle, prev_error = calculate_steering_angle(
                white_pixels_left,
                white_pixels_right,
                max_roi_pixels,
                prev_error
            )
            set_steering_angle(steering_angle)

            # --- Debug output ---
            print(f"L: {white_pixels_left:4d}, R: {white_pixels_right:4d}, "
                  f"Steering: {steering_angle:6.2f} deg")

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        cap.release()
        cleanup_servo()
        cleanup_motor()
        GPIO.cleanup()
        print("Resources cleaned up. Exiting.")


if __name__ == "__main__":
    main_loop()
