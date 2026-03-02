import pandas as pd
from modules.predictor import prepare_data


def test_result_column_exists():
    df = pd.DataFrame({
        "home_score": [2, 1, 1],
        "away_score": [1, 2, 1]
    })
    result = prepare_data(df)
    assert "result" in result.columns


def test_correct_results():
    df = pd.DataFrame({
        "home_score": [2, 1, 1],
        "away_score": [1, 2, 1]
    })
    result = prepare_data(df)
    assert list(result["result"]) == ["H", "A", "D"]


def test_no_nulls_after_prepare():
    df = pd.DataFrame({
        "home_score": [2, None, 1],
        "away_score": [1, 2, 1]
    })
    result = prepare_data(df)
    assert result.isnull().sum().sum() == 0