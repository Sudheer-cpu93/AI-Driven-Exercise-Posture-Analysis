import os
import tempfile

import cv2
import streamlit as st

from pose_detector import PoseDetector
from form_analyzer import FormAnalyzer
from utils import draw_feedback_box, draw_status

st.set_page_config(page_title="AI Exercise Posture Analysis", page_icon="🏋️", layout="centered")

EXERCISES = [
    "PushUps",
    "BodyWeightSquats",
    "Lunges",
    "BenchPress",
    "PullUps",
    "WallPushUps",
    "HandstandPushUps",
    "JumpingJack",
    "CleanAndJerk",
]

st.title("🏋️ AI-Driven Exercise Posture Analysis")
st.write(
    "Upload a short workout video, pick the exercise, and get back a video with "
    "live pose landmarks and form feedback drawn on it, plus a form-accuracy score."
)

exercise = st.selectbox("Exercise type", EXERCISES)
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])

run_button = st.button("Analyze video", type="primary", disabled=uploaded_file is None)


def process_video(exercise_type: str, input_path: str, output_path: str, progress_bar, status_text):
    pose_detector = PoseDetector()
    form_analyzer = FormAnalyzer(exercise_type)

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open uploaded video.")

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    perfect_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        image = frame.copy()

        try:
            pose_data = pose_detector.detect_pose(image)
            if pose_data is None:
                raise Exception("No pose detected")

            coords = pose_data["coords"]
            feedback, status = form_analyzer.analyze_frame(coords)

            if status == "PERFECT FORM":
                perfect_frames += 1

            image = pose_detector.draw_landmarks(image, pose_data)
            image = draw_status(image, status)
            image = draw_feedback_box(image, feedback)
            cv2.putText(
                image,
                f"Exercise: {exercise_type.upper()}",
                (10, image.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )
        except Exception as e:
            cv2.putText(image, "Pose not detected - adjust camera", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"Error: {str(e)[:50]}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        writer.write(image)

        if frame_count % 5 == 0 or frame_count == total_frames:
            progress = min(frame_count / total_frames, 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Processing frame {frame_count}/{total_frames}")

    cap.release()
    writer.release()
    pose_detector.close()

    accuracy = (perfect_frames / frame_count * 100) if frame_count else 0
    return frame_count, perfect_frames, accuracy


if run_button and uploaded_file is not None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = os.path.join(tmp_dir, "input_" + uploaded_file.name)
        output_path = os.path.join(tmp_dir, "output.mp4")

        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        progress_bar = st.progress(0)
        status_text = st.empty()

        with st.spinner("Analyzing form..."):
            try:
                frame_count, perfect_frames, accuracy = process_video(
                    exercise, input_path, output_path, progress_bar, status_text
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        status_text.empty()
        progress_bar.empty()

        st.success("Analysis complete!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Frames", frame_count)
        col2.metric("Perfect Form Frames", perfect_frames)
        col3.metric("Form Accuracy", f"{accuracy:.1f}%")

        with open(output_path, "rb") as f:
            video_bytes = f.read()

        st.video(video_bytes)
        st.download_button(
            "Download analyzed video",
            data=video_bytes,
            file_name=f"{exercise}_analyzed.mp4",
            mime="video/mp4",
        )
elif uploaded_file is None:
    st.info("Upload a video to get started.")
