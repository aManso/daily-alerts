import json
from pathlib import Path

from providers.fuel import find


CONFIG_PATH = Path("config/config.json")


def update_config(station):

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)

    fuel = config["monitors"]["fuel"]

    fuel["enabled"] = True
    fuel["reference_station_id"] = station.id

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def main():

    print("=" * 60)
    print("               Fuel Station Finder")
    print("=" * 60)

    while True:

        print()

        text = input("Search (empty to exit): ").strip()

        if not text:
            return

        stations = find(text)

        if not stations:
            print("\nNo stations found.")
            continue

        print()

        for i, station in enumerate(stations, start=1):

            print(
                f"[{i}] {station.name}"
            )
            print(f"    ID       : {station.id}")
            print(f"    Address  : {station.address}")
            print(f"    City     : {station.city}")
            print(f"    Price    : {station.price:.3f} €/L")
            print()

        while True:

            option = input(
                "Select station (Enter to search again): "
            ).strip()

            if option == "":
                break

            if not option.isdigit():
                print("Invalid option.")
                continue

            option = int(option)

            if option < 1 or option > len(stations):
                print("Invalid option.")
                continue

            station = stations[option - 1]

            print()
            print(f"Selected: {station.name}")
            print(f"ID: {station.id}")
            print()

            confirm = input(
                "Update config.json? (Y/n): "
            ).strip().lower()

            if confirm in ("", "y", "yes", "s", "si"):

                update_config(station)

                print()
                print("✅ config.json updated.")
                return

            break


if __name__ == "__main__":
    main()