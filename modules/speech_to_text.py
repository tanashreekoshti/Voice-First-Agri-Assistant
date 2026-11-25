
import speech_recognition as sr
import io

# --------------------------------------------------
# SUPPORTED SPEECH RECOGNITION LANGUAGES
# --------------------------------------------------

LANGUAGE_CODES = {
    "English": "en-IN",
    "मराठी": "mr-IN",
    "हिन्दी": "hi-IN"
}


# --------------------------------------------------
# SPEECH TO TEXT FUNCTION
# --------------------------------------------------

def convert_audio_to_text(audio_bytes, language="en-IN"):

    """
    Converts recorded audio into text using Google Speech Recognition.

    Supported languages:
    English, Marathi and Hindi.
    """

    recognizer = sr.Recognizer()

    try:

        # Validate audio
        if not audio_bytes:
            return {
                "success": False,
                "text": "",
                "language": language,
                "error": "No audio received."
            }

        # Validate language
        supported_languages = ["en-IN", "mr-IN", "hi-IN"]

        if language not in supported_languages:
            return {
                "success": False,
                "text": "",
                "language": language,
                "error": "Unsupported speech recognition language."
            }

        # Read recorded WAV audio
        audio_file = sr.AudioFile(
            io.BytesIO(audio_bytes)
        )

        with audio_file as source:
            audio_data = recognizer.record(source)

        # Recognize speech using selected language
        recognized_text = recognizer.recognize_google(
            audio_data,
            language=language
        )

        return {
            "success": True,
            "text": recognized_text,
            "language": language,
            "error": None
        }

    except sr.UnknownValueError:

        return {
            "success": False,
            "text": "",
            "language": language,
            "error": "Speech could not be understood. Please speak clearly."
        }

    except sr.RequestError as error:

        return {
            "success": False,
            "text": "",
            "language": language,
            "error": f"Google Speech Recognition error: {error}"
        }

    except Exception as error:

        return {
            "success": False,
            "text": "",
            "language": language,
            "error": str(error)
        }
