
import re
import csv
from pathlib import Path
from difflib import SequenceMatcher
from functools import lru_cache
from pypdf import PdfReader


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

PDF_FOLDERS = [
    PROJECT_FOLDER / "dataset" / "crop_guides",
    PROJECT_FOLDER / "dataset" / "pest_advisories"
]

METADATA_FILE = (
    PROJECT_FOLDER / "dataset" / "knowledge_base_metadata.csv"
)


# --------------------------------------------------
# LOAD KNOWLEDGE BASE METADATA
# --------------------------------------------------

@lru_cache(maxsize=1)
def load_knowledge_metadata():

    metadata = {}

    if not METADATA_FILE.exists():

        print(
            "Knowledge base metadata file not found:",
            METADATA_FILE
        )

        return metadata

    try:

        with open(
            METADATA_FILE,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            required_columns = [
                "Document Name",
                "Approval Status"
            ]

            if not reader.fieldnames or not all(
                column in reader.fieldnames
                for column in required_columns
            ):

                print(
                    "Invalid metadata CSV format. "
                    "Check the column headings."
                )

                return metadata

            for row in reader:

                document_name = row.get(
                    "Document Name", ""
                ).strip()

                approval_status = row.get(
                    "Approval Status", ""
                ).strip().lower()

                if document_name:

                    metadata[document_name] = {

                        "document_id": row.get(
                            "Document ID", ""
                        ).strip(),

                        "source_publisher": row.get(
                            "Source / Publisher", ""
                        ).strip(),

                        "crop": row.get(
                            "Crop", ""
                        ).strip(),

                        "region": row.get(
                            "Region", ""
                        ).strip(),

                        "publication_year": row.get(
                            "Publication Year", ""
                        ).strip(),

                        "version": row.get(
                            "Version", ""
                        ).strip(),

                        "approval_status": approval_status,

                        "date_added": row.get(
                            "Date Added", ""
                        ).strip()

                    }

    except Exception as error:

        print(
            "Error loading knowledge metadata:",
            error
        )

    return metadata


# --------------------------------------------------
# CROP NAMES AND SYNONYMS
# --------------------------------------------------

CROP_ALIASES = {

    "soybean": ["soybean", "soya"],

    "cotton": ["cotton"],

    "wheat": ["wheat"],

    "rice": ["rice", "paddy"],

    "maize": ["maize", "corn"],

    "sugarcane": ["sugarcane", "sugar cane"],

    "groundnut": ["groundnut", "peanut"],

    "pigeon pea": ["pigeon pea", "tur", "arhar"],

    "chickpea": ["chickpea", "gram", "chana"],

    "jowar": ["jowar", "sorghum"],

    "bajra": ["bajra", "pearl millet"],

    "millet": ["millet"]

}


# --------------------------------------------------
# TOPIC KEYWORDS
# --------------------------------------------------

TOPICS = {

    "sowing": [
        "sowing", "sow", "seed", "seeding",
        "planting", "seed rate", "germination",
        "sowing time", "seed treatment"
    ],

    "cultivation": [
        "cultivation", "crop management",
        "soil preparation", "irrigation",
        "nutrient management", "farming practices"
    ],

    "pest": [
        "pest", "insect", "infestation",
        "pest management", "pest control",
        "insect management", "insect control"
    ],

    "disease": [
        "disease", "fungus", "fungal",
        "symptoms", "disease management",
        "plant disease"
    ],

    "fertilizer": [
        "fertilizer", "fertiliser", "nutrient",
        "nitrogen", "phosphorus", "potassium",
        "manure", "npk"
    ]

}


# --------------------------------------------------
# EXTRACT TEXT FROM APPROVED AGRICULTURAL PDF DOCUMENTS
# --------------------------------------------------

@lru_cache(maxsize=1)
def extract_pdf_pages():

    documents = []

    metadata = load_knowledge_metadata()

    approved_count = 0

    skipped_count = 0

    for folder in PDF_FOLDERS:

        if not folder.exists():

            print(
                "PDF folder not found:",
                folder
            )

            continue

        for pdf_file in folder.glob("*.pdf"):

            # ------------------------------------------
            # CHECK DOCUMENT METADATA
            # ------------------------------------------

            document_metadata = metadata.get(
                pdf_file.name
            )

            if not document_metadata:

                print(
                    f"Skipping {pdf_file.name}: "
                    "Metadata not found."
                )

                skipped_count += 1

                continue

            # ------------------------------------------
            # CHECK APPROVAL STATUS
            # ------------------------------------------

            if document_metadata["approval_status"] != "approved":

                print(
                    f"Skipping {pdf_file.name}: "
                    f"Status is "
                    f"{document_metadata['approval_status'] or 'missing'}."
                )

                skipped_count += 1

                continue

            # ------------------------------------------
            # EXTRACT APPROVED PDF
            # ------------------------------------------

            try:

                reader = PdfReader(
                    str(pdf_file)
                )

                year_match = re.search(
                    r"20\d{2}",
                    pdf_file.name
                )

                year = (
                    year_match.group()
                    if year_match
                    else document_metadata["publication_year"] or "Unknown"
                )

                for page_number, page in enumerate(
                    reader.pages,
                    start=1
                ):

                    text = page.extract_text() or ""

                    if text.strip():

                        documents.append({

                            "filename": pdf_file.name,

                            "page": page_number,

                            "year": year,

                            "text": text,

                            "document_id": document_metadata["document_id"],

                            "source_publisher": document_metadata["source_publisher"],

                            "crop_metadata": document_metadata["crop"],

                            "region": document_metadata["region"],

                            "version": document_metadata["version"],

                            "approval_status": document_metadata["approval_status"]

                        })

                approved_count += 1

                print(
                    f"Approved document loaded: {pdf_file.name}"
                )

            except Exception as error:

                print(
                    f"Could not read {pdf_file.name}: {error}"
                )

    print("\n========== KNOWLEDGE BASE STATUS ==========")

    print(
        "Approved PDF documents loaded:",
        approved_count
    )

    print(
        "Documents skipped:",
        skipped_count
    )

    print(
        "Total searchable PDF pages:",
        len(documents)
    )

    return documents


# --------------------------------------------------
# IDENTIFY CROP
# --------------------------------------------------

def identify_crop(query):

    query = query.lower()

    for canonical_crop, aliases in CROP_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"\b" +
                re.escape(alias) +
                r"\b"
            )

            if re.search(pattern, query):

                return canonical_crop

    return None


