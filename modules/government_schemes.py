
# --------------------------------------------------
# GOVERNMENT SCHEMES KNOWLEDGE BASE
# --------------------------------------------------

SCHEMES = [

    {
        "name": "PM-KISAN",

        "keywords": [
            "pm kisan",
            "pm-kisan",
            "kisan samman nidhi",
            "farmer income support"
        ],

        "description": (
            "PM-KISAN is a Central Government scheme providing "
            "eligible landholding farmer families financial "
            "assistance of Rs. 6,000 per year in three equal "
            "installments through Direct Benefit Transfer (DBT)."
        ),

        "eligibility": (
            "Eligible landholding farmer families, subject to "
            "scheme exclusion criteria, land record verification "
            "and other applicable requirements."
        ),

        "benefits": (
            "Rs. 6,000 per year in three installments "
            "of Rs. 2,000 each."
        ),

        "source_name": "PM-KISAN Official Government Portal",

        "source": "https://pmkisan.gov.in/",

        "source_checked_on": "2026-11-25",

        "information_type": "Official scheme information"
    },

    {
        "name": "Namo Shetkari Mahasanman Nidhi Yojana",

        "keywords": [
            "namo shetkari",
            "namo shetkari yojana",
            "maharashtra farmer scheme",
            "namo shetkari nidhi"
        ],

        "description": (
            "A Maharashtra Government scheme providing additional "
            "financial assistance to eligible PM-KISAN beneficiaries."
        ),

        "eligibility": (
            "Eligibility is linked to PM-KISAN beneficiary status "
            "and applicable Maharashtra Government rules."
        ),

        "benefits": (
            "Additional financial assistance of Rs. 6,000 per year "
            "under the scheme as described in the government resolution, "
            "subject to applicable rules."
        ),

        "source_name": "Maharashtra Government Resolution",

        "source": (
            "https://gr.maharashtra.gov.in/Site/Upload/"
            "Government%20Resolutions/English/202402211658102601.pdf"
        ),

        "source_checked_on": "2026-11-25",

        "information_type": "Official government resolution"
    },

    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",

        "keywords": [
            "pmfby",
            "fasal bima",
            "crop insurance",
            "crop loss insurance",
            "pradhan mantri fasal bima"
        ],

        "description": (
            "A Government of India crop insurance scheme designed "
            "to provide financial protection against specified "
            "crop losses caused by notified risks such as natural "
            "calamities, pests and diseases."
        ),

        "eligibility": (
            "Farmers growing notified crops in notified areas during "
            "the relevant season, subject to insurable interest, "
            "documentation and applicable scheme conditions."
        ),

        "benefits": (
            "Insurance protection against covered crop losses "
            "under the applicable scheme guidelines."
        ),

        "source_name": "Pradhan Mantri Fasal Bima Yojana Portal",

        "source": "https://pmfby.gov.in/",

        "source_checked_on": "2026-11-25",

        "information_type": "Official scheme information"
    },

    {
        "name": "Soil Health Card Scheme",

        "keywords": [
            "soil health card",
            "soil testing",
            "soil nutrients",
            "fertilizer recommendation",
            "soil fertility"
        ],

        "description": (
            "A Government of India scheme that helps farmers "
            "understand the nutrient status of their soil through "
            "soil testing and provides recommendations for "
            "appropriate fertilizer use."
        ),

        "eligibility": (
            "The scheme is applicable to farmers across India. "
            "Soil testing services are provided through the "
            "applicable government implementation process."
        ),

        "benefits": (
            "Soil nutrient information, soil health assessment "
            "and fertilizer recommendations based on soil test results."
        ),

        "source_name": "Soil Health Card Official Portal",

        "source": "https://soilhealth.dac.gov.in/",

        "source_checked_on": "2026-11-25",

        "information_type": "Official scheme information"
    }

]


# --------------------------------------------------
# SEARCH GOVERNMENT SCHEMES
# --------------------------------------------------

def search_scheme(query):

    query = query.lower().strip()

    if not query:
        return []

    results = []

    for scheme in SCHEMES:

        searchable_text = (
            scheme["name"] + " " +
            " ".join(scheme["keywords"]) + " " +
            scheme["description"] + " " +
            scheme["eligibility"] + " " +
            scheme["benefits"]
        ).lower()

        # Match complete query or individual meaningful words
        query_words = query.split()

        if (
            query in searchable_text
            or all(word in searchable_text for word in query_words)
        ):

            results.append(scheme)

    return results


# --------------------------------------------------
# DISPLAY GOVERNMENT SCHEME INFORMATION
# --------------------------------------------------

def display_schemes(results):

    print("\n========== GOVERNMENT SCHEME INFORMATION ==========")

    if not results:

        print("No matching scheme found.")
        print("Please try another scheme name or keyword.")

        return

    for index, scheme in enumerate(results, start=1):

        print(f"\nScheme {index}: {scheme['name']}")

        print("\nDescription:")
        print(scheme["description"])

        print("\nEligibility:")
        print(scheme["eligibility"])

        print("\nBenefits:")
        print(scheme["benefits"])

        print("\n========== SOURCE INFORMATION ==========")

        print("Information Type:", scheme["information_type"])

        print("Source Name:", scheme["source_name"])

        print("Official Source:", scheme["source"])

        print("Source Checked On:", scheme["source_checked_on"])

        print(
            "\nNote: Eligibility and benefits should be confirmed "
            "through the official government portal before applying."
        )


# --------------------------------------------------
# MAIN TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("===== AGRICULTURAL GOVERNMENT SCHEME SEARCH =====")

    query = input(
        "Enter scheme name or keyword: "
    ).strip()

    results = search_scheme(query)

    display_schemes(results)
