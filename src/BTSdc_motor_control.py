import RPi.GPIO as GPIO
import config

# Global PWM objects for the motor
pwm_motor_rpwm = None
pwm_motor_lpwm = None

def setup_motor():
    """Initializes the GPIO pins for the DC motor (BTS7960)."""
    global pwm_motor_rpwm, pwm_motor_lpwm
    
    # Setup enable pins
    GPIO.setup(config.MOTOR_R_EN, GPIO.OUT)
    GPIO.setup(config.MOTOR_L_EN, GPIO.OUT)

    # Setup PWM pins
    GPIO.setup(config.MOTOR_RPWM, GPIO.OUT)
    GPIO.setup(config.MOTOR_LPWM, GPIO.OUT)

    # Start both PWM objects
    pwm_motor_rpwm = GPIO.PWM(config.MOTOR_RPWM, 1000)
    pwm_motor_lpwm = GPIO.PWM(config.MOTOR_LPWM, 1000)
    
    # Start with duty cycle of 0
    pwm_motor_rpwm.start(0)
    pwm_motor_lpwm.start(0)
    
    # Enable the driver permanently
    GPIO.output(config.MOTOR_R_EN, GPIO.HIGH)
    GPIO.output(config.MOTOR_L_EN, GPIO.HIGH)
    
    print("Motor GPIO setup complete for BTS7960.")

def set_motor_speed(speed):
    """
    Sets the motor speed and direction for BTS7960.
    Speed: a value from -100 to 100.
    """
    global pwm_motor_rpwm, pwm_motor_lpwm
    if pwm_motor_rpwm is None or pwm_motor_lpwm is None:
        print("Error: Motor PWM is not set up.")
        return

    # Clamp speed to a valid range
    speed = max(-100, min(100, speed))
    
    if speed > 0:
        # Forward
        pwm_motor_lpwm.ChangeDutyCycle(abs(speed))
        pwm_motor_rpwm.ChangeDutyCycle(0)
    elif speed < 0:
        # Backward
        pwm_motor_lpwm.ChangeDutyCycle(0)
        pwm_motor_rpwm.ChangeDutyCycle(abs(speed))
    else:
        # Stop
        pwm_motor_lpwm.ChangeDutyCycle(0)
        pwm_motor_rpwm.ChangeDutyCycle(0)
        
    print(f"Setting motor speed to {speed}%")

def cleanup_motor():
    """Stops the motor PWM and releases the GPIO pins."""
    global pwm_motor_rpwm, pwm_motor_lpwm
    if pwm_motor_rpwm:
        pwm_motor_rpwm.stop()
    if pwm_motor_lpwm:
        pwm_motor_lpwm.stop()
    print("Motor GPIO cleaned up.")