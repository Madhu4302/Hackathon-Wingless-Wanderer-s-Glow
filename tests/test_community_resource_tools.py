import pytest

from coded_tools.basic.community_resource_tools.resource_finder import ResourceFinder
from coded_tools.basic.community_resource_tools.eligibility_checker import EligibilityChecker
from coded_tools.basic.community_resource_tools.verification_agent import VerificationAgent
from coded_tools.basic.community_resource_tools.coordinator import Coordinator


def test_resource_finder_basic():
    rf = ResourceFinder()
    res = rf.invoke({"location": "Seattle", "service_type": "food bank"}, {})
    assert "resources" in res
    assert len(res["resources"]) >= 1


def test_eligibility_checker_basic():
    ec = EligibilityChecker()
    out = ec.invoke({"resource_id": "res-1", "household": {"household_size": 5, "income_bracket": "low"}}, {})
    assert out["eligibility"] in ("likely", "needs_documents", "unlikely")


def test_verification_agent_basic():
    va = VerificationAgent()
    rec = {"id": "res-1", "phone": "+1-555-0101", "website": "https://example.org", "source": "test"}
    out = va.invoke({"resource_record": rec}, {})
    assert out["verification_confidence"] == "high"


def test_coordinator_basic():
    co = Coordinator()
    out = co.invoke({"task": "volunteer_delivery", "details": {}}, {})
    assert "checklist" in out or "steps" in out
