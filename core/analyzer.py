def analyze(results):

    analysis = {
        "sections": [],
        "alerts": []
    }

    for result in results:

        if result["title"] == "Portfolio":

            assets = result["data"]

            if not assets:
                continue

            portfolio_value = round(
                sum(asset["base_position_value"] for asset in assets),
                2
            )

            best = max(
                assets,
                key=lambda asset: asset["daily_change"]
            )

            worst = min(
                assets,
                key=lambda asset: asset["daily_change"]
            )

            analysis["sections"].append({

                "title": "💼 Cartera",

                "lines": [

                    f"Valor: {portfolio_value:.2f} {best['base_currency']}",

                    f"🏆 {best['name']} ({best['daily_change']:+.2f}%)",

                    f"📉 {worst['name']} ({worst['daily_change']:+.2f}%)"

                ]

            })

            for asset in assets:

                alerts = asset.get("alerts")

                if not alerts:
                    continue

                target = alerts.get("target")
                stop = alerts.get("stop")

                if target is not None and asset["current_price"] >= target:

                    analysis["alerts"].append(
                        f"🎯 {asset['name']} ha alcanzado el target."
                    )

                if stop is not None and asset["current_price"] <= stop:

                    analysis["alerts"].append(
                        f"🛑 {asset['name']} ha alcanzado el stop."
                    )

        elif result["title"] == "BOE":

            calls = result["data"]

            for call in calls:

                analysis["alerts"].append(
                    f"🚆 Nueva convocatoria de ADIF\n{call['id']}\n{call['url']}"
                )

        elif result["title"] == "Fuel":
            analysis["alerts"].append(analyze_fuel(result["data"]))
        
        analysis["alerts"].extend(
            result["alerts"]
        )

    return analysis

def analyze_fuel(data):

    reference = data["reference_station"]
    cheapest = data["cheapest_station"]
    radius = data["radius_km"]

    return (
        "⛽ Combustible\n\n"
        f"📍 Tu gasolinera\n"
        f"{reference.name} → {reference.price:.3f} €/L\n\n"
        f"🥇 Más barata ({radius} km)\n"
        f"{cheapest.name} → {cheapest.price:.3f} €/L\n\n"
    )

