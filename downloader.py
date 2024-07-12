import yt_dlp
import uuid
from moviepy.editor import VideoFileClip
import os
import ffmpeg

def downloadVideo(url, file_type, output_path=None):
    """
    Downloads a YouTube video from the given URL.
    
    Args:
        url (str): The URL of the YouTube video.
        file_type (str): The type of download file, can be 'mp4', 'wmv', or 'mp3'.
        output_path (str, optional): The path to save the downloaded video file.
            If not provided, the video will be saved in the current directory.
    
    Returns:
        video_path (str): The path where the video file was saved.
        video_name (str): Filename which is randomly generated.
        original_title (str): The original title of the YouTube video.
    """
    video_name = str(uuid.uuid4())
    copy_name = video_name  # For WMV conversion
    
    ydl_opts = {}
    if file_type == 'mp4' or file_type == 'wmv':
        copy_name += ".mp4"
        ydl_opts = {
            'format': 'bestvideo+bestaudio[ext=m4a]/best',
            'outtmpl': os.path.join(output_path if output_path else '', video_name),
            'merge_output_format': 'mp4'
        }
    elif file_type == 'mp3':
        copy_name += ".mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path if output_path else '', video_name),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        original_title = info_dict.get('title', None)
    
    video_path = output_path if output_path else os.getcwd()

    # Use moviepy to convert video file from MP4 to WMV
    if file_type == "wmv":
        if output_path:
            video_file = os.path.join(output_path, video_name)
            VideoFileClip(video_file).write_videofile(f"{output_path}/{copy_name}.wmv", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="wmv2", audio_codec="aac")
        else:
            VideoFileClip(video_name).write_videofile(f"{copy_name}.wmv", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="wmv2", audio_codec="aac")
        if os.path.exists(video_file):
            os.remove(video_file)
        copy_name = copy_name + ".wmv"
    
    print("Video downloaded successfully")
    return copy_name , video_path, original_title

# # Example usage:
# if __name__ == "__main__":
#     video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#     file_type = 'mp4'  # Change to 'wmv' or 'mp3' as needed
#     download_video(video_url, file_type)
