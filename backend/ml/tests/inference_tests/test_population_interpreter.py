from app.inference.population.interpreter import interpret


def test_interpret_low_population():
    assert interpret(0.10) == {
        "density_score": 0.1,
        "level": "baixa",
        "estimated_count": "500–1.500",
    }


def test_interpret_medium_population_boundary():
    assert interpret(0.25) == {
        "density_score": 0.25,
        "level": "média",
        "estimated_count": "1.500–3.000",
    }


def test_interpret_high_population():
    assert interpret(0.60) == {
        "density_score": 0.6,
        "level": "alta",
        "estimated_count": "3.000–5.000",
    }


def test_interpret_very_high_population():
    assert interpret(0.95) == {
        "density_score": 0.95,
        "level": "muito alta",
        "estimated_count": "5.000+",
    }
