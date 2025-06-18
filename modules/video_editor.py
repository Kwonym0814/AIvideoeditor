from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
import os

def edit_video(video_path, highlights):
    clips = []
    video = VideoFileClip(video_path)
    for start, end in highlights:
        clips.append(video.subclipped(start, end))
    if clips:
        final_clip = concatenate_videoclips(clips)
        output_path = os.path.splitext(video_path)[0] + '_highlight.mp4'
        # ffmpeg 인코딩 옵션 추가: -c:v hevc_nvenc -preset p5 -cq 20
        final_clip.write_videofile(
            output_path,
            codec='hevc_nvenc',
            preset='p5',
            ffmpeg_params=['-cq', '20']
        )
        return output_path
    else:
        return '하이라이트 구간이 없습니다.'
