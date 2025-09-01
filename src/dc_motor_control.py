import RPi.GPIO as GPIO
import config

# Global PWM object for the motor
pwm_motor_ena = None

def setup_motor():
    """Initializes the GPIO pins for the DC motor."""
    global pwm_motor_ena
    GPIO.setup(config.MOTOR_IN1, GPIO.OUT)
    GPIO.setup(config.MOTOR_IN2, GPIO.OUT)
    GPIO.setup(config.MOTOR_ENA, GPIO.OUT)
    
    pwm_motor_ena = GPIO.PWM(config.MOTOR_ENA, 1000) # Assuming 1000 Hz for motor PWM
    pwm_motor_ena.start(0)
    print("Motor GPIO setup complete.")

def set_motor_speed(speed):
    """
    Sets the motor speed and direction.
    Speed: a value from -100 to 100.
    """
    if pwm_motor_ena is None:
        print("Error: Motor PWM is not set up.")
        return

    # Clamp speed to a valid range
    speed = max(-100, min(100, speed))
    
    if speed > 0:
        # Forward
        GPIO.output(config.MOTOR_IN1, GPIO.HIGH)
        GPIO.output(config.MOTOR_IN2, GPIO.LOW)
    elif speed < 0:
        # Backward
        GPIO.output(config.MOTOR_IN1, GPIO.LOW)
        GPIO.output(config.MOTOR_IN2, GPIO.HIGH)
    else:
        # Stop
        GPIO.output(config.MOTOR_IN1, GPIO.LOW)
        GPIO.output(config.MOTOR_IN2, GPIO.LOW)
    
    pwm_motor_ena.ChangeDutyCycle(abs(speed))
    print(f"Setting motor speed to {speed}%")

def cleanup_motor():
    """Stops the motor PWM and releases the GPIO pins."""
    global pwm_motor_ena
    if pwm_motor_ena:
        pwm_motor_ena.stop()
        print("Motor GPIO cleaned up.")
