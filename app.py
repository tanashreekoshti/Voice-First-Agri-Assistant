
import streamlit as st

from modules.weather import get_weather, extract_weather_location
from modules.mandi_prices import get_mandi_prices
from modules.government_schemes import search_scheme
from modules.crop_advisory import search_crop_advisory
from modules.language import detect_language
from modules.translator import translate_agri_query, translate_from_english
from modules.speech_to_text import convert_audio_to_text
from modules.text_to_speech import convert_text_to_audio

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Agricultural Assistant",
    page_icon="🌾",
    layout="wide"
)


# --------------------------------------------------
# SESSION-LEVEL TRANSLATION CACHE
# --------------------------------------------------

if "translation_cache" not in st.session_state:
    st.session_state["translation_cache"] = {}


def cached_translate_query(text, detected_language):
    key = ("query", text.strip(), detected_language)
    cache = st.session_state["translation_cache"]

    if key in cache:
        return cache[key]

    result = translate_agri_query(text.strip(), detected_language)

    # Cache successful translations only; failed API calls can be retried.
    if result.get("success"):
        cache[key] = result

    return result


def cached_translate_advisory(text, target_language):
    key = ("advisory", text, target_language)
    cache = st.session_state["translation_cache"]

    if key in cache:
        return cache[key]

    result = translate_from_english(text, target_language)

    # Cache successful translations only; failed API calls can be retried.
    if result.get("success"):
        cache[key] = result

    return result




# --------------------------------------------------
# LANGUAGE TRANSLATIONS
# --------------------------------------------------

