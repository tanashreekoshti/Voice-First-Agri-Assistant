
import re


def detect_language(text):

    text = text.strip().lower()

    if not text:
        return "English"

    # Detect Devanagari characters
    devanagari_count = len(
        re.findall(r"[\u0900-\u097F]", text)
    )

    if devanagari_count == 0:
        return "English"

    # Common Marathi words
    marathi_words = [
        "कसे", "कशी", "कसा", "करावे", "करावी",
        "आहे", "आहेत", "माझ्या", "मला", "शेतात",
        "पेरणी", "किती", "कधी", "कोणते", "काय"
    ]

    # Common Hindi words
    hindi_words = [
        "कैसे", "कैसी", "कैसा", "करें", "करना",
        "है", "हैं", "मेरा", "मुझे", "खेत",
        "बुवाई", "कितना", "कब", "कौन", "क्या"
    ]

    marathi_score = sum(
        1 for word in marathi_words if word in text
    )

    hindi_score = sum(
        1 for word in hindi_words if word in text
    )

    if marathi_score > hindi_score:
        return "मराठी"

    if hindi_score > marathi_score:
        return "हिन्दी"

    # Use selected language as a fallback
    return "Unknown"


if __name__ == "__main__":

    test_questions = [
        "How to sow soybean?",
        "सोयाबीन पेरणी कशी करावी?",
        "सोयाबीन की बुवाई कैसे करें?"
    ]

    for question in test_questions:
        print("Question:", question)
        print("Language:", detect_language(question))
        print()


