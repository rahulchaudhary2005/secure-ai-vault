from moviepy import VideoFileClip

class VideoParser:

    @staticmethod
    def extract_metadata(file_path: str):

        clip = VideoFileClip(file_path)

        return {
            "duration": clip.duration,
            "fps": clip.fps,
            "size": clip.size
        }