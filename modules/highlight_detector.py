from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
import numpy as np

def detect_highlights(video_path, frame_duration=1.0, motion_threshold=70):
    video = VideoFileClip(video_path)
    duration = video.duration
    highlights = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * frame_duration)
    prev_gray = None
    motions = []
    times = []

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                diff = cv2.absdiff(gray, prev_gray)
                motion = np.mean(diff)
                motions.append(motion)
                times.append(frame_idx / fps)
            prev_gray = gray
        frame_idx += 1
    cap.release()

    # threshold 이상인 구간만 하이라이트로
    threshold = np.percentile(motions, motion_threshold)
    start = None
    for i, motion in enumerate(motions):
        if motion > threshold:
            if start is None:
                start = times[i]
        else:
            if start is not None:
                end = times[i]
                if end - start > 1.0:
                    highlights.append((start, end))
                start = None
    if start is not None:
        highlights.append((start, duration))
    return highlights
