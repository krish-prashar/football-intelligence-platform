from modules.fantasy import optimize_team


def test_team_within_budget():
    team, total = optimize_team(budget=83.0)
    assert total <= 83.0


def test_team_max_11_players():
    team, total = optimize_team(budget=83.0)
    assert len(team) <= 11


def test_team_has_goalkeeper():
    team, total = optimize_team(budget=83.0)
    positions = list(team["position"])
    assert "GK" in positions