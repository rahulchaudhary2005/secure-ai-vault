from mutagen import File

class AudioParser:

    @staticmethod
    def extract_metadata(file_path: str):

        audio = File(file_path)

        if not audio:
            return {}

        return {
            "length": audio.info.length if audio.info else None,
            "bitrate": getattr(audio.info, "bitrate", None)
        }