translations = {
    "English": {
        "home": "Home",
        "weather": "Weather Information",
        "mandi": "Mandi Prices",
        "schemes": "Government Schemes",
        "crop": "Crop Advisory",
        "choose": "Choose a service",
        "title": "Voice-First Agricultural Assistant",
        "tagline": "Your digital agricultural assistant for crop guidance, government schemes, mandi prices and weather information.",
        "prototype": "Initial prototype: Text-based interaction. Voice support will be added in a later phase.",
        "welcome": "Welcome, Farmer!",
        "select_service": "Select a service to get agricultural information.",
        "weather_desc": "Check current weather conditions.",
        "schemes_desc": "Search information about farmer welfare schemes.",
        "mandi_desc": "Find agricultural market prices.",
        "crop_desc": "Search crop cultivation and pest-management guidance.",
        "current_weather": "Current weather for Pune (default location).",
        "get_weather": "Get Current Weather",
        "fetching_weather": "Fetching weather information...",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind": "Wind Speed",
        "datetime": "Date and Time",
        "precipitation": "Precipitation",
        "rainfall": "Rainfall",
        "weather_error": "Unable to retrieve weather information.",
        "mandi_title": "Agricultural Mandi Prices",
        "state": "Enter State",
        "district": "Enter District",
        "commodity": "Enter Commodity",
        "search_mandi": "Search Mandi Prices",
        "no_markets": "No matching market records found.",
        "found_markets": "Found",
        "records": "matching market records.",
        "arrival_date": "Arrival Date",
        "minimum_price": "Minimum Price",
        "maximum_price": "Maximum Price",
        "modal_price": "Modal Price",
        "variety": "Variety",
        "price_note": "Prices are from the downloaded dataset. Check the arrival date and price unit before use.",
        "fill_fields": "Please enter all three search fields.",
        "schemes_title": "Government Schemes",
        "scheme_query": "Enter scheme name or keyword",
        "scheme_placeholder": "Example: PM KISAN",
        "search_schemes": "Search Schemes",
        "eligibility": "Eligibility",
        "benefits": "Benefits",
        "official_source": "Official Source",
        "no_scheme": "No matching scheme found.",
        "enter_scheme": "Please enter a scheme name.",
        "crop_title": "Agricultural Crop Advisory",
        "crop_query": "Ask a crop-related question",
        "crop_placeholder": "Example: soybean sowing",
        "search_crop": "Search Crop Advisory",
        "searching_crop": "Searching agricultural documents...",
        "result": "Result",
        "topic": "Topic",
        "source": "Source",
        "page": "Page",
        "year": "Publication year",
        "general": "General",
        "crop_warning": "Retrieved information must be checked against current local agricultural guidance. Do not use pesticide dosage instructions without official verification.",
        "no_crop": "No sufficiently relevant crop information found.",
        "enter_crop": "Please enter a crop-related question.",
        "footer": "Agricultural Assistant Prototype | Designed to support Indian farmers"
    },

    "मराठी": {
        "home": "मुख्यपृष्ठ",
        "weather": "हवामान माहिती",
        "mandi": "बाजारभाव",
        "schemes": "सरकारी योजना",
        "crop": "पीक सल्ला",
        "choose": "सेवा निवडा",
        "title": "आवाजावर आधारित कृषी सहाय्यक",
        "tagline": "पीक मार्गदर्शन, सरकारी योजना, बाजारभाव आणि हवामान माहितीसाठी तुमचा डिजिटल कृषी सहाय्यक.",
        "prototype": "प्रारंभिक प्रोटोटाइप: मजकूर आधारित संवाद. आवाजाची सुविधा पुढील टप्प्यात जोडली जाईल.",
        "welcome": "शेतकरी मित्रांनो, आपले स्वागत आहे!",
        "select_service": "कृषीविषयक माहिती मिळवण्यासाठी सेवा निवडा.",
        "weather_desc": "सध्याची हवामान परिस्थिती तपासा.",
        "schemes_desc": "शेतकरी कल्याणकारी योजनांची माहिती शोधा.",
        "mandi_desc": "शेतमालाचे बाजारभाव जाणून घ्या.",
        "crop_desc": "पीक लागवड आणि कीड व्यवस्थापनाविषयी मार्गदर्शन मिळवा.",
        "current_weather": "पुणे येथील सध्याचे हवामान (मूळ स्थान).",
        "get_weather": "सध्याचे हवामान मिळवा",
        "fetching_weather": "हवामानाची माहिती मिळवत आहे...",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "wind": "वाऱ्याचा वेग",
        "datetime": "दिनांक आणि वेळ",
        "precipitation": "पर्जन्य",
        "rainfall": "पाऊस",
        "weather_error": "हवामानाची माहिती मिळवता आली नाही.",
        "mandi_title": "कृषी बाजारभाव",
        "state": "राज्याचे नाव टाका",
        "district": "जिल्ह्याचे नाव टाका",
        "commodity": "पिकाचे नाव टाका",
        "search_mandi": "बाजारभाव शोधा",
        "no_markets": "जुळणारी बाजारपेठेची नोंद आढळली नाही.",
        "found_markets": "आढळलेल्या बाजारपेठेच्या नोंदी:",
        "records": "नोंदी",
        "arrival_date": "आवक दिनांक",
        "minimum_price": "किमान किंमत",
        "maximum_price": "कमाल किंमत",
        "modal_price": "प्रचलित किंमत",
        "variety": "जात",
        "price_note": "किंमती डाउनलोड केलेल्या डेटासेटमधील आहेत. वापरण्यापूर्वी आवक दिनांक आणि किंमतीचे एकक तपासा.",
        "fill_fields": "कृपया तिन्ही माहिती भरा.",
        "schemes_title": "सरकारी योजना",
        "scheme_query": "योजनेचे नाव किंवा शब्द टाका",
        "scheme_placeholder": "उदाहरण: PM KISAN",
        "search_schemes": "योजना शोधा",
        "eligibility": "पात्रता",
        "benefits": "लाभ",
        "official_source": "अधिकृत स्रोत",
        "no_scheme": "जुळणारी योजना आढळली नाही.",
        "enter_scheme": "कृपया योजनेचे नाव टाका.",
        "crop_title": "कृषी पीक सल्ला",
        "crop_query": "पिकासंबंधी प्रश्न विचारा",
        "crop_placeholder": "उदाहरण: soybean sowing",
        "search_crop": "पीक सल्ला शोधा",
        "searching_crop": "कृषीविषयक कागदपत्रे शोधत आहे...",
        "result": "निकाल",
        "topic": "विषय",
        "source": "स्रोत",
        "page": "पृष्ठ",
        "year": "प्रकाशन वर्ष",
        "general": "सामान्य",
        "crop_warning": "मिळालेली माहिती स्थानिक कृषी तज्ज्ञांच्या सध्याच्या मार्गदर्शनाशी तपासा. अधिकृत पडताळणीशिवाय कीटकनाशकांचे प्रमाण वापरू नका.",
        "no_crop": "पुरेशी संबंधित पीक माहिती आढळली नाही.",
        "enter_crop": "कृपया पिकासंबंधी प्रश्न विचारा.",
        "footer": "कृषी सहाय्यक प्रोटोटाइप | भारतीय शेतकऱ्यांच्या मदतीसाठी तयार"
    },

    "हिन्दी": {
        "home": "मुख्य पृष्ठ",
        "weather": "मौसम की जानकारी",
        "mandi": "मंडी भाव",
        "schemes": "सरकारी योजनाएँ",
        "crop": "फसल सलाह",
        "choose": "सेवा चुनें",
        "title": "आवाज़ आधारित कृषि सहायक",
        "tagline": "फसल मार्गदर्शन, सरकारी योजनाओं, मंडी भाव और मौसम की जानकारी के लिए आपका डिजिटल कृषि सहायक।",
        "prototype": "प्रारंभिक प्रोटोटाइप: टेक्स्ट आधारित बातचीत। आवाज़ की सुविधा अगले चरण में जोड़ी जाएगी।",
        "welcome": "किसान भाइयों, आपका स्वागत है!",
        "select_service": "कृषि संबंधी जानकारी प्राप्त करने के लिए सेवा चुनें।",
        "weather_desc": "वर्तमान मौसम की जानकारी प्राप्त करें।",
        "schemes_desc": "किसान कल्याण योजनाओं की जानकारी खोजें।",
        "mandi_desc": "कृषि उपज के मंडी भाव जानें।",
        "crop_desc": "फसल की खेती और कीट प्रबंधन संबंधी सलाह प्राप्त करें।",
        "current_weather": "पुणे का वर्तमान मौसम (डिफ़ॉल्ट स्थान)।",
        "get_weather": "वर्तमान मौसम प्राप्त करें",
        "fetching_weather": "मौसम की जानकारी प्राप्त की जा रही है...",
        "temperature": "तापमान",
        "humidity": "नमी",
        "wind": "हवा की गति",
        "datetime": "दिनांक और समय",
        "precipitation": "वर्षण",
        "rainfall": "बारिश",
        "weather_error": "मौसम की जानकारी प्राप्त नहीं हो सकी।",
        "mandi_title": "कृषि मंडी भाव",
        "state": "राज्य का नाम दर्ज करें",
        "district": "जिले का नाम दर्ज करें",
        "commodity": "फसल का नाम दर्ज करें",
        "search_mandi": "मंडी भाव खोजें",
        "no_markets": "मिलते-जुलते मंडी रिकॉर्ड नहीं मिले।",
        "found_markets": "मिले हुए मंडी रिकॉर्ड:",
        "records": "रिकॉर्ड",
        "arrival_date": "आवक की तारीख",
        "minimum_price": "न्यूनतम मूल्य",
        "maximum_price": "अधिकतम मूल्य",
        "modal_price": "प्रचलित मूल्य",
        "variety": "किस्म",
        "price_note": "कीमतें डाउनलोड किए गए डेटासेट से हैं। उपयोग से पहले तारीख और मूल्य की इकाई जाँचें।",
        "fill_fields": "कृपया तीनों जानकारी दर्ज करें।",
        "schemes_title": "सरकारी योजनाएँ",
        "scheme_query": "योजना का नाम या कीवर्ड दर्ज करें",
        "scheme_placeholder": "उदाहरण: PM KISAN",
        "search_schemes": "योजनाएँ खोजें",
        "eligibility": "पात्रता",
        "benefits": "लाभ",
        "official_source": "आधिकारिक स्रोत",
        "no_scheme": "कोई मिलती-जुलती योजना नहीं मिली।",
        "enter_scheme": "कृपया योजना का नाम दर्ज करें।",
        "crop_title": "कृषि फसल सलाह",
        "crop_query": "फसल से संबंधित प्रश्न पूछें",
        "crop_placeholder": "उदाहरण: soybean sowing",
        "search_crop": "फसल सलाह खोजें",
        "searching_crop": "कृषि दस्तावेज़ खोजे जा रहे हैं...",
        "result": "परिणाम",
        "topic": "विषय",
        "source": "स्रोत",
        "page": "पृष्ठ",
        "year": "प्रकाशन वर्ष",
        "general": "सामान्य",
        "crop_warning": "प्राप्त जानकारी की स्थानीय कृषि विशेषज्ञों के वर्तमान मार्गदर्शन से जाँच करें। आधिकारिक पुष्टि के बिना कीटनाशक की मात्रा का उपयोग न करें।",
        "no_crop": "पर्याप्त प्रासंगिक फसल जानकारी नहीं मिली।",
        "enter_crop": "कृपया फसल से संबंधित प्रश्न दर्ज करें।",
        "footer": "कृषि सहायक प्रोटोटाइप | भारतीय किसानों की सहायता के लिए बनाया गया"
    }
}


