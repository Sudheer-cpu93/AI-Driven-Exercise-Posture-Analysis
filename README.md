# AI-Driven Exercise Posture Analysis

Upload a workout video, pick an exercise, and get back a video with pose
landmarks and real-time form feedback drawn on it, plus a form-accuracy score.

Built on MediaPipe Pose + OpenCV. Supports: Push-Ups, Bodyweight Squats,
Lunges, Bench Press, Pull-Ups, Wall Push-Ups, Handstand Push-Ups, Jumping
Jacks, Clean and Jerk.

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Deploy for free — Streamlit Community Cloud

1. Push this repo to GitHub (see `.gitignore` — it already excludes the
   `venv/` folder, `__pycache__/`, and the large `Gym Exercises/` sample
   video folder; don't commit those).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **"New app"**, pick this repo/branch, and set the main file path to
   `app.py`.
4. Click **Deploy**. First build takes a few minutes (MediaPipe is a large
   dependency). You'll get a public `https://<your-app>.streamlit.app` URL.

### Notes
- `requirements.txt` pins `mediapipe==0.10.14`. Newer MediaPipe versions
  (0.10.15+) removed the legacy `mp.solutions` API this code depends on —
  don't bump that version without also updating `pose_detector.py` to the
  new Tasks API.
- Uses `opencv-python-headless` (not `opencv-python`) since there's no
  display on a server — the old desktop script's `cv2.imshow` live-preview
  window was removed; the web app instead lets you preview and download the
  processed video after analysis.
- Free tier apps sleep after inactivity and wake on the next visit (~30s
  cold start).

## Alternative: Hugging Face Spaces

Same repo works with no changes. Create a new Space → SDK: Streamlit →
upload `app.py`, `pose_detector.py`, `form_analyzer.py`, `utils.py`, and
`requirements.txt`.
