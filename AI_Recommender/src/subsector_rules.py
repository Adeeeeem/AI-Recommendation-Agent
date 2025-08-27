# subsector_rules.py
# ------------------
# This dictionary maps customer subsectors (their industry/field)
# to the most relevant insurance branches.
# It represents "domain knowledge" to guide recommendations.

subsector_rules =
{
    # --------------------------
    # Agriculture & Food
    # --------------------------
    "AGRICULTURE, CHASSE, SERVICES ANNEXES": ["MULTIRISQUE AGRICOLE", "INCENDIE", "VIE"],
    "PECHE, AQUACULTURE": ["MULTIRISQUE AGRICOLE", "RESPONSABILITÉ CIVILE"],
    "INDUSTRIES ALIMENTAIRES": ["INCENDIE", "MULTIRISQUE INDUSTRIELLE", "RESPONSABILITÉ CIVILE"],
    "BOUCHERIE": ["MULTIRISQUE COMMERCANT", "RESPONSABILITÉ CIVILE"],

    # --------------------------
    # Commerce & Services
    # --------------------------
    "COMMERCE DE DETAIL": ["MULTIRISQUE COMMERCANT", "INCENDIE"],
    "COMMERCE DE GROS": ["MULTIRISQUE COMMERCANT", "TRANSPORT MARCHANDISES"],
    "STATION DE SERVICE": ["MULTIRISQUE COMMERCANT", "RESPONSABILITÉ CIVILE", "INCENDIE"],
    "ACTIVITES IARD TARIFIABLES": ["AUTOMOBILE", "INCENDIE", "RESPONSABILITÉ CIVILE"],

    # --------------------------
    # Transport
    # --------------------------
    "TRANSPORT TERRESTRE": ["AUTOMOBILE", "RESPONSABILITÉ CIVILE"],
    "TRANSPORT AERIEN": ["ASSURANCE AVIATION", "RESPONSABILITÉ CIVILE"],
    "TRANSPORT MARITIME": ["ASSURANCE MARINE", "TRANSPORT MARCHANDISES"],

    # --------------------------
    # Construction & Industry
    # --------------------------
    "CONSTRUCTION": ["DECENNALE", "RESPONSABILITÉ CIVILE", "ACCIDENTS DU TRAVAIL"],
    "INDUSTRIE": ["MULTIRISQUE INDUSTRIELLE", "INCENDIE"],
    "EAU, ENERGIE, ENVIRONNEMENT": ["RESPONSABILITÉ CIVILE", "MULTIRISQUE INDUSTRIELLE"],

    # --------------------------
    # Public & Private Services
    # --------------------------
    "ADMINISTRATION PUBLIQUE": ["RESPONSABILITÉ CIVILE", "VIE COLLECTIVE"],
    "EMPLOYÉS": ["ACCIDENTS DU TRAVAIL", "VIE COLLECTIVE"],
    "SANTÉ ET ACTION SOCIALE": ["MALADIE", "PRÉVOYANCE", "VIE"],
    "EDUCATION": ["VIE", "ASSURANCE SCOLAIRE"],
    "ETUDIANT": ["ASSURANCE SCOLAIRE", "SANTÉ"],

    # --------------------------
    # Financial & Professional
    # --------------------------
    "INTERMEDIATION FINANCIERE": ["RESPONSABILITÉ CIVILE", "VIE"],
    "ASSURANCES ET CAISSES": ["RESPONSABILITÉ CIVILE", "MULTIRISQUE BUREAU"],
    "PROFESSIONS LIBERALES": ["RESPONSABILITÉ CIVILE", "MULTIRISQUE BUREAU", "VIE"],

    # --------------------------
    # Real Estate & Housing
    # --------------------------
    "IMMOBILIER": ["MULTIRISQUE IMMEUBLE", "INCENDIE"],
    "LOCATION": ["MULTIRISQUE IMMEUBLE", "RESPONSABILITÉ CIVILE"],

    # --------------------------
    # Special cases
    # --------------------------
    "SPORT ET LOISIRS": ["ASSURANCE INDIVIDUELLE ACCIDENT", "RESPONSABILITÉ CIVILE"],
    "HOTELS, RESTAURANTS": ["MULTIRISQUE COMMERCANT", "RESPONSABILITÉ CIVILE", "INCENDIE"],
    "INFORMATIQUE ET TELECOM": ["RESPONSABILITÉ CIVILE", "MULTIRISQUE BUREAU"],
}
