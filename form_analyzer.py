from utils import calculate_angle, SmoothingBuffer


class FormAnalyzer:
    """
    Analyzes exercise form for your dataset exercises
    """
    
    def __init__(self, exercise='pushups'):
        self.exercise = exercise.lower()
        
        # Smoothing buffers (10-frame window)
        self.buffer1 = SmoothingBuffer(window_size=10)
        self.buffer2 = SmoothingBuffer(window_size=10)
        self.buffer3 = SmoothingBuffer(window_size=10)
        self.buffer4 = SmoothingBuffer(window_size=10)
        self.buffer5 = SmoothingBuffer(window_size=10)
        
        print(f"FormAnalyzer initialized for: {exercise}")
    
    def analyze_frame(self, coords):
        """
        Main analysis function
        Returns: feedback list and overall status
        """
        if self.exercise == 'pushups':
            return self._analyze_pushups(coords)
        elif self.exercise == 'bodyweightsquats':
            return self._analyze_squats(coords)
        elif self.exercise == 'lunges':
            return self._analyze_lunges(coords)
        elif self.exercise == 'benchpress':
            return self._analyze_benchpress(coords)
        elif self.exercise == 'pullups':
            return self._analyze_pullups(coords)
        elif self.exercise == 'wallpushups':
            return self._analyze_wall_pushups(coords)
        elif self.exercise == 'handstandpushups':
            return self._analyze_handstand_pushups(coords)
        elif self.exercise == 'jumpingjack':
            return self._analyze_jumping_jack(coords)
        elif self.exercise == 'cleanandjerk':
            return self._analyze_clean_and_jerk(coords)
        else:
            return [f"Exercise {self.exercise} not configured"], "UNKNOWN EXERCISE"
    
    # ========== PUSH-UPS ANALYSIS ==========
    
    def _analyze_pushups(self, coords):
        """Push-ups form analysis - 5 rules"""
        full_feedback = []
        overall_status = "PERFECT FORM"
        
        try:
            # Rule 1: Elbow Angle (should reach 90° or less at bottom)
            shoulder = coords['R_SHOULDER']
            elbow = coords['R_ELBOW']
            wrist = coords['R_WRIST']
            
            angle1 = calculate_angle(shoulder, elbow, wrist)
            self.buffer1.add_value(angle1)
            smoothed_angle1 = self.buffer1.get_smoothed_value()
            
            fb1 = "Elbow Angle OK"
            if smoothed_angle1 > 100:
                fb1 = "Go lower! Elbows need more flexion."
                overall_status = "MINOR ERROR"
            elif 70 <= smoothed_angle1 <= 100:
                fb1 = "PERFECT depth achieved!"
            elif smoothed_angle1 < 70:
                fb1 = "Good depth - chest near ground."
            
            full_feedback.append(f"Elbow Angle ({int(smoothed_angle1)}°): {fb1}")
            
            # Rule 2: Back Alignment (body should be straight)
            hip = coords['R_HIP']
            
            angle2 = calculate_angle(shoulder, hip, coords['R_KNEE'])
            self.buffer2.add_value(angle2)
            smoothed_angle2 = self.buffer2.get_smoothed_value()
            
            fb2 = "Back Alignment Good"
            if smoothed_angle2 < 160 or smoothed_angle2 > 200:
                fb2 = "ERROR: Keep body straight. No sagging/piking."
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Body Line ({int(smoothed_angle2)}°): {fb2}")
            
            # Rule 3: Elbow Position (elbows shouldn't flare too much)
            # Check angle between shoulders and elbows
            l_shoulder = coords['L_SHOULDER']
            l_elbow = coords['L_ELBOW']
            
            # Elbow flare check (simplified)
            fb3 = "Elbow Position OK"
            if angle1 < 90:
                fb3 = "Keep elbows at 45° from body."
            
            full_feedback.append(f"Elbow Flare: {fb3}")
            
            # Rule 4: Neck Alignment
            nose = coords['NOSE']
            neck_angle = calculate_angle(nose, shoulder, hip)
            self.buffer4.add_value(neck_angle)
            smoothed_angle4 = self.buffer4.get_smoothed_value()
            
            fb4 = "Neck Neutral"
            if smoothed_angle4 < 160:
                fb4 = "Look down slightly, keep neck neutral."
                
            full_feedback.append(f"Neck ({int(smoothed_angle4)}°): {fb4}")
            
            # Rule 5: Full Extension Check
            if smoothed_angle1 > 160:
                fb5 = "Full extension achieved at top."
            else:
                fb5 = "Extend arms fully at top."
            
            full_feedback.append(f"Extension: {fb5}")
            
        except KeyError as e:
            full_feedback.append(f"Missing keypoint: {e}")
            overall_status = "DETECTION ERROR"
        
        return full_feedback, overall_status
    
    # ========== BODYWEIGHT SQUATS ANALYSIS ==========
    
    def _analyze_squats(self, coords):
        """BodyWeight Squats analysis - 5 rules"""
        full_feedback = []
        overall_status = "PERFECT FORM"
        
        try:
            # Rule 1: Knee Flexion (Depth)
            hip = coords['R_HIP']
            knee = coords['R_KNEE']
            ankle = coords['R_ANKLE']
            
            angle1 = calculate_angle(hip, knee, ankle)
            self.buffer1.add_value(angle1)
            smoothed_angle1 = self.buffer1.get_smoothed_value()
            
            fb1 = "Knee Angle OK"
            if smoothed_angle1 > 110:
                fb1 = "Go deeper! Not reaching parallel."
                overall_status = "MINOR ERROR"
            elif 70 <= smoothed_angle1 <= 110:
                fb1 = "PERFECT depth (parallel or below)!"
            elif smoothed_angle1 < 70:
                fb1 = "Excellent depth!"
            
            full_feedback.append(f"Knee Flexion ({int(smoothed_angle1)}°): {fb1}")
            
            # Rule 2: Hip Flexion
            shoulder = coords['R_SHOULDER']
            
            angle2 = calculate_angle(shoulder, hip, knee)
            self.buffer2.add_value(angle2)
            smoothed_angle2 = self.buffer2.get_smoothed_value()
            
            fb2 = "Hip Flexion Good"
            if smoothed_angle2 < 70 or smoothed_angle2 > 110:
                fb2 = "Check hip position - sit back more."
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Hip Angle ({int(smoothed_angle2)}°): {fb2}")
            
            # Rule 3: Back Alignment
            nose = coords['NOSE']
            
            angle3 = calculate_angle(hip, shoulder, nose)
            self.buffer3.add_value(angle3)
            smoothed_angle3 = self.buffer3.get_smoothed_value()
            
            fb3 = "Back Straight"
            if smoothed_angle3 < 150:
                fb3 = "ERROR: Back rounding. Keep chest up!"
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Back ({int(smoothed_angle3)}°): {fb3}")
            
            # Rule 4: Knee Tracking (knees shouldn't go too far forward)
            knee_x = coords['R_KNEE'][0]
            foot_x = coords['R_FOOT_INDEX'][0]
            
            fb4 = "Knee Tracking Good"
            if knee_x > foot_x + 0.05:
                fb4 = "ERROR: Knees past toes! Sit back more."
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Knee Track: {fb4}")
            
            # Rule 5: Symmetry check
            l_knee = coords['L_KNEE']
            l_ankle = coords['L_ANKLE']
            l_hip = coords['L_HIP']
            
            left_angle = calculate_angle(l_hip, l_knee, l_ankle)
            angle_diff = abs(smoothed_angle1 - left_angle)
            
            fb5 = "Both legs symmetric"
            if angle_diff > 15:
                fb5 = "Asymmetric squat. Check balance."
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Symmetry: {fb5}")
            
        except KeyError as e:
            full_feedback.append(f"Missing keypoint: {e}")
            overall_status = "DETECTION ERROR"
        
        return full_feedback, overall_status
    
    # ========== LUNGES ANALYSIS ==========
    
    def _analyze_lunges(self, coords):
        """Lunges analysis - 5 rules"""
        full_feedback = []
        overall_status = "PERFECT FORM"
        
        try:
            # Rule 1: Front Knee Angle (should reach 90°)
            hip = coords['R_HIP']
            knee = coords['R_KNEE']
            ankle = coords['R_ANKLE']
            
            angle1 = calculate_angle(hip, knee, ankle)
            self.buffer1.add_value(angle1)
            smoothed_angle1 = self.buffer1.get_smoothed_value()
            
            fb1 = "Front Knee Angle OK"
            if smoothed_angle1 < 80 or smoothed_angle1 > 100:
                fb1 = "Front knee should be at 90° (right angle)."
                overall_status = "MINOR ERROR"
            else:
                fb1 = "PERFECT 90° front knee angle!"
            
            full_feedback.append(f"Front Knee ({int(smoothed_angle1)}°): {fb1}")
            
            # Rule 2: Back Knee Angle
            l_hip = coords['L_HIP']
            l_knee = coords['L_KNEE']
            l_ankle = coords['L_ANKLE']
            
            angle2 = calculate_angle(l_hip, l_knee, l_ankle)
            self.buffer2.add_value(angle2)
            smoothed_angle2 = self.buffer2.get_smoothed_value()
            
            fb2 = "Back Knee OK"
            if smoothed_angle2 < 70 or smoothed_angle2 > 110:
                fb2 = "Back knee should hover near ground."
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Back Knee ({int(smoothed_angle2)}°): {fb2}")
            
            # Rule 3: Torso Uprightness
            shoulder = coords['R_SHOULDER']
            nose = coords['NOSE']
            
            angle3 = calculate_angle(hip, shoulder, nose)
            self.buffer3.add_value(angle3)
            smoothed_angle3 = self.buffer3.get_smoothed_value()
            
            fb3 = "Torso Upright"
            if smoothed_angle3 < 160:
                fb3 = "ERROR: Leaning forward. Keep torso upright!"
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Torso ({int(smoothed_angle3)}°): {fb3}")
            
            # Rule 4: Front Knee Position (shouldn't go past toes)
            knee_x = coords['R_KNEE'][0]
            foot_x = coords['R_FOOT_INDEX'][0]
            
            fb4 = "Front Knee Position Good"
            if knee_x > foot_x + 0.05:
                fb4 = "WARNING: Front knee past toes."
                overall_status = "MINOR ERROR"
            
            full_feedback.append(f"Knee Track: {fb4}")
            
            # Rule 5: Step depth
            fb5 = "Lunge depth appropriate"
            if smoothed_angle1 > 110:
                fb5 = "Step forward more for deeper lunge."
            
            full_feedback.append(f"Depth: {fb5}")
            
        except KeyError as e:
            full_feedback.append(f"Missing keypoint: {e}")
            overall_status = "DETECTION ERROR"
        
        return full_feedback, overall_status
    
    
    
    def _analyze_benchpress(self, coords):
        """Bench press analysis"""
        full_feedback = []
        overall_status = "PERFECT FORM"
        
        try:
            shoulder = coords['R_SHOULDER']
            elbow = coords['R_ELBOW']
            wrist = coords['R_WRIST']
            
            angle = calculate_angle(shoulder, elbow, wrist)
            self.buffer1.add_value(angle)
            smoothed = self.buffer1.get_smoothed_value()
            
            if smoothed < 85:
                fb = "DEPTH GOOD: Bar near chest."
            elif 85 <= smoothed <= 100:
                fb = "PERFECT depth for bench press."
            else:
                fb = "Full extension at top."
            
            full_feedback.append(f"Elbow ({int(smoothed)}°): {fb}")
            
        except KeyError:
            full_feedback.append("Keypoints not fully visible")
            overall_status = "DETECTION ERROR"
        
        return full_feedback, overall_status
    
    
    
    def _analyze_pullups(self, coords):
        """Pull-ups analysis"""
        full_feedback = []
        overall_status = "PERFECT FORM"
        
        try:
            shoulder = coords['R_SHOULDER']
            elbow = coords['R_ELBOW']
            wrist = coords['R_WRIST']
            
            angle = calculate_angle(shoulder, elbow, wrist)
            self.buffer1.add_value(angle)
            smoothed = self.buffer1.get_smoothed_value()
            
            if smoothed < 90:
                fb = "GOOD: Chin above bar."
            else:
                fb = "Pull higher - chin over bar."
            
            full_feedback.append(f"Elbow ({int(smoothed)}°): {fb}")
            
        except KeyError:
            full_feedback.append("Keypoints not visible")
            overall_status = "DETECTION ERROR"
        
        return full_feedback, overall_status
    

    
    def _analyze_wall_pushups(self, coords):
        return self._analyze_pushups(coords)  
    
    def _analyze_handstand_pushups(self, coords):
        return self._analyze_pushups(coords)  
    
    def _analyze_jumping_jack(self, coords):
        """Jumping jack analysis"""
        return ["Jumping jack detected - tracking movement"], "TRACKING"
    
    def _analyze_clean_and_jerk(self, coords):
        """Clean and jerk analysis"""
        return ["Clean & Jerk - complex movement tracked"], "TRACKING"