# --------------------------------------------------
# IDENTIFY AGRICULTURAL TOPIC
# --------------------------------------------------

def identify_topic(query):

    query = query.lower()

    for topic, keywords in TOPICS.items():

        for keyword in keywords:

            if keyword in query:

                return topic, keywords

    return None, []


# --------------------------------------------------
# GET CROP-RELATED TEXT CONTEXT
# --------------------------------------------------

def get_crop_context(text, crop):

    text_lower = text.lower()

    aliases = CROP_ALIASES.get(
        crop,
        [crop]
    )

    matches = []

    for alias in aliases:

        pattern = (
            r"\b" +
            re.escape(alias) +
            r"\b"
        )

        matches.extend(
            re.finditer(pattern, text_lower)
        )

    # Sort matches by their position in the document

    matches.sort(
        key=lambda match: match.start()
    )

    contexts = []

    for match in matches:

        start = max(
            0,
            match.start() - 500
        )

        end = min(
            len(text),
            match.end() + 1000
        )

        context = text[start:end]

        contexts.append(context)

    return contexts


# --------------------------------------------------
# SEARCH CROP ADVISORY DOCUMENTS
# --------------------------------------------------

def search_crop_advisory(query):

    if not query.strip():

        return []

    # ------------------------------------------
    # IDENTIFY CROP AND TOPIC
    # ------------------------------------------

    crop = identify_crop(query)

    topic, topic_keywords = identify_topic(query)

    if not crop:

        print(
            "\nPlease include a recognized crop name "
            "such as soybean, cotton or wheat."
        )

        return []

    if not topic:

        print(
            "\nNo specific topic detected. "
            "Searching for general crop-related information."
        )

    # ------------------------------------------
    # LOAD APPROVED PDF DOCUMENTS
    # ------------------------------------------

    documents = extract_pdf_pages()

    results = []

    for document in documents:

        contexts = get_crop_context(
            document["text"],
            crop
        )

        for context in contexts:

            context_lower = context.lower()

            # ------------------------------------------
            # IDENTIFY MATCHING TOPIC KEYWORDS
            # ------------------------------------------

            matched_topics = [

                word

                for word in topic_keywords

                if word in context_lower

            ]

            # Require topic relevance when a topic is requested

            if topic and not matched_topics:

                continue

            # ------------------------------------------
            # CALCULATE RELEVANCE SCORE
            # ------------------------------------------

            score = 10

            if topic:

                score += len(matched_topics) * 3

            if "maharashtra" in context_lower:

                score += 5

            if "introduction" in context_lower[:150]:

                score -= 3

            # ------------------------------------------
            # ADD SEARCH RESULT
            # ------------------------------------------

            results.append({

                "document_id": document["document_id"],

                "filename": document["filename"],

                "page": document["page"],

                "year": document["year"],

                "source_publisher": document["source_publisher"],

                "region": document["region"],

                "version": document["version"],

                "approval_status": document["approval_status"],

                "score": score,

                "crop": crop,

                "topic": topic,

                "matched_topics": matched_topics,

                "text": context

            })

    # --------------------------------------------------
    # SORT RESULTS BY RELEVANCE
    # --------------------------------------------------

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # --------------------------------------------------
    # REMOVE DUPLICATE EXCERPTS
    # --------------------------------------------------

    unique_results = []

    for result in results:

        duplicate = False

        for existing in unique_results:

            similarity = SequenceMatcher(
                None,
                result["text"][:1200].lower(),
                existing["text"][:1200].lower()
            ).ratio()

            if similarity > 0.85:

                duplicate = True

                break

        if not duplicate:

            unique_results.append(result)

    return unique_results[:5]


