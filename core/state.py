import json

from config import STATE_FILE


def load_state():

    try:

        with open(STATE_FILE, encoding="utf-8") as file:

            return json.load(file)

    except FileNotFoundError:

        return {}


def save_state(state):

    with STATE_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            ensure_ascii=False,
            indent=4,
            sort_keys=True
        )