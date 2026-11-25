
from gtts import gTTS
import io

LANGUAGE_CODES = {
    "English": "en",
    "मराठी": "mr",
    "हिन्दी": "hi"
}


def convert_text_to_audio(text, language):

    """
    Converts text into speech using Google Text-to-Speech.
    Retries once if the connection temporarily fails.
    """

    import io
    import time
    from gtts import gTTS

    if not text or not text.strip():
        return None

    language_code = LANGUAGE_CODES.get(language)

    if not language_code:
        return None

    for attempt in range(2):

        try:
            speech = gTTS(
                text=text,
                lang=language_code,
                timeout=(10, 30)
            )

            audio_buffer = io.BytesIO()
            speech.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            return audio_buffer

        except Exception as error:

            print("Text-to-Speech Error:", error)

            if attempt == 0:
                time.sleep(2)

    return None