# --------------------------------------------------
# DISPLAY CROP ADVISORY RESULTS
# --------------------------------------------------

def display_advisory_results(results):

    print(
        "\n========== CROP ADVISORY SEARCH =========="
    )

    if not results:

        print(
            "No sufficiently relevant crop-specific "
            "information was found in the approved PDFs."
        )

        print(
            "Try another query or add and approve "
            "a relevant agricultural document."
        )

        return

    for index, result in enumerate(
        results,
        start=1
    ):

        text = re.sub(
            r"\s+",
            " ",
            result["text"]
        ).strip()

        print(f"\nResult {index}")

        print(
            "Document ID:",
            result["document_id"]
        )

        print(
            "Crop:",
            result["crop"]
        )

        print(
            "Topic:",
            result["topic"] or "General"
        )

        print(
            "Source Document:",
            result["filename"]
        )

        print(
            "Source / Publisher:",
            result["source_publisher"]
        )

        print(
            "Publication Year:",
            result["year"]
        )

        print(
            "Region:",
            result["region"]
        )

        print(
            "Document Version:",
            result["version"]
        )

        print(
            "Approval Status:",
            result["approval_status"]
        )

        print(
            "Page Number:",
            result["page"]
        )

        print(
            "Relevance Score:",
            result["score"]
        )

        if result["matched_topics"]:

            print(
                "Matched Topic Terms:",
                ", ".join(result["matched_topics"])
            )

        print(
            "\nRelevant Extracted Information:"
        )

        print(text[:1000])

        print("\n" + "-" * 55)

    print(
        "\nTotal relevant excerpts:",
        len(results)
    )

    # --------------------------------------------------
    # PESTICIDE SAFETY CHECK
    # --------------------------------------------------

    all_text = " ".join(
        result["text"].lower()
        for result in results
    )

    safety_terms = [
        "pesticide",
        "insecticide",
        "fungicide",
        "herbicide",
        "dosage",
        "dose"
    ]

    if any(
        term in all_text
        for term in safety_terms
    ):

        print("\nIMPORTANT SAFETY NOTICE:")

        print(
            "Verify pesticide recommendations, dosage, "
            "crop approval and application instructions "
            "against current official local guidance "
            "and product labels."
        )


# --------------------------------------------------
# MAIN TEST
# --------------------------------------------------

if __name__ == "__main__":

    print(
        "===== AGRICULTURAL CROP ADVISORY ASSISTANT ====="
    )

    query = input(
        "Enter crop or agricultural question: "
    ).strip()

    results = search_crop_advisory(query)

    display_advisory_results(results)
