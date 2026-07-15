def build_report(analysis):

    report = []

    report.append("📅 Informe diario")
    report.append("")

    for section in analysis["sections"]:

        report.append(section["title"])

        for line in section["lines"]:
            report.append(line)

        report.append("")

    if analysis["alerts"]:

        report.append("🚨 Alertas")

        for alert in analysis["alerts"]:
            report.append(f"• {alert}")

    else:

        report.append("✅ Sin alertas")

    return "\n".join(report)