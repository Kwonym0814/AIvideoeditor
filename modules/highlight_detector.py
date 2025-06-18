from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
import numpy as np

def merge_and_expand_highlights(highlights, min_gap=3.0, expand=1.0, duration=None):
    if not highlights:
        return []
    merged = []
    prev_start, prev_end = highlights[0]
    for start, end in highlights[1:]:
        if start - prev_end < min_gap:
            prev_end = end  # 구간 병합
        else:
            merged.append((max(0, prev_start - expand), min(prev_end + expand, duration)))
            prev_start, prev_end = start, end
    merged.append((max(0, prev_start - expand), min(prev_end + expand, duration)))
    return merged

def detect_highlights(video_path, frame_duration=1.0, motion_threshold=50):
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

    threshold = np.percentile(motions, motion_threshold)
    raw_highlights = []
    start = None
    for i, motion in enumerate(motions):
        if motion > threshold:
            if start is None:
                start = times[i]
        else:
            if start is not None:
                end = times[i]
                if end - start > 1.0:
                    raw_highlights.append((start, end))
                start = None
    if start is not None:
        raw_highlights.append((start, duration))
    # 구간 병합 및 확장 적용
    highlights = merge_and_expand_highlights(raw_highlights, min_gap=3.0, expand=1.0, duration=duration)
    return highlights
