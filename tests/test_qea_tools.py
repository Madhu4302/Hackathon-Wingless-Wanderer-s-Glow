import pytest

from coded_tools.basic.qea_tools.scenario_generator import ScenarioGenerator
from coded_tools.basic.qea_tools.env_planner import EnvPlanner
from coded_tools.basic.qea_tools.test_data_generator import TestDataGenerator
from coded_tools.basic.qea_tools.risk_analyzer import RiskAnalyzer


def test_scenario_generator_basic():
    sg = ScenarioGenerator()
    out = sg.invoke({"system": "payments", "goal": "regression"}, {})
    assert "scenarios" in out and len(out["scenarios"]) >= 1


def test_env_planner_basic():
    ep = EnvPlanner()
    out = ep.invoke({"scale": "medium"}, {})
    assert "components" in out and "sizes" in out


def test_test_data_generator_basic():
    td = TestDataGenerator()
    out = td.invoke({"data_domains": ["users", "payments"], "privacy_level": "high"}, {})
    assert out["privacy_level"] == "high"
    assert len(out["strategies"]) == 2


def test_risk_analyzer_basic():
    ra = RiskAnalyzer()
    failures = [{"description": "Intermittent timeout calling downstream API"}]
    out = ra.invoke({"recent_failures": failures, "test_type": "integration"}, {})
    assert "probable_causes" in out
