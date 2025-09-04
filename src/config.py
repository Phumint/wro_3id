# ackermann_robot_control/src/config.py

# --- Motor Control Pins ---
# Changed to 16, 20, 21 as requested
MOTOR_IN1 = 20  # GPIO pin for motor driver input 1 (previously 17)
MOTOR_IN2 = 21  # GPIO pin for motor driver input 2 (previously 27)
MOTOR_ENA = 16  # GPIO pin for motor driver enable (PWM) (previously 22)

# Encoder Pins (assuming these remain the same, if you're not changing them)
ENCODER_A = 5   # GPIO pin for encoder channel A
ENCODER_B = 6   # GPIO pin for encoder channel B (if using quadrature encoder)

# --- Steering Control Pins ---
# Assuming this remains the same, if you're not changing it
SERVO_PWM_PIN = 18 # GPIO pin for steering servo (PWM)

# Robot Dimensions (for Ackermann calculations, will be used later)
WHEELBASE_CM = 20.0 # Length from front to rear axle in cm
TRACK_WIDTH_CM = 15.0 # Distance between steering pivots in cm

# Servo Calibration (you might need to adjust these after physical testing)
SERVO_MIN_ANGLE = -25 # Minimum steering angle in degrees (e.g., full right)
SERVO_MAX_ANGLE = 20  # Maximum steering angle in degrees (e.g., full left)
SERVO_CENTER_ANGLE = 0 # Add this line to define the center angle
SERVO_CENTER_PULSE_WIDTH = 1.5 # Pulse width for center in ms (typically 1.5ms)
SERVO_MAX_PULSE_WIDTH = 2.5 # Pulse width for max angle in ms (typically 2.5ms)
SERVO_MIN_PULSE_WIDTH = 0.5 # Pulse width for min angle in ms (typically 0.5ms)
SERVO_FREQUENCY = 50 # Standard servo frequency in Hz