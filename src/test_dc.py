# ackermann_robot_control/src/motor_test.py
import RPi.GPIO as GPIO
import time
import threading
import config # Assuming config.py is in the same directory now

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup() # Add this line to ensure a clean state before setup

# Setup motor pins
GPIO.setup(config.MOTOR_IN1, GPIO.OUT)
GPIO.setup(config.MOTOR_IN2, GPIO.OUT)
GPIO.setup(config.MOTOR_ENA, GPIO.OUT)

# Setup PWM for motor speed control
pwm_motor = GPIO.PWM(config.MOTOR_ENA, 100) # 100 Hz PWM frequency
pwm_motor.start(0) # Start with 0% duty cycle (motor off)

# --- Encoder setup ---
# Global variables for encoder
encoder_pulse_count = 0 # This will now be a signed count
last_encoder_time = time.time() # This variable is currently unused but useful for velocity calculation later
lock = threading.Lock() # To protect encoder_pulse_count in multithreaded context

# Setup both encoder pins for input
GPIO.setup(config.ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(config.ENCODER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def encoder_callback(channel):
    """
    Callback function for encoder interrupts (quadrature).
    This function increments or decrements the count based on the state of ENCODER_B
    when a rising edge is detected on ENCODER_A, providing a signed pulse count.
    """
    global encoder_pulse_count
    with lock:
        # Check the state of ENCODER_A. We only add an event detect for RISING edge on A.
        # When ENCODER_A rises, we check ENCODER_B to determine direction.
        if GPIO.input(config.ENCODER_B) == GPIO.LOW:
            # If B is LOW when A rises, it's typically one direction (e.g., forward)
            encoder_pulse_count += 1
        else:
            # If B is HIGH when A rises, it's the other direction (e.g., reverse)
            encoder_pulse_count -= 1
    # You can uncomment the print below for real-time debugging of pulses
    print(f"Encoder pulse! Current signed count: {encoder_pulse_count}")

# Add interrupt detection for only the rising edge of ENCODER_A.
# The bouncetime is crucial to prevent multiple detections from a single physical event.
GPIO.add_event_detect(config.ENCODER_A, GPIO.RISING, callback=encoder_callback, bouncetime=20)


def set_motor_speed(speed):
    """
    Sets the motor speed and direction.
    Speed should be a value between -100 (full reverse) and 100 (full forward).
    """
    if speed > 0: # Forward
        GPIO.output(config.MOTOR_IN1, GPIO.HIGH)
        GPIO.output(config.MOTOR_IN2, GPIO.LOW)
        pwm_motor.ChangeDutyCycle(speed)
        print(f"Motor moving forward at {speed}% speed.")
    elif speed < 0: # Reverse
        GPIO.output(config.MOTOR_IN1, GPIO.LOW)
        GPIO.output(config.MOTOR_IN2, GPIO.HIGH)
        pwm_motor.ChangeDutyCycle(abs(speed))
        print(f"Motor moving reverse at {abs(speed)}% speed.")
    else: # Stop
        GPIO.output(config.MOTOR_IN1, GPIO.LOW)
        GPIO.output(config.MOTOR_IN2, GPIO.LOW)
        pwm_motor.ChangeDutyCycle(0)
        print("Motor stopped.")

def get_encoder_data():
    """Returns the current encoder pulse count (signed)."""
    with lock:
        return encoder_pulse_count

try:
    print("--- DC Motor Test (Quadrature Encoder) ---")
    print("Motor will run forward, then reverse, then stop. Encoder pulses will be signed.")
    print("Watching for encoder pulses...")

    # Reset encoder count for the start of the test
    with lock:
        encoder_pulse_count = 0

    # Test forward movement
    set_motor_speed(50) # 50% speed forward
    time.sleep(3) # Run for 3 seconds
    forward_pulses = get_encoder_data()
    print(f"Forward movement pulses (signed): {forward_pulses}")

    # Stop briefly
    set_motor_speed(0)
    time.sleep(1)

    # Reset encoder count for the reverse test
    with lock:
        encoder_pulse_count = 0

    # Test reverse movement
    set_motor_speed(-50) # 50% speed reverse
    time.sleep(3) # Run for 3 seconds
    reverse_pulses = get_encoder_data()
    print(f"Reverse movement pulses (signed): {reverse_pulses}")

    # Stop
    set_motor_speed(0)
    time.sleep(1)

except KeyboardInterrupt:
    print("\nTest interrupted by user.")
finally:
    pwm_motor.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
