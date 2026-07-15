import json

from dotenv import load_dotenv
load_dotenv()
from config import CONFIG_FILE

from core.state import load_state
from core.state import save_state

from core.analyzer import analyze
from core.formatter import build_report
from core.notifier import send_whatsapp

from monitors.portfolio import check as check_portfolio
from monitors.boe import check as check_boe
from monitors.fuel import check as check_fuel

def load_config():

    with open(
        CONFIG_FILE,
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    config = load_config()

    state = load_state()

    results = []

    monitors = config["monitors"]

    if monitors["portfolio"]["enabled"]:
        try:
            results.append(
                check_portfolio(
                    config["portfolio"],
                    config["settings"],
                    state
                )
            )
        except Exception as e:
            print(f"Error checking portfolio: {e}")
            results.append({
                "title": "Portfolio",
                "data": [],
                "alerts": [
                    "⚠️ Portfolio monitor unavailable today."
                ]
            })

    if monitors["boe"]["enabled"]:
        try:
            results.append(
                check_boe(state)
            )
        except Exception as e:
            print(f"Error checking BOE: {e}")
            results.append({
                "title": "BOE",
                "data": [],
                "alerts": [
                    "⚠️ BOE monitor unavailable today."
                ]
            })

    if monitors["fuel"]["enabled"]:
        try:
            results.append(
                check_fuel(
                    state,
                    monitors["fuel"],
                    config["settings"]
                )
            )
        except Exception as e:
            print(f"Error checking fuel: {e}")
            results.append({
                "title": "Fuel",
                "data": [],
                "alerts": [
                    "⚠️ Fuel monitor unavailable today."
                ]
            })

    print(f"Results: {results}")

    save_state(state)

    print("Analyzing results...")

    analysis = analyze(results)

    print("Building report...")

    report = build_report(analysis)

    print(f"Sending WhatsApp report... {report}")

    send_whatsapp(report)


if __name__ == "__main__":
    main()