# --------------------------------------------------
# LANGUAGE SELECTION
# --------------------------------------------------

language = st.sidebar.selectbox(
    "Select Language / भाषा निवडा / भाषा चुनें",
    ["English", "मराठी", "हिन्दी"]
)

t = translations[language]


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("🌾 " + t["title"])
st.write(t["tagline"])
st.info(t["prototype"])


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

menu_options = {
    t["home"]: "home",
    t["weather"]: "weather",
    t["mandi"]: "mandi",
    t["schemes"]: "schemes",
    t["crop"]: "crop"
}

selected_menu = st.sidebar.selectbox(
    t["choose"],
    list(menu_options.keys())
)

menu = menu_options[selected_menu]


# --------------------------------------------------
# HOME
# --------------------------------------------------

if menu == "home":

    st.header(t["welcome"])
    st.write(t["select_service"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌦️ " + t["weather"])
        st.write(t["weather_desc"])

        st.subheader("🏛️ " + t["schemes"])
        st.write(t["schemes_desc"])

    with col2:
        st.subheader("📊 " + t["mandi"])
        st.write(t["mandi_desc"])

        st.subheader("🌱 " + t["crop"])
        st.write(t["crop_desc"])


# --------------------------------------------------
# WEATHER
# --------------------------------------------------

elif menu == "weather":

    st.header("🌦️ " + t["weather"])
    st.write(t["current_weather"])

    # Initialize session state
    if "weather_result" not in st.session_state:
        st.session_state["weather_result"] = None

    if "weather_language" not in st.session_state:
        st.session_state["weather_language"] = "English"

    if "weather_audio" not in st.session_state:
        st.session_state["weather_audio"] = None

    # Voice language selection
    voice_language = st.selectbox(
        "Select voice input language",
        ["English", "मराठी", "हिन्दी"],
        key="weather_voice_language"
    )

    speech_languages = {
        "English": "en-IN",
        "मराठी": "mr-IN",
        "हिन्दी": "hi-IN"
    }

    # Voice input
    st.subheader("🎤 Ask using your voice")

    st.caption(
        "Example: What is the current weather in Pune?"
    )

    audio_input = st.audio_input("Record your question")

    if st.button("Convert Voice to Text"):

        if audio_input is not None:

            speech_result = convert_audio_to_text(
                audio_input.getvalue(),
                language=speech_languages[voice_language]
            )

            if speech_result["success"]:

                recognized_text = speech_result["text"]

                st.session_state["weather_query"] = recognized_text
                st.session_state["weather_language"] = voice_language

                st.success("Recognized: " + recognized_text)

            else:
                st.warning(speech_result["error"])

        else:
            st.warning("Please record your question first.")

    # Text input
    weather_query = st.text_input(
        "Weather question",
        placeholder="Example: Current weather in Pune",
        key="weather_query"
    )

    # Fetch weather
    if st.button(t["get_weather"]):

        if weather_query.strip():

            with st.spinner(t["fetching_weather"]):

                detected_language = st.session_state["weather_language"]

                translation_result = translate_agri_query(
                    weather_query,
                    detected_language
                )

                if translation_result["success"]:

                    english_query = translation_result["translation"]

                    # Extract requested city or district
                    weather_location = extract_weather_location(
                        english_query
                    )

                    # Fetch weather for requested location
                    result = get_weather(weather_location)

                    st.session_state["weather_result"] = result
                    st.session_state["weather_language"] = detected_language
                    st.session_state["weather_audio"] = None

                else:

                    st.session_state["weather_result"] = {
                        "error": translation_result["error"]
                    }

        else:
            st.warning("Please enter or record a weather question.")

    # Display saved weather
    result = st.session_state["weather_result"]
    response_language = st.session_state["weather_language"]

    if result:

        if "error" in result:

            st.error(result["error"])

        else:

            # Display requested location
            location_text = result["location"]

            if result.get("state"):
                location_text += ", " + result["state"]

            if result.get("country"):
                location_text += ", " + result["country"]

            st.subheader("📍 " + location_text)

            # Weather metrics
            col1, col2, col3 = st.columns(3)

            col1.metric(
                t["temperature"],
                f'{result["temperature"]} °C'
            )

            col2.metric(
                t["humidity"],
                f'{result["humidity"]} %'
            )

            col3.metric(
                t["wind"],
                f'{result["wind_speed"]} km/h'
            )

            st.write(t["datetime"] + ":", result["date_time"])
            st.write(t["precipitation"] + ":", result["precipitation"], "mm")
            st.write(t["rainfall"] + ":", result["rain"], "mm")

            # --------------------------------------------------
            # WEATHER SOURCE INFORMATION
            # --------------------------------------------------

            st.divider()
            st.subheader("📚 Weather Data Source")

            st.write(
                "**Data Type:**",
                result.get("data_type", "Current weather")
            )

            st.write(
                "**Data As Of:**",
                result.get("data_as_of", result["date_time"])
            )

            st.write(
                "**Timezone:**",
                result.get("timezone", "Asia/Kolkata")
            )

            st.markdown(
                f'**Source:** [{result.get("source", "Open-Meteo Weather API")}]'
                f'({result.get("source_url", "https://open-meteo.com/")})'
            )

            st.caption(
                "Weather information is provided by Open-Meteo. "
                "The timestamp indicates the time of the returned weather data."
            )

            # --------------------------------------------------
            # PREPARE SPOKEN WEATHER REPORT
            # --------------------------------------------------

            weather_text = (
                f'Current weather report for {result["location"]}.\n'
                f'Temperature: {result["temperature"]} degrees Celsius.\n'
                f'Humidity: {result["humidity"]} percent.\n'
                f'Wind speed: {result["wind_speed"]} kilometers per hour.\n'
                f'Precipitation: {result["precipitation"]} millimeters.\n'
                f'Rainfall: {result["rain"]} millimeters.'
            )

            # Translate weather report
            if response_language != "English":

                translation_result = translate_from_english(
                    weather_text,
                    response_language
                )

                if translation_result["success"]:
                    display_weather_text = translation_result["translation"]

                else:
                    display_weather_text = weather_text

                    st.warning(
                        "Translation unavailable. Showing English information."
                    )

            else:
                display_weather_text = weather_text

            # Audio response
            if st.button("🔊 Listen to Weather Report"):

                audio = convert_text_to_audio(
                    display_weather_text,
                    response_language
                )

                if audio:

                    st.session_state["weather_audio"] = audio.getvalue()

                else:
                    st.warning("Audio generation failed. Please try again.")

            # Play saved audio
            if st.session_state["weather_audio"]:

                st.audio(
                    st.session_state["weather_audio"],
                    format="audio/mp3"
                )


# --------------------------------------------------
# MANDI PRICES
# --------------------------------------------------

elif menu == "mandi":

    st.header("📊 " + t["mandi_title"])

    # --------------------------------------------------
    # INITIALIZE SESSION STATE
    # --------------------------------------------------

    if "mandi_results" not in st.session_state:
        st.session_state["mandi_results"] = None

    if "mandi_language" not in st.session_state:
        st.session_state["mandi_language"] = "English"

    if "mandi_voice_query" not in st.session_state:
        st.session_state["mandi_voice_query"] = ""

    if "mandi_audio" not in st.session_state:
        st.session_state["mandi_audio"] = None

    # --------------------------------------------------
    # VOICE LANGUAGE SELECTION
    # --------------------------------------------------

    voice_language = st.selectbox(
        "Select voice input language",
        ["English", "मराठी", "हिन्दी"],
        key="mandi_voice_language"
    )

    speech_languages = {
        "English": "en-IN",
        "मराठी": "mr-IN",
        "हिन्दी": "hi-IN"
    }

    # --------------------------------------------------
    # VOICE INPUT
    # --------------------------------------------------

    st.subheader("🎤 Ask using your voice")

    st.caption(
        "Speak in this format: State, District, Commodity"
    )

    st.caption(
        "Example: Maharashtra, Pune, Tomato"
    )

    audio_input = st.audio_input("Record your question")

    if st.button("Convert Voice to Text"):

        if audio_input is not None:

            audio_bytes = audio_input.getvalue()

            speech_result = convert_audio_to_text(
                audio_bytes,
                language=speech_languages[voice_language]
            )

            if speech_result["success"]:

                recognized_text = speech_result["text"]

                # Translate voice query into English
                translation_result = translate_agri_query(
                    recognized_text,
                    voice_language
                )

                if translation_result["success"]:

                    english_query = translation_result["translation"]

                    parts = [
                        item.strip()
                        for item in english_query.split(",")
                        if item.strip()
                    ]

                    if len(parts) == 3:

                        st.session_state["mandi_state"] = parts[0]
                        st.session_state["mandi_district"] = parts[1]
                        st.session_state["mandi_commodity"] = parts[2]

                        st.session_state["mandi_voice_query"] = english_query
                        st.session_state["mandi_language"] = voice_language

                        st.success(
                            "Recognized: " + recognized_text
                        )

                    else:

                        st.warning(
                            "Please speak in this format: "
                            "State, District, Commodity. "
                            "Example: Maharashtra, Pune, Tomato."
                        )

                else:

                    st.error(translation_result["error"])

            else:

                st.warning(speech_result["error"])

        else:

            st.warning("Please record your question first.")

    st.divider()

    # --------------------------------------------------
    # MANUAL SEARCH FIELDS
    # --------------------------------------------------

    state = st.text_input(
        t["state"],
        value="Maharashtra",
        key="mandi_state"
    )

    district = st.text_input(
        t["district"],
        value="Pune",
        key="mandi_district"
    )

    commodity = st.text_input(
        t["commodity"],
        value="Tomato",
        key="mandi_commodity"
    )

    # --------------------------------------------------
    # SEARCH MANDI PRICES
    # --------------------------------------------------

    if st.button(t["search_mandi"]):

        if state.strip() and district.strip() and commodity.strip():

            with st.spinner("Fetching mandi prices..."):

                results = get_mandi_prices(
                    state.strip(),
                    district.strip(),
                    commodity.strip()
                )

                st.session_state["mandi_results"] = results

                # Clear previous audio when a new search is performed
                st.session_state["mandi_audio"] = None

                # Determine response language
                if (
                    state == st.session_state["mandi_state"]
                    and district == st.session_state["mandi_district"]
                    and commodity == st.session_state["mandi_commodity"]
                    and st.session_state["mandi_voice_query"]
                ):

                    response_language = st.session_state["mandi_language"]

                else:

                    response_language = detect_language(commodity)

                    if response_language == "Unknown":
                        response_language = "English"

                st.session_state["mandi_language"] = response_language

        else:

            st.warning(t["fill_fields"])

    # --------------------------------------------------
    # DISPLAY SAVED RESULTS
    # --------------------------------------------------

    results = st.session_state["mandi_results"]

    response_language = st.session_state["mandi_language"]

    if isinstance(results, dict) and results.get("error"):

        st.error(results["error"])

    elif isinstance(results, dict):

        records = results.get("records", [])

        if records:

            st.success(
                f'{t["found_markets"]} {len(records)} {t["records"]}'
            )

            # --------------------------------------------------
            # SOURCE INFORMATION
            # --------------------------------------------------

            st.divider()

            st.subheader("📚 Mandi Price Data Source")

            st.write(
                "**Data Type:**",
                results.get(
                    "data_type",
                    "Historical mandi price dataset"
                )
            )

            st.write(
                "**Latest Available Arrival Date:**",
                results.get("data_as_of") or "Not available"
            )

            source_name = results.get("source", "AGMARKNET")

            source_url = results.get(
                "source_url",
                "https://agmarknet.gov.in/"
            )

            st.markdown(
                f"**Source:** [{source_name}]({source_url})"
            )

            st.caption(
                "Prices are retrieved from the available AGMARKNET "
                "dataset. They may not represent today's live market prices."
            )

            st.divider()

            # --------------------------------------------------
            # DISPLAY MARKET-WISE PRICE DETAILS
            # --------------------------------------------------

            audio_response_text = ""

            for index, row in enumerate(records, start=1):

                market_text = (
                    "Market: " + str(row.get("Market", "N/A")) + "\n" +
                    "Commodity: " + str(row.get("Commodity", "N/A")) + "\n" +
                    "Variety: " + str(row.get("Variety", "N/A")) + "\n" +
                    "Grade: " + str(row.get("Grade", "N/A")) + "\n" +
                    "Arrival Date: " + str(row.get("Arrival_Date", "N/A")) + "\n" +
                    "Minimum Price: " + str(row.get("Min_x0020_Price", "N/A")) + "\n" +
                    "Maximum Price: " + str(row.get("Max_x0020_Price", "N/A")) + "\n" +
                    "Modal Price: " + str(row.get("Modal_x0020_Price", "N/A"))
                )

                # Translate market details
                if response_language != "English":

                    translation_result = translate_from_english(
                        market_text,
                        response_language
                    )

                    if translation_result["success"]:

                        display_text = translation_result["translation"]

                    else:

                        display_text = market_text

                        st.warning(
                            "Translation unavailable. "
                            "Showing market information in English."
                        )

                else:

                    display_text = market_text

                # Market-wise expandable results
                market_name = row.get("Market", f"Market {index}")

                with st.expander(str(market_name)):

                    st.text(display_text)

                audio_response_text += market_text + "\n\n"

            st.caption(t["price_note"])

            # --------------------------------------------------
            # AUDIO RESPONSE
            # --------------------------------------------------

            if st.button("🔊 Listen to Mandi Prices"):

                if response_language != "English":

                    translation_result = translate_from_english(
                        audio_response_text,
                        response_language
                    )

                    if translation_result["success"]:

                        audio_text = translation_result["translation"]

                    else:

                        audio_text = audio_response_text

                        st.warning(
                            "Translation unavailable. "
                            "Audio will be generated in English."
                        )

                else:

                    audio_text = audio_response_text

                audio = convert_text_to_audio(
                    audio_text,
                    response_language
                )

                if audio:

                    st.session_state["mandi_audio"] = audio.getvalue()

                else:

                    st.warning(
                        "Audio generation failed. Please try again."
                    )

            # --------------------------------------------------
            # PLAY SAVED AUDIO
            # --------------------------------------------------

            if st.session_state.get("mandi_audio"):

                st.audio(
                    st.session_state["mandi_audio"],
                    format="audio/mp3"
                )

        else:

            st.warning(t["no_markets"])

    elif results == []:

        st.warning(t["no_markets"])


# --------------------------------------------------
# GOVERNMENT SCHEMES
# --------------------------------------------------

elif menu == "schemes":

    st.header("🏛️ " + t["schemes_title"])

    # --------------------------------------------------
    # INITIALIZE SESSION STATE
    # --------------------------------------------------

    if "scheme_results" not in st.session_state:
        st.session_state["scheme_results"] = None

    if "scheme_language" not in st.session_state:
        st.session_state["scheme_language"] = "English"

    if "scheme_voice_query" not in st.session_state:
        st.session_state["scheme_voice_query"] = ""

    # --------------------------------------------------
    # VOICE INPUT LANGUAGE
    # --------------------------------------------------

    voice_language = st.selectbox(
        "Select voice input language",
        ["English", "मराठी", "हिन्दी"],
        key="scheme_voice_language"
    )

    speech_languages = {
        "English": "en-IN",
        "मराठी": "mr-IN",
        "हिन्दी": "hi-IN"
    }

    # --------------------------------------------------
    # VOICE INPUT
    # --------------------------------------------------

    st.subheader("🎤 Ask using your voice")

    st.caption(
        "Example: Tell me about PM-KISAN scheme"
    )

    audio_input = st.audio_input("Record your question")

    if st.button("Convert Voice to Text"):

        if audio_input is not None:

            audio_bytes = audio_input.getvalue()

            speech_result = convert_audio_to_text(
                audio_bytes,
                language=speech_languages[voice_language]
            )

            if speech_result["success"]:

                recognized_text = speech_result["text"]

                st.session_state["scheme_query"] = recognized_text
                st.session_state["scheme_voice_query"] = recognized_text
                st.session_state["scheme_language"] = voice_language

                st.success("Recognized: " + recognized_text)

            else:

                st.warning(speech_result["error"])

        else:

            st.warning("Please record your question first.")

    # --------------------------------------------------
    # TEXT INPUT
    # --------------------------------------------------

    query = st.text_input(
        t["scheme_query"],
        placeholder=t["scheme_placeholder"],
        key="scheme_query"
    )

    # --------------------------------------------------
    # SEARCH GOVERNMENT SCHEMES
    # --------------------------------------------------

    if st.button(t["search_schemes"]):

        if query.strip():

            # Identify language
            if query == st.session_state["scheme_voice_query"]:

                detected_language = st.session_state["scheme_language"]

            else:

                detected_language = detect_language(query)

                if detected_language == "Unknown":
                    detected_language = "English"

            # Translate query into English
            translation_result = translate_agri_query(
                query,
                detected_language
            )

            if translation_result["success"]:

                english_query = translation_result["translation"]

                results = search_scheme(english_query)

                st.session_state["scheme_results"] = results
                st.session_state["scheme_language"] = detected_language

            else:

                st.session_state["scheme_results"] = None

                st.error(translation_result["error"])

        else:

            st.warning(t["enter_scheme"])

    # --------------------------------------------------
    # DISPLAY SAVED RESULTS
    # --------------------------------------------------

    results = st.session_state["scheme_results"]

    response_language = st.session_state["scheme_language"]

    if results:

        st.success(
            f"{len(results)} government scheme(s) found."
        )

        for index, scheme in enumerate(results, start=1):

            st.subheader("🏛️ " + scheme["name"])

            # --------------------------------------------------
            # PREPARE SCHEME INFORMATION
            # --------------------------------------------------

            scheme_text = (
                scheme["name"] + "\n\n" +
                scheme["description"] + "\n\n" +
                "Eligibility: " + scheme["eligibility"] + "\n\n" +
                "Benefits: " + scheme["benefits"]
            )

            # Translate scheme information
            if response_language != "English":

                translation_result = translate_from_english(
                    scheme_text,
                    response_language
                )

                if translation_result["success"]:

                    display_text = translation_result["translation"]

                else:

                    display_text = scheme_text

                    st.warning(
                        "Translation unavailable. "
                        "Showing English information."
                    )

            else:

                display_text = scheme_text

            # Display translated information
            st.write(display_text)

            # --------------------------------------------------
            # OFFICIAL SOURCE INFORMATION
            # --------------------------------------------------

            with st.expander("📚 Official Source Information"):

                st.write(
                    "**Information Type:**",
                    scheme.get(
                        "information_type",
                        "Official scheme information"
                    )
                )

                st.write(
                    "**Source Name:**",
                    scheme.get("source_name", "Government source")
                )

                st.write(
                    "**Source Checked On:**",
                    scheme.get("source_checked_on", "Not specified")
                )

                source_name = scheme.get("source_name", scheme["name"])
                source_url = scheme.get("source", "")

                if source_url:
                    st.markdown(
                        f'**Official Source:** [{source_name}]({source_url})'
                    )

            st.caption(
                "Note: Eligibility and benefits are subject to "
                "applicable government rules. Please verify details "
                "through the official government portal before applying."
            )

            # --------------------------------------------------
            # AUDIO RESPONSE
            # --------------------------------------------------

            if st.button(
                "🔊 Listen",
                key="listen_scheme_" + str(scheme["name"])
            ):

                audio = convert_text_to_audio(
                    display_text,
                    response_language
                )

                if audio:

                    st.session_state[
                        "scheme_audio_" + str(scheme["name"])
                    ] = audio.getvalue()

                else:

                    st.warning(
                        "Audio generation failed. Please try again."
                    )

            # Play saved audio
            audio_data = st.session_state.get(
                "scheme_audio_" + str(scheme["name"])
            )

            if audio_data:

                st.audio(
                    audio_data,
                    format="audio/mp3"
                )

            st.divider()

    elif results == []:

        st.warning(t["no_scheme"])



# --------------------------------------------------
# CROP ADVISORY
# --------------------------------------------------

elif menu == "crop":

    st.header("🌱 " + t["crop_title"])

    # --------------------------------------------------
    # INITIALIZE SESSION STATE
    # --------------------------------------------------

    if "crop_results" not in st.session_state:
        st.session_state["crop_results"] = None

    if "crop_detected_language" not in st.session_state:
        st.session_state["crop_detected_language"] = language

    if "crop_error" not in st.session_state:
        st.session_state["crop_error"] = None

    if "crop_query" not in st.session_state:
        st.session_state["crop_query"] = ""

    if "tts_cache" not in st.session_state:
        st.session_state["tts_cache"] = {}

    # --------------------------------------------------
    # VOICE INPUT LANGUAGE
    # --------------------------------------------------

    speech_languages = {
        "English": "en-IN",
        "मराठी": "mr-IN",
        "हिन्दी": "hi-IN"
    }

    st.caption(
        "Ask questions about crop cultivation, sowing, "
        "pests, diseases and fertilizer management."
    )

    # --------------------------------------------------
    # VOICE INPUT
    # --------------------------------------------------

    st.subheader("🎤 Ask using your voice")

    audio_value = st.audio_input(
        "Record your agricultural question"
    )

    if st.button("Convert Speech to Text"):

        if audio_value is not None:

            with st.spinner("Recognizing speech..."):

                speech_result = convert_audio_to_text(
                    audio_value.getvalue(),
                    speech_languages[language]
                )

            if speech_result["success"]:

                recognized_text = speech_result["text"]

                st.session_state["crop_query"] = recognized_text

                st.session_state["crop_detected_language"] = language

                st.success(
                    "Recognized: " + recognized_text
                )

            else:

                st.error(speech_result["error"])

        else:

            st.warning("Please record your question first.")

    st.divider()

    # --------------------------------------------------
    # TEXT INPUT
    # --------------------------------------------------

    query = st.text_input(
        t["crop_query"],
        placeholder=t["crop_placeholder"],
        key="crop_query"
    )

    # --------------------------------------------------
    # SEARCH CROP ADVISORY
    # --------------------------------------------------

    if st.button(t["search_crop"]):

        if query.strip():

            detected_language = detect_language(query)

            if detected_language == "Unknown":

                detected_language = language

            st.session_state["crop_detected_language"] = detected_language

            st.session_state["crop_results"] = None

            st.session_state["crop_error"] = None

            # Clear previous audio cache for a new search
            st.session_state["tts_cache"] = {}

            with st.spinner("Searching agricultural documents..."):

                query_result = translate_agri_query(
                    query,
                    detected_language
                )

                if query_result["success"]:

                    search_query = query_result["translation"]

                    results = search_crop_advisory(search_query)

                    # --------------------------------------
                    # VALIDATE RETRIEVED EVIDENCE
                    # --------------------------------------

                    valid_results = []

                    if isinstance(results, list):

                        for result in results:

                            advisory_text = result.get(
                                "text", ""
                            ).strip()

                            filename = result.get("filename")

                            page = result.get("page")

                            # Check for usable text and source details

                            if (
                                advisory_text
                                and len(advisory_text) >= 80
                                and filename
                                and page is not None
                            ):

                                valid_results.append(result)

                    st.session_state["crop_results"] = valid_results

                else:

                    st.session_state["crop_error"] = (
                        query_result.get(
                            "error",
                            "Unable to translate your question. Please try again."
                        )
                    )

        else:

            st.warning(t["enter_crop"])

    # --------------------------------------------------
    # DISPLAY SAVED RESULTS
    # --------------------------------------------------

    detected_language = st.session_state["crop_detected_language"]

    if st.session_state["crop_error"]:

        st.error(st.session_state["crop_error"])

    results = st.session_state["crop_results"]

    # --------------------------------------------------
    # SAFE FALLBACK FUNCTION
    # --------------------------------------------------

    def show_crop_fallback(message):

        fallback_text = message + (
            " Please contact your nearest Krishi Vigyan Kendra "
            "or Kisan Call Centre for expert guidance."
        )

        display_message = fallback_text

        speech_language = detected_language

        # ------------------------------------------
        # TRANSLATE FALLBACK MESSAGE
        # ------------------------------------------

        if detected_language != "English":

            translated_fallback = translate_from_english(
                fallback_text,
                detected_language
            )

            if translated_fallback["success"]:

                display_message = translated_fallback["translation"]

            else:

                speech_language = "English"

        # ------------------------------------------
        # DISPLAY FALLBACK MESSAGE
        # ------------------------------------------

        st.warning(display_message)

        st.info(
            "For reliable agricultural guidance, contact your "
            "nearest Krishi Vigyan Kendra (KVK) or Kisan Call Centre."
        )

        st.markdown(
            "**Kisan Call Centre:** 1800-180-1551"
        )

        # ------------------------------------------
        # TEXT-TO-SPEECH FOR FALLBACK
        # ------------------------------------------

        if st.button(
            "🔊 Listen to Safety Message",
            key="crop_fallback_audio"
        ):

            with st.spinner("Generating audio..."):

                audio_buffer = convert_text_to_audio(
                    display_message,
                    speech_language
                )

                if audio_buffer:

                    st.audio(
                        audio_buffer,
                        format="audio/mp3"
                    )

                else:

                    st.warning(
                        "Audio generation failed. Please try again."
                    )

    # --------------------------------------------------
    # HANDLE INSUFFICIENT EVIDENCE
    # --------------------------------------------------

    if results == []:

        st.subheader("Safe Response")

        fallback_message = (
            "Sorry, I could not find sufficient reliable "
            "information in the available agricultural documents "
            "to answer your question. I do not want to provide "
            "incorrect agricultural advice."
        )

        show_crop_fallback(fallback_message)

    # --------------------------------------------------
    # DISPLAY RETRIEVED ADVISORY RESULTS
    # --------------------------------------------------

    elif results:

        st.success(
            f"{min(len(results), 2)} relevant results found."
        )

        for index, result in enumerate(results[:2], start=1):

            st.subheader(
                f'{t["result"]} {index}'
            )

            # ------------------------------------------
            # SOURCE AND RELEVANCE INFORMATION
            # ------------------------------------------

            st.write(
                "**Crop:**",
                result.get("crop", "Not specified")
            )

            st.write(
                "**Topic:**",
                result.get("topic") or t["general"]
            )

            st.write(
                "**Source Document:**",
                result["filename"]
            )

            st.write(
                "**Publication Year:**",
                result.get("year", "Not specified")
            )

            st.write(
                "**PDF Page Number:**",
                result["page"]
            )

            st.write(
                "**Relevance Score:**",
                result.get("score", "Not available")
            )

            if result.get("matched_topics"):

                st.write(
                    "**Matched Topic Terms:**",
                    ", ".join(result["matched_topics"])
                )

            # ------------------------------------------
            # EXTRACTED ADVISORY TEXT
            # ------------------------------------------

            original_text = result["text"][:700]

            advisory_for_speech = original_text

            speech_output_language = "English"

            # ------------------------------------------
            # TRANSLATE ADVISORY
            # ------------------------------------------

            if detected_language != "English":

                answer_result = translate_from_english(
                    original_text,
                    detected_language
                )

                if answer_result["success"]:

                    advisory_for_speech = answer_result["translation"]

                    speech_output_language = detected_language

                    st.markdown("### Translated Advisory")

                    st.write(advisory_for_speech)

                    with st.expander(
                        "View Original English Advisory"
                    ):

                        st.write(original_text)

                else:

                    speech_output_language = "English"

                    st.warning(
                        "Translation unavailable. "
                        "Showing English advisory."
                    )

                    st.write(original_text)

            else:

                st.markdown("### Advisory")

                st.write(original_text)

            # ------------------------------------------
            # TEXT-TO-SPEECH
            # ------------------------------------------

            cache_key = (
                advisory_for_speech,
                speech_output_language
            )

            if st.button(
                "🔊 Listen to Advisory",
                key=f"listen_advisory_{index}"
            ):

                if cache_key not in st.session_state["tts_cache"]:

                    with st.spinner("Generating audio..."):

                        audio_buffer = convert_text_to_audio(
                            advisory_for_speech,
                            speech_output_language
                        )

                    if audio_buffer:

                        st.session_state["tts_cache"][cache_key] = (
                            audio_buffer.getvalue()
                        )

                    else:

                        st.warning(
                            "Audio generation failed. Please try again."
                        )

            # ------------------------------------------
            # PLAY SAVED AUDIO
            # ------------------------------------------

            audio_bytes = st.session_state["tts_cache"].get(
                cache_key
            )

            if audio_bytes:

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

            st.divider()

        # ------------------------------------------
        # AGRICULTURAL SAFETY NOTICE
        # ------------------------------------------

        st.warning(t["crop_warning"])

    # --------------------------------------------------
    # NO SEARCH RESULTS STORED YET
    # --------------------------------------------------

    elif results is None and not st.session_state["crop_error"]:

        pass

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(t["footer"])
