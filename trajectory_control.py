# Integration with Sarthak's code
import math
import path_planning


# Carrot-Chasing Algorithm
def get_carrot_position(current_position, path, d):
    closest_point = find_closest_point(current_position, path)
    carrot_position = place_carrot_ahead(closest_point, path, d)
    return carrot_position


def find_closest_point(current_position, path):
    # Placeholder: Find closest point on path (can be implemented using distance formula)
    return path[0]  # Simplified for demonstration


def place_carrot_ahead(closest_point, path, d):
    # Placeholder: Place carrot d units ahead on the path
    return path[1]  # Simplified for demonstration


def calculate_desired_heading(current_position, carrot_position):
    dx = carrot_position[0] - current_position[0]
    dy = carrot_position[1] - current_position[1]
    desired_heading = math.atan2(dy, dx)
    return math.degrees(desired_heading)


# PID Controller
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output


def calculate_heading_error(current_heading, desired_heading):
    error = desired_heading - current_heading
    error = (error + 180) % 360 - 180
    return error


# ------------------- Main Function -------------------
def main(waypoints):
    print("Trajectory Control")
    # Example current position and heading (these would be real-time data in practice)
    current_position = (10, 10)  # Replace with actual data
    current_heading = 90  # Replace with actual data

    # Set the carrot-chasing distance
    d = 10
    # Path-following loop (would typically be inside a control loop)
    for i in range(len(waypoints) - 1):
        path_segment = [waypoints[i], waypoints[i + 1]]
        carrot_position = get_carrot_position(current_position, path_segment, d)
        desired_heading = calculate_desired_heading(current_position, carrot_position)
        heading_error = calculate_heading_error(current_heading, desired_heading)
        pid = PIDController(kp=1.0, ki=0.1, kd=0.05)
        control_command = pid.update(heading_error, dt=0.1)
        # Update current heading and position for the next iteration
        current_heading += control_command * 0.1  # Simplified heading update
        current_position = carrot_position  # Assume aircraft reaches carrot position
        print(
            f"Waypoint {i}: Carrot={carrot_position}, Heading Command={control_command}"
        )


if __name__ == "__main__":
    # Path planning algorithm generates the path and velocity command
    Wn, Wf = path_planning.main()
    waypoints = Wn  # Use Wn not Wf
    main(waypoints)
