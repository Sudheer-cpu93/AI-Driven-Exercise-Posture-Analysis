import cv2
import mediapipe as mp
import numpy as np


class PoseDetector:
    """Detects human pose using MediaPipe - YOUR CONFIGURATION"""
    
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize using YOUR MediaPipe setup
        """
        print("Initializing PoseDetector with your configuration...")
        
        # YOUR ORIGINAL MEDIAPIPE SETUP
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Define keypoint mapping (expanded for all 3 exercises)
        self.landmarks_map = {
            # Right side
            'R_SHOULDER': self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
            'R_ELBOW': self.mp_pose.PoseLandmark.RIGHT_ELBOW.value,
            'R_WRIST': self.mp_pose.PoseLandmark.RIGHT_WRIST.value,
            'R_HIP': self.mp_pose.PoseLandmark.RIGHT_HIP.value,
            'R_KNEE': self.mp_pose.PoseLandmark.RIGHT_KNEE.value,
            'R_ANKLE': self.mp_pose.PoseLandmark.RIGHT_ANKLE.value,
            'R_INDEX': self.mp_pose.PoseLandmark.RIGHT_INDEX.value,
            'R_FOOT_INDEX': self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value,
            
            # Left side
            'L_SHOULDER': self.mp_pose.PoseLandmark.LEFT_SHOULDER.value,
            'L_ELBOW': self.mp_pose.PoseLandmark.LEFT_ELBOW.value,
            'L_WRIST': self.mp_pose.PoseLandmark.LEFT_WRIST.value,
            'L_HIP': self.mp_pose.PoseLandmark.LEFT_HIP.value,
            'L_KNEE': self.mp_pose.PoseLandmark.LEFT_KNEE.value,
            'L_ANKLE': self.mp_pose.PoseLandmark.LEFT_ANKLE.value,
            'L_INDEX': self.mp_pose.PoseLandmark.LEFT_INDEX.value,
            'L_FOOT_INDEX': self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value,
            
            # Center
            'NOSE': self.mp_pose.PoseLandmark.NOSE.value
        }
        
        print("✓ PoseDetector ready!")
    
    def detect_pose(self, frame):
        """
        Detect pose in a frame - YOUR EXACT PROCESS
        """
        # YOUR ORIGINAL CONVERSION PROCESS
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        
        if not results.pose_landmarks:
            return None
        
        # Extract coordinates using your method
        coords = self._get_coords(results.pose_landmarks.landmark)
        
        return {
            'coords': coords,
            'landmarks': results.pose_landmarks.landmark,
            'pose_landmarks': results.pose_landmarks
        }
    
    def _get_coords(self, landmarks):
        """
        YOUR ORIGINAL METHOD - Extracts (x, y) coordinates
        """
        coords = {}
        for name, index in self.landmarks_map.items():
            # Use only x and y for 2D angle calculation
            coords[name] = [landmarks[index].x, landmarks[index].y]
        return coords
    
    def draw_landmarks(self, frame, pose_data):
        """
        Draw skeleton - YOUR EXACT DRAWING STYLE
        """
        if pose_data is None:
            return frame
        
        # YOUR ORIGINAL DRAWING SPECS
        self.mp_drawing.draw_landmarks(
            frame, 
            pose_data['pose_landmarks'], 
            self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
            self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
        )
        
        return frame
    
    def close(self):
        """Release resources"""
        self.pose.close()
        print("PoseDetector closed")