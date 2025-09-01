import RPi.GPIO as GPIO
import time
import config

# Global PWM object for the servo
pwm_servo = None

def setup_servo():
    """Initializes the GPIO pin and PWM for the steering servo."""
    global pwm_servo
    GPIO.setup(config.SERVO_PWM_PIN, GPIO.OUT)
    pwm_servo = GPIO.PWM(config.SERVO_PWM_PIN, config.SERVO_FREQUENCY)
    pwm_servo.start(0)
    print("Servo GPIO setup complete.")

def angle_to_duty_cycle(angle):
    """
    Converts a steering angle to a PWM duty cycle for the servo.
    This function uses a linear interpolation based on your configuration.
    """
    # Clamp the angle to the configured range
    angle = max(config.SERVO_MIN_ANGLE, min(config.SERVO_MAX_ANGLE, angle))
    
    # Linear interpolation
    pulse_range = config.SERVO_MAX_PULSE_WIDTH - config.SERVO_MIN_PULSE_WIDTH
    angle_range = config.SERVO_MAX_ANGLE - config.SERVO_MIN_ANGLE
    
    pulse_width = config.SERVO_MIN_PULSE_WIDTH + (angle - config.SERVO_MIN_ANGLE) * (pulse_range / angle_range)
    
    # Convert pulse width to duty cycle
    duty_cycle = (pulse_width / (1000.0 / config.SERVO_FREQUENCY)) * 100
    
    return duty_cycle

def set_steering_angle(angle):
    """Sets the steering angle of the robot's servo."""
    if pwm_servo is None:
        print("Error: Servo PWM is not set up.")
        return

    duty_cycle = angle_to_duty_cycle(angle)
    pwm_servo.ChangeDutyCycle(duty_cycle)
    print(f"Setting steering to {angle} degrees (Duty Cycle: {duty_cycle:.2f}%)")

def cleanup_servo():
    """Stops the servo PWM and releases the GPIO pin."""
    global pwm_servo
    if pwm_servo:
        pwm_servo.stop()
        print("Servo GPIO cleaned up.")
