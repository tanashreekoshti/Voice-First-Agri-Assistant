
import requests

# --------------------------------------------------
# BHASINI TRANSLATION API CONFIGURATION
# --------------------------------------------------

API_URL = "https://mcp.bhasini.com/v1/translate"

LANGUAGE_CODES = {
    "English": "en",
    "मराठी": "mr",
    "हिन्दी": "hi"
}


# --------------------------------------------------
# CORE TRANSLATION FUNCTION
# --------------------------------------------------

def translate_text(text, source_language, target_language):

    """
    Translates text using the Bhasini Translation API.

    Supported languages:
    English (en), Marathi (mr), Hindi (hi)
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "success": False,
            "translation": "",
            "error": "Empty text provided."
        }

    if source_language == target_language:
        return {
            "success": True,
            "translation": text,
            "error": None
        }

    payload = {
        "text": text,
        "source": source_language,
        "target": target_language
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        translated_text = data.get("translation")

        if not translated_text:
            return {
                "success": False,
                "translation": "",
                "error": "Translation missing in API response."
            }

        return {
            "success": True,
            "translation": translated_text,
            "error": None
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "translation": "",
            "error": "Translation request timed out."
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "translation": "",
            "error": f"Translation API connection failed: {error}"
        }

    except ValueError:

        return {
            "success": False,
            "translation": "",
            "error": "Invalid response received from translation API."
        }


# --------------------------------------------------
# FARMER QUESTION: REGIONAL LANGUAGE TO ENGLISH
# --------------------------------------------------

def translate_to_english(query, detected_language):

    """
    Converts a farmer's Marathi or Hindi question
    into English for agricultural document retrieval.
    """

    source_code = LANGUAGE_CODES.get(detected_language)

    if source_code is None:
        return {
            "success": False,
            "translation": "",
            "error": "Unsupported source language."
        }

    return translate_text(
        query,
        source_code,
        "en"
    )


# --------------------------------------------------
# ADVISORY ANSWER: ENGLISH TO REGIONAL LANGUAGE
# --------------------------------------------------

def translate_from_english(text, target_language):

    """
    Translates retrieved English agricultural information
    into the farmer's selected language.
    """

    target_code = LANGUAGE_CODES.get(target_language)

    if target_code is None:
        return {
            "success": False,
            "translation": "",
            "error": "Unsupported target language."
        }

    return translate_text(
        text,
        "en",
        target_code
    )


# --------------------------------------------------
# COMPATIBILITY FUNCTION
# --------------------------------------------------

def translate_agri_query(query, detected_language=None):

    """
    Compatibility wrapper for the existing app.

    English queries are returned unchanged.
    Marathi and Hindi queries are translated into English.
    """

    if detected_language == "English":
        return {
            "success": True,
            "translation": query,
            "error": None
        }

    if detected_language not in ["मराठी", "हिन्दी"]:
        return {
            "success": False,
            "translation": "",
            "error": "Please provide a supported language."
        }

    return translate_to_english(
        query,
        detected_language
    )


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    test_questions = [
        ("सोयाबीन पेरणी कशी करावी?", "मराठी"),
        ("गेहूं की बुवाई कैसे करें?", "हिन्दी"),
        ("How to sow soybean?", "English")
    ]

    for question, language in test_questions:

        print("\nOriginal question:", question)
        print("Detected language:", language)

        if language == "English":

            result = {
                "success": True,
                "translation": question,
                "error": None
            }

        else:

            result = translate_to_english(
                question,
                language
            )

        if result["success"]:

            print(
                "English query:",
                result["translation"]
            )

        else:

            print("Error:", result["error"])


    # Test English-to-Marathi answer translation

    print("\n--- ANSWER TRANSLATION TEST ---")

    sample_answer = (
        "Use certified soybean seeds and follow "
        "the recommended sowing time for your region."
    )

    result = translate_from_english(
        sample_answer,
        "मराठी"
    )

    if result["success"]:

        print("Marathi answer:", result["translation"])

    else:

        print("Error:", result["error"])
