import cv2
import moviepy.editor as mp
from moviepy.editor import VideoFileClip
import magic  # To detect MIME type
import os

def get_mimetype(file_path):
    """
    Detects the MIME type of a file (e.g., video file) using python-magic.
    """
    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(file_path)
    return mimetype

def extract_frames_from_video(video_path):
    """
    Extracts frames from a video file and returns them as a list of frames.
    """
    try:
        video = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = video.read()
            if not ret:
                break
            frames.append(frame)
        video.release()
        return frames
    except Exception as e:
        return f"Error extracting frames: {str(e)}"

def process_video(video_path, output_path):
    """
    Processes a video by trimming the first 10 seconds and saving it to a new file.
    """
    try:
        # Check MIME type of the input video file
        mimetype = get_mimetype(video_path)
        print(f"Detected MIME type: {mimetype}")

        # Ensure the file is a valid video format
        if not mimetype.startswith('video'):
            raise ValueError(f"Provided file is not a video. MIME type: {mimetype}")

        # Processing the video using MoviePy
        clip = VideoFileClip(video_path)
        clip = clip.subclip(0, 10)  # Trim the first 10 seconds
        clip.write_videofile(output_path, codec='libx264')
        return output_path
    except Exception as e:
        return f"Error processing video: {str(e)}"

def process_video_file(video_path, output_path):
    """
    Processes the video file: extract frames, trim, and return processed video.
    """
    mimetype = get_mimetype(video_path)
    print(f"Detected MIME type: {mimetype}")

    # Extract frames from the video
    frames = extract_frames_from_video(video_path)

    # Process the video (trim and save)
    processed_video = process_video(video_path, output_path)

    return {
        "mimetype": mimetype,
        "frames_extracted": len(frames),
        "processed_video": processed_video
    }

# Example usage
video_path = "path_to_your_video.mp4"
output_path = "path_to_output_video.mp4"
result = process_video_file(video_path, output_path)
print(result)
