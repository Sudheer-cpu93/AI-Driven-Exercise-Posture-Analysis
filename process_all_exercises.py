import sys
import os
import glob

sys.path.insert(0, 'src')
from video_processor import VideoProcessor

# ============================================================================
# CONFIGURATION
# ============================================================================

# Your base folder containing all exercise folders
BASE_PATH = r"D:\CV_Project\Gym Exercises"

# Which exercises to process (for submission, pick your best 3)
EXERCISES_TO_PROCESS = [
    'PushUps',          # Recommended #1
    'BodyWeightSquats', # Recommended #2
    'Lunges',           # Recommended #3
    # 'BenchPress',
    # 'PullUps',
    # 'WallPushups',
]

# Output folder
OUTPUT_FOLDER = r"D:\CV_Project\Gym Exercises\Output"

# ============================================================================


def find_videos_in_folder(folder_path):
    """Find all video files in a folder"""
    video_extensions = ['*.avi', '*.mp4', '*.mov', '*.mkv']
    videos = []
    
    for ext in video_extensions:
        pattern = os.path.join(folder_path, ext)
        videos.extend(glob.glob(pattern))
    
    return videos


def main():
    """Process all selected exercises"""
    print("\n" + ""*30)
    print("BATCH EXERCISE PROCESSING")
    print(""*30 + "\n")
    
    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    total_videos = 0
    successful = 0
    failed_videos = []
    
    # Process each exercise
    for exercise in EXERCISES_TO_PROCESS:
        print(f"\n{'='*60}")
        print(f"PROCESSING: {exercise.upper()}")
        print(f"{'='*60}\n")
        
        # Build folder path
        exercise_folder = os.path.join(BASE_PATH, exercise)
        
        # Check if folder exists
        if not os.path.exists(exercise_folder):
            print(f"  WARNING: Folder not found: {exercise_folder}")
            print(f"Skipping {exercise}\n")
            continue
        
        # Find all videos in this folder
        videos = find_videos_in_folder(exercise_folder)
        
        if not videos:
            print(f"  No videos found in {exercise_folder}")
            print(f"Skipping {exercise}\n")
            continue
        
        print(f"Found {len(videos)} video(s) in {exercise} folder:")
        for v in videos:
            print(f"  - {os.path.basename(v)}")
        print()
        
        # Process each video
        for video_path in videos:
            total_videos += 1
            video_name = os.path.basename(video_path)
            base_name = os.path.splitext(video_name)[0]
            
            # Create output path
            output_name = f"{exercise.lower()}_{base_name}_analyzed.mp4"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)
            
            print(f"Processing: {video_name}")
            print(f"Output: {output_name}\n")
            
            try:
                # Process video
                processor = VideoProcessor(exercise, video_path, output_path)
                processor.run_analysis()
                
                successful += 1
                print(f" Successfully processed: {video_name}\n")
                
            except Exception as e:
                print(f" ERROR processing {video_name}: {e}\n")
                failed_videos.append((exercise, video_name, str(e)))
    
    # Final summary
    print("\n" + "="*60)
    print("BATCH PROCESSING COMPLETE")
    print("="*60)
    print(f"Total videos found: {total_videos}")
    print(f" Successfully processed: {successful}")
    print(f" Failed: {len(failed_videos)}")
    
    if failed_videos:
        print("\nFailed videos:")
        for exercise, video, error in failed_videos:
            print(f"  - {exercise}/{video}: {error[:50]}")
    
    print(f"\n All outputs saved to: {OUTPUT_FOLDER}")
    print("="*60 + "\n")
    
    # List output files
    output_files = glob.glob(os.path.join(OUTPUT_FOLDER, "*.mp4"))
    if output_files:
        print(f"Generated {len(output_files)} output video(s):")
        for f in output_files:
            print(f"  ✓ {os.path.basename(f)}")
    
    print("\n Done! Check your output folder for results.")


if __name__ == "__main__":
    main()