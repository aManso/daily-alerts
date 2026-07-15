from providers.fuel import search


def check(state, config, settings):

    print("Checking fuel prices...")

    result = search(
        reference_station_id=config["reference_station_id"],
        radius_km=config["radius_km"],
        fuel_type=config["fuel_type"],
        use_cache=settings["development"]
    )

    messages = []

    #
    # Daily report
    #

    messages.append(
        "⛽ Combustible\n\n"
        f"📍 Tu gasolinera\n"
        f"{result.reference_station.name}\n"
        f"{result.reference_station.price:.3f} €/L\n\n"
        f"🥇 Más barata ({config['radius_km']} km)\n"
        f"{result.cheapest_station.name}\n"
        f"{result.cheapest_station.price:.3f} €/L"
    )

    #
    # Alerts
    #

    previous = state.get("fuel")

    if previous:

        #
        # Reference station
        #

        if previous["reference_station"]["price"] != result.reference_station.price:

            direction = "⬆" if result.reference_station.price > previous["reference_station"]["price"] else "⬇"

            messages.append(
                "⛽ Tu gasolinera ha cambiado de precio\n\n"
                f"{result.reference_station.name}\n\n"
                f"{previous['reference_station']['price']:.3f} €/L\n"
                f"{direction}\n"
                f"{result.reference_station.price:.3f} €/L"
            )

        #
        # Cheapest station price
        #

        if previous["cheapest_station"]["price"] != result.cheapest_station.price:

            direction = "⬆" if result.cheapest_station.price > previous["cheapest_station"]["price"] else "⬇"

            messages.append(
                "⛽ La gasolinera más barata ha cambiado de precio\n\n"
                f"{result.cheapest_station.name}\n\n"
                f"{previous['cheapest_station']['price']:.3f} €/L\n"
                f"{direction}\n"
                f"{result.cheapest_station.price:.3f} €/L"
            )

        #
        # Cheapest station changed
        #

        if previous["cheapest_station"]["id"] != result.cheapest_station.id:

            messages.append(
                "🥇 Nueva gasolinera más barata\n\n"
                f"{result.cheapest_station.name}\n"
                f"{result.cheapest_station.price:.3f} €/L"
            )

    #
    # Update state
    #

    state["fuel"] = {
        "reference_station": {
            "id": result.reference_station.id,
            "price": result.reference_station.price,
        },
        "cheapest_station": {
            "id": result.cheapest_station.id,
            "price": result.cheapest_station.price,
        },
    }

    return {
        "title": "Fuel",
        "data": {
            "reference_station": result.reference_station,
            "cheapest_station": result.cheapest_station,
            "radius_km": config["radius_km"],
        },
        "alerts": []
    }
