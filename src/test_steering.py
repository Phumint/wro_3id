# ackermann_robot_control/src/steering_test.py
import RPi.GPIO as GPIO
import time
import config

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup servo pin
GPIO.setup(config.SERVO_PWM_PIN, GPIO.OUT)

# Setup PWM for servo control
# Servos typically operate at 50 Hz
pwm_servo = GPIO.PWM(config.SERVO_PWM_PIN, config.SERVO_FREQUENCY)
pwm_servo.start(0) # Start with 0% duty cycle

def angle_to_duty_cycle(angle):
    """
    Converts an angle (-90 to 90 degrees) to a PWM duty cycle for the servo.
    This is a simplified conversion. Actual values might need calibration.
    Typically, 0.5ms pulse is 0 degrees, 1.5ms is 90 degrees (center), 2.5ms is 180 degrees.
    With a 50Hz frequency (20ms period), these correspond to:
    0.5ms / 20ms = 2.5% duty cycle
    1.5ms / 20ms = 7.5% duty cycle
    2.5ms / 20ms = 12.5% duty cycle
    """
    # Map the desired angle range (e.g., -30 to 30) to the servo's pulse width range
    # Ensure angle is within the defined min/max
    angle = max(config.SERVO_MIN_ANGLE, min(config.SERVO_MAX_ANGLE, angle))

    min_dc = 5.0  # Duty cycle for minimum angle (e.g., full left)
    max_dc = 10.0 # Duty cycle for maximum angle (e.g., full right)

    # Convert angle from [-SERVO_MAX_ANGLE, +SERVO_MAX_ANGLE] to [0, 1] range
    normalized_angle = (angle - config.SERVO_MIN_ANGLE) / (config.SERVO_MAX_ANGLE - config.SERVO_MIN_ANGLE)

    # Map to duty cycle range
    duty_cycle = min_dc + normalized_angle * (max_dc - min_dc)
    return duty_cycle

def set_steering_angle(angle):
    """
    Sets the steering angle for the servo.
    Angle should be within SERVO_MIN_ANGLE and SERVO_MAX_ANGLE.
    """
    duty_cycle = angle_to_duty_cycle(angle)
    pwm_servo.ChangeDutyCycle(duty_cycle)
    print(f"Setting steering to {angle} degrees (Duty Cycle: {duty_cycle:.2f}%)")

try:
    print("--- Steering Servo Test ---")
    print("Servo will move from center to max left, then max right, then back to center.")

    # Center position
    set_steering_angle(0)
    time.sleep(2)

    # Max left
    set_steering_angle(config.SERVO_MIN_ANGLE)
    time.sleep(2)

    # Max right
    set_steering_angle(config.SERVO_MAX_ANGLE)
    time.sleep(2)

    # Back to center
    set_steering_angle(0)
    time.sleep(2)

except KeyboardInterrupt:
    print("\nTest interrupted by user.")
finally:
    pwm_servo.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
