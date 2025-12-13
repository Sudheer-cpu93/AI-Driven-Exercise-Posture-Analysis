import numpy as np
import cv2
from collections import deque


def calculate_angle(a, b, c):
    """
    Calculates the angle (in degrees) between three 2D points.
    b: The vertex of the angle (e.g., Elbow or Hip).
    """
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle


class SmoothingBuffer:

    def __init__(self, window_size=5):
        self.buffer = deque(maxlen=window_size)

    def add_value(self, value):
        self.buffer.append(value)
        
    def get_smoothed_value(self):
        if not self.buffer:
            return 0
        return np.mean(self.buffer)


def draw_feedback_box(frame, feedback_list, position="top_left"):

    height, width = frame.shape[:2]
    
    if position == "top_left":
        x, y = 10, 70
    elif position == "top_right":
        x, y = width - 500, 70
    else:
        x, y = 10, height - 200
    
    # Draw each message
    for i, line in enumerate(feedback_list):
        # Color based on message content
        if "PERFECT" in line or "GOOD" in line:
            color = (0, 255, 0)  # Green
        elif "ERROR" in line:
            color = (0, 0, 255)  # Red
        else:
            color = (255, 255, 255)  # White
            
        cv2.putText(frame, line, (x, y + i * 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)
    
    return frame


def draw_status(frame, status):
    
    status_color = (0, 255, 0) if "PERFECT" in status else (0, 0, 255)
    cv2.putText(frame, status, (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2, cv2.LINE_AA)
    return frame


def draw_angle_arc(frame, point1, vertex, point3, angle, color=(255, 255, 0), radius=50):
    
    try:
        vertex_int = (int(vertex[0] * frame.shape[1]), int(vertex[1] * frame.shape[0]))
        
        
        v1 = np.array([point1[0] - vertex[0], point1[1] - vertex[1]])
        v2 = np.array([point3[0] - vertex[0], point3[1] - vertex[1]])
        
        start_angle = np.degrees(np.arctan2(v1[1], v1[0]))
        end_angle = np.degrees(np.arctan2(v2[1], v2[0]))
        

        cv2.ellipse(frame, vertex_int, (radius, radius), 0, 
                   start_angle, end_angle, color, 2)
        
        
        text_pos = (vertex_int[0] + 10, vertex_int[1] - 10)
        cv2.putText(frame, f"{int(angle)}deg", text_pos,
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    except:
        pass
    
    return frame