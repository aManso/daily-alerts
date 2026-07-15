from providers.boe import search, contains_keywords


KEYWORDS = [
    "OFERTA DE EMPLEO",
    "CONVOCATORIA",
    "PROCESO SELECTIVO",
    "PERSONAL LABORAL"
]


def check(state):
    print("Checking BOE...")

    try:

        results = search("ADIF oferta de empleo")

        results = [
            result
            for result in results
            if contains_keywords(
                result["title"],
                KEYWORDS
            )
        ]

        boe_state = state.setdefault("boe", {})
        adif_state = boe_state.setdefault("ADIF", {})
        seen = set(adif_state.setdefault("seen", []))

        new_calls = []

        for result in results:

            if result["id"] in seen:
                continue

            new_calls.append({
                "source": "ADIF",
                **result
            })
            seen.add(result["id"])

        adif_state["seen"] = list(seen)

        return {
            "title": "BOE",
            "data": new_calls,
            "alerts": []
        }
    
    except Exception as e:

        print(f"BOE monitor failed: {e}")

        return {
            "title": "BOE",
            "data": [],
            "alerts": []
        }