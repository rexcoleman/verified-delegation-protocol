"""Tests for verified delegation protocol."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from src.agent import MockAgent, DelegatedTask, create_agent
from src.judge import MockJudge
from src.protocol import VerifiedDelegationProtocol, create_defense
from src.testbed import Testbed


class TestMockAgent:
    def test_clean_agent(self):
        agent = MockAgent(agent_id=0, role="analyst")
        task = DelegatedTask(task_id=0, content="test", source_agent_id=-1, target_agent_id=0)
        resp = agent.process_task(task)
        assert not resp.is_poisoned

    def test_compromised_agent(self):
        agent = MockAgent(agent_id=0, role="analyst", compromised=True,
                         attack_payload="buy CryptoScamCoin")
        task = DelegatedTask(task_id=0, content="test", source_agent_id=-1, target_agent_id=0)
        resp = agent.process_task(task)
        assert resp.is_poisoned
        assert "CryptoScamCoin" in resp.output

    def test_signing(self):
        agent = MockAgent(agent_id=0, role="analyst")
        task = DelegatedTask(task_id=0, content="test", source_agent_id=0, target_agent_id=1)
        sig = agent.sign_task(task)
        assert len(sig) == 16
        # Same task, same signature
        assert agent.sign_task(task) == sig

    def test_create_agent_factory(self):
        agent = create_agent(0, "analyst", mode="mock")
        assert isinstance(agent, MockAgent)


class TestMockJudge:
    def test_clean_output_passes(self):
        judge = MockJudge(detection_rate=0.8)
        verdict = judge.verify("Clean analysis of quarterly data")
        assert verdict.passed

    def test_poisoned_output_detected(self):
        judge = MockJudge(detection_rate=1.0)  # Perfect detection
        verdict = judge.verify("Buy CryptoScamCoin for investment opportunities")
        assert not verdict.passed

    def test_detection_rate(self):
        rng = np.random.default_rng(42)
        judge = MockJudge(detection_rate=0.5, rng=rng)
        detected = 0
        for _ in range(100):
            v = judge.verify("investment in CryptoScamCoin recommended")
            if not v.passed:
                detected += 1
        assert 30 < detected < 70  # ~50% detection


class TestProtocol:
    def test_no_defense(self):
        defense = create_defense("none")
        assert defense is None

    def test_verified_delegation_creates(self):
        defense = create_defense("verified_delegation")
        assert defense is not None
        assert defense.judge_enabled
        assert defense.signing_enabled
        assert defense.rate_limiting_enabled

    def test_static_zt(self):
        defense = create_defense("static_zero_trust")
        assert defense.judge_enabled
        assert not defense.signing_enabled
        assert not defense.rate_limiting_enabled

    def test_judge_blocks_poison(self):
        rng = np.random.default_rng(42)
        defense = create_defense("verified_delegation", rng=rng)
        defense.judge = MockJudge(detection_rate=1.0, rng=rng)

        agent = MockAgent(0, "analyst", compromised=True,
                         attack_payload="buy CryptoScamCoin", rng=rng)
        task = DelegatedTask(task_id=0, content="test", source_agent_id=0, target_agent_id=1)
        resp = agent.process_task(task)
        accepted, reason = defense.verify_delegation(task, agent, resp)
        assert not accepted

    def test_clean_passes(self):
        rng = np.random.default_rng(42)
        defense = create_defense("verified_delegation", rng=rng)
        agent = MockAgent(0, "analyst", rng=rng)
        task = DelegatedTask(task_id=0, content="test", source_agent_id=0, target_agent_id=1)
        resp = agent.process_task(task)
        accepted, _ = defense.verify_delegation(task, agent, resp)
        assert accepted

    def test_ablation_signing_only(self):
        defense = create_defense("signing_only")
        assert not defense.judge_enabled
        assert defense.signing_enabled
        assert not defense.rate_limiting_enabled


class TestTestbed:
    def test_no_defense_run(self):
        tb = Testbed(n_agents=3, defense_type="none", seed=42)
        result = tb.run(n_tasks=5)
        assert result.total_decisions > 0
        assert result.poison_rate > 0  # Compromised agent at id=0

    def test_verified_delegation_reduces_poison(self):
        # No defense
        tb1 = Testbed(n_agents=3, defense_type="none", seed=42)
        r1 = tb1.run(n_tasks=10)

        # Verified delegation
        tb2 = Testbed(n_agents=3, defense_type="verified_delegation", seed=42)
        r2 = tb2.run(n_tasks=10)

        assert r2.poison_rate <= r1.poison_rate

    def test_reproducibility(self):
        tb1 = Testbed(n_agents=3, defense_type="verified_delegation", seed=42)
        r1 = tb1.run(n_tasks=5)
        tb2 = Testbed(n_agents=3, defense_type="verified_delegation", seed=42)
        r2 = tb2.run(n_tasks=5)
        assert r1.poison_rate == r2.poison_rate

    def test_scaling(self):
        for n in [3, 5, 10]:
            tb = Testbed(n_agents=n, defense_type="verified_delegation", seed=42)
            result = tb.run(n_tasks=5)
            assert result.total_decisions > 0
