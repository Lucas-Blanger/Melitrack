LEVELS = [
    (0.25, "baixa", "500–1.500"),
    (0.50, "média", "1.500–3.000"),
    (0.75, "alta", "3.000–5.000"),
    (1.01, "muito alta", "5.000+"),
]


def interpret(density_score: float) -> dict:
    for threshold, level, estimated_count in LEVELS:
        if density_score < threshold:
            return {
                "density_score": round(density_score, 4),
                "level": level,
                "estimated_count": estimated_count,
            }
    return {
        "density_score": round(density_score, 4),
        "level": "muito alta",
        "estimated_count": "5.000+",
    }
