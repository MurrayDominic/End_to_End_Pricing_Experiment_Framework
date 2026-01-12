from dataclasses import dataclass
from typing import Literal


@dataclass
class PolicySchema:
    age: int
    gender: Literal["M", "F"]
    region: str
    tenure: float
    smoker: Literal["Y", "N"]
    bmi: Literal["Underweight", "Normal", "Overweight", "Obese"]
    plan: Literal["Budget", "Standard", "Premium"]
    ncd: Literal["0", "10", "20", "30"]
    excess: Literal["0", "250", "500", "1000", "2000"]

def validate_policy_df(df):
    assert df["age"].between(0, 100).all()
    assert df["tenure"].between(0, 30).all()
    assert df["smoker"].isin(["Y", "N"]).all()