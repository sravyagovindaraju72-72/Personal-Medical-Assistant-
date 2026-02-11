SORE_THROAT_KEYWORDS = [
    "sore throat",
    "throat pain",
    "scratchy throat",
    "pain when swallowing",
    "hoarse voice"
]

def matches_sore_throat(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in SORE_THROAT_KEYWORDS)


def sore_throat_guidance():
    return {
        "self_care": [
            "Drink plenty of fluids (water or warm tea).",
            "Rest your voice and avoid yelling or long talking.",
            "Use throat lozenges if safe for you.",
            "Gargle with warm salt water.",
            "Use a humidifier or breathe moist air."
        ],
        "red_flags": [
            "Trouble breathing",
            "Not able to swallow",
            "Trouble opening the mouth",
            "Fever higher than 101°F (38.3°C)",
            "Bloody mucus",
            "Swelling in the neck or face"
        ],
        "when_to_seek_care": [
            "Sore throat lasts longer than one week",
            "Symptoms keep coming back",
            "Hoarseness lasts more than two weeks",
            "You notice a lump in the neck"
        ],
        "sources": [
            {
                "name": "Mayo Clinic — Sore Throat",
                "url": "https://www.mayoclinic.org/symptoms/sore-throat/basics/definition/sym-20050919"
            }
        ]
    }