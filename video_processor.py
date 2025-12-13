import cv2
import os
from pose_detector import PoseDetector
from form_analyzer import FormAnalyzer
from utils import draw_feedback_box, draw_status


class VideoProcessor:
    
    def __init__(self, exercise_type, input_path, output_path=None):
        
        print("\n" + "="*60)
        print("EXERCISE FORM DETECTION SYSTEM")
        print("="*60)
        
        self.exercise_type = exercise_type
        self.input_path = input_path
        self.output_path = output_path
        
        
        print("\nInitializing components...")
        self.pose_detector = PoseDetector()
        self.form_analyzer = FormAnalyzer(exercise_type)
        
        print(f"Exercise: {exercise_type}")
        print(f"Input: {input_path}")
        if output_path:
            print(f"Output: {output_path}")
        print("="*60 + "\n")
        
        
        self.frame_count = 0
        self.perfect_frames = 0
        self.total_frames = 0
    
    def run_analysis(self):
        
        cap = cv2.VideoCapture(self.input_path)
        
        if not cap.isOpened():
            raise FileNotFoundError(f"Error: Could not open video file at {self.input_path}")
        
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps == 0:
            fps = 30  # Default if can't read
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Video: {width}x{height} @ {fps}fps")
        if self.total_frames > 0:
            print(f"Total frames: {self.total_frames}")
        print("Processing... (Press 'q' to quit)\n")
        
        
        writer = None
        if self.output_path:
            # Create output directory if doesn't exist
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))
            print(f"Saving output to: {self.output_path}")
        
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            
    
            processed_frame = self._process_frame(frame)
            
            
            if writer:
                writer.write(processed_frame)
            
        
            cv2.imshow('Exercise Form Analysis - Press Q to quit', processed_frame)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                print("\nStopped by user")
                break
            
            
            if self.frame_count % 30 == 0:
                if self.total_frames > 0:
                    progress = (self.frame_count / self.total_frames) * 100
                    print(f"Progress: {self.frame_count}/{self.total_frames} ({progress:.1f}%)")
                else:
                    print(f"Processed: {self.frame_count} frames")
        
    
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
        self.pose_detector.close()
        
    
        self._print_summary()
    
    def _process_frame(self, frame):
        """Process single frame"""
        image = frame.copy()
        full_feedback = []
        overall_status = "PERFECT FORM"
        
        try:
        
            pose_data = self.pose_detector.detect_pose(image)
            
            if pose_data is None:
                raise Exception("No pose detected")
            
            coords = pose_data['coords']
            
            
            full_feedback, overall_status = self.form_analyzer.analyze_frame(coords)
            
            if overall_status == "PERFECT FORM":
                self.perfect_frames += 1
            
    
            
            
            image = self.pose_detector.draw_landmarks(image, pose_data)
            
        
            image = draw_status(image, overall_status)
            
            
            image = draw_feedback_box(image, full_feedback)
            
        
            cv2.putText(image, f"Exercise: {self.exercise_type.upper()}", 
                       (10, image.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
        except Exception as e:

            cv2.putText(image, "Pose not detected - adjust camera", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"Error: {str(e)[:50]}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        
        return image
    
    def _print_summary(self):
        print("\n" + "="*60)
        print("PROCESSING COMPLETE - SUMMARY")
        print("="*60)
        print(f"Total Frames: {self.frame_count}")
        print(f"Perfect Form Frames: {self.perfect_frames}")
        
        if self.frame_count > 0:
            accuracy = (self.perfect_frames / self.frame_count) * 100
            print(f"Form Accuracy: {accuracy:.1f}%")
        
        if self.output_path:
            print(f"\n Output saved: {self.output_path}")
        print("="*60 + "\n")




if __name__ == '__main__':
    
     
    EXERCISE = 'PushUps'  # Change to: PushUps, BodyWeightSquats, Lunges, etc.
    
    
    BASE_PATH = r"D:\CV_Project\Gym Exercises"  # Your base folder
    VIDEO_FILE = r"PushUps\v_PushUps_g01_c02.avi"  # Relative path from base
    OUTPUT_FILE = r"Output\pushups_analyzed.mp4"  # Output path
    
    
    INPUT_PATH = os.path.join(BASE_PATH, VIDEO_FILE)
    OUTPUT_PATH = os.path.join(BASE_PATH, OUTPUT_FILE)
    
    print(f"\n Processing {EXERCISE}")
    print(f" Input: {INPUT_PATH}")
    print(f" Output: {OUTPUT_PATH}\n")
    

    if not os.path.exists(INPUT_PATH):
        print(f" ERROR: Video file not found!")
        print(f"Looking for: {INPUT_PATH}")
        print(f"\nMake sure:")
        print(f"1. BASE_PATH points to your test folder")
        print(f"2. VIDEO_FILE matches your video name")
        print(f"3. File exists in the folder")
    else:
        
        processor = VideoProcessor(EXERCISE, INPUT_PATH, OUTPUT_PATH)
        processor.run_analysis()
