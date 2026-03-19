"""Verified Delegation Protocol — the core defense.

Combines three defense layers:
  1. LLM-as-judge semantic verification (detects poisoned content)
  2. Cryptographic task signing (prevents delegation forgery)
  3. Adaptive rate limiting (escalates verification on anomaly detection)

Each layer can be enabled/disabled independently for ablation.
"""
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .agent import DelegatedTask, AgentResponse, MockAgent
from .judge import JudgeVerdict, MockJudge, create_judge


@dataclass
class ProtocolMetrics:
    """Metrics from a protocol-protected delegation."""
    total_delegations: int = 0
    delegations_blocked: int = 0
    poison_detected_by_judge: int = 0
    signature_failures: int = 0
    rate_limit_escalations: int = 0
    total_latency_ms: float = 0.0
    judge_latency_ms: float = 0.0
    # Per-agent tracking
    agent_poison_counts: dict = field(default_factory=dict)
    agent_decision_counts: dict = field(default_factory=dict)

    @property
    def block_rate(self) -> float:
        return self.delegations_blocked / max(self.total_delegations, 1)

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / max(self.total_delegations, 1)

    def to_dict(self) -> dict:
        total_decisions = sum(self.agent_decision_counts.values())
        total_poisoned = sum(self.agent_poison_counts.values())
        return {
            "total_delegations": self.total_delegations,
            "delegations_blocked": self.delegations_blocked,
            "block_rate": self.block_rate,
            "poison_detected_by_judge": self.poison_detected_by_judge,
            "signature_failures": self.signature_failures,
            "rate_limit_escalations": self.rate_limit_escalations,
            "total_decisions": total_decisions,
            "poisoned_decisions": total_poisoned,
            "poison_rate": total_poisoned / max(total_decisions, 1),
            "avg_latency_ms": self.avg_latency_ms,
            "judge_latency_ms": self.judge_latency_ms,
        }


class VerifiedDelegationProtocol:
    """The verified delegation protocol."""

    def __init__(
        self,
        judge_enabled: bool = True,
        signing_enabled: bool = True,
        rate_limiting_enabled: bool = True,
        judge_mode: str = "mock",
        judge_detection_rate: float = 0.8,
        judge_model: str = "",
        anomaly_threshold: float = 2.0,
        escalation_factor: float = 2.0,
        window_size: int = 5,
        rng: Optional[np.random.Generator] = None,
    ):
        self.judge_enabled = judge_enabled
        self.signing_enabled = signing_enabled
        self.rate_limiting_enabled = rate_limiting_enabled
        self.anomaly_threshold = anomaly_threshold
        self.escalation_factor = escalation_factor
        self.rng = rng or np.random.default_rng(42)

        # Create judge
        if judge_enabled:
            self.judge = create_judge(
                mode=judge_mode,
                detection_rate=judge_detection_rate,
                rng=self.rng,
            ) if judge_mode == "mock" else create_judge(
                mode=judge_mode, model=judge_model,
            )
        else:
            self.judge = None

        # Rate limiting state
        self.recent_blocks: deque = deque(maxlen=window_size)
        self.escalation_active = False
        self.base_verification_rate = 1.0  # Verify every delegation by default

        self.metrics = ProtocolMetrics()

    def verify_delegation(
        self,
        task: DelegatedTask,
        sender_agent: MockAgent,
        response: AgentResponse,
    ) -> tuple[bool, str]:
        """Verify a delegation through the protocol layers.

        Returns (accepted: bool, reason: str).
        """
        start = time.time()
        self.metrics.total_delegations += 1

        # Layer 1: Cryptographic signature verification
        if self.signing_enabled and task.signature:
            expected_sig = sender_agent.sign_task(task)
            if task.signature != expected_sig:
                self.metrics.signature_failures += 1
                self.metrics.delegations_blocked += 1
                return False, "Signature verification failed"

        # Layer 2: LLM-as-judge semantic verification
        if self.judge_enabled and self.judge:
            # Adaptive rate: verify more frequently during escalation
            should_verify = True
            if not self.escalation_active:
                should_verify = self.rng.random() < self.base_verification_rate

            if should_verify:
                verdict = self.judge.verify(
                    output=response.output,
                    task_context=task.content,
                )
                self.metrics.judge_latency_ms += verdict.latency_ms

                if not verdict.passed:
                    self.metrics.poison_detected_by_judge += 1
                    self.metrics.delegations_blocked += 1
                    self._update_rate_limiting(blocked=True)
                    return False, f"Judge rejected: {verdict.reason}"

        # Layer 3: Rate limiting check
        if self.rate_limiting_enabled:
            self._update_rate_limiting(blocked=False)

        self.metrics.total_latency_ms += (time.time() - start) * 1000
        return True, "Accepted"

    def _update_rate_limiting(self, blocked: bool):
        """Update rate limiting state based on recent blocks."""
        self.recent_blocks.append(1 if blocked else 0)

        if len(self.recent_blocks) >= 3:
            recent_block_rate = sum(self.recent_blocks) / len(self.recent_blocks)
            mean_rate = 0.1  # Expected baseline block rate
            std_rate = 0.1

            if recent_block_rate > mean_rate + self.anomaly_threshold * std_rate:
                if not self.escalation_active:
                    self.escalation_active = True
                    self.metrics.rate_limit_escalations += 1
            else:
                self.escalation_active = False

    def track_decision(self, agent_id: int, is_poisoned: bool):
        """Track per-agent decision outcomes."""
        self.metrics.agent_decision_counts[agent_id] = \
            self.metrics.agent_decision_counts.get(agent_id, 0) + 1
        if is_poisoned:
            self.metrics.agent_poison_counts[agent_id] = \
                self.metrics.agent_poison_counts.get(agent_id, 0) + 1

    def reset(self):
        """Reset protocol state for new run."""
        self.metrics = ProtocolMetrics()
        self.recent_blocks.clear()
        self.escalation_active = False
        if hasattr(self.judge, 'total_checks'):
            self.judge.total_checks = 0
            self.judge.poison_detected = 0


def create_defense(defense_type: str, rng=None, **kwargs) -> Optional[VerifiedDelegationProtocol]:
    """Factory: create defense by type."""
    if defense_type == "none":
        return None
    elif defense_type == "static_zero_trust":
        return VerifiedDelegationProtocol(
            judge_enabled=True, signing_enabled=False,
            rate_limiting_enabled=False, judge_detection_rate=0.8,
            rng=rng, **kwargs,
        )
    elif defense_type == "verified_delegation":
        return VerifiedDelegationProtocol(
            judge_enabled=True, signing_enabled=True,
            rate_limiting_enabled=True, judge_detection_rate=0.85,
            rng=rng, **kwargs,
        )
    elif defense_type == "oracle":
        return VerifiedDelegationProtocol(
            judge_enabled=True, signing_enabled=True,
            rate_limiting_enabled=True, judge_detection_rate=0.99,
            rng=rng, **kwargs,
        )
    elif defense_type == "judge_only":
        return VerifiedDelegationProtocol(
            judge_enabled=True, signing_enabled=False,
            rate_limiting_enabled=False, judge_detection_rate=0.85,
            rng=rng, **kwargs,
        )
    elif defense_type == "signing_only":
        return VerifiedDelegationProtocol(
            judge_enabled=False, signing_enabled=True,
            rate_limiting_enabled=False, rng=rng, **kwargs,
        )
    elif defense_type == "rate_limit_only":
        return VerifiedDelegationProtocol(
            judge_enabled=False, signing_enabled=False,
            rate_limiting_enabled=True, rng=rng, **kwargs,
        )
    else:
        raise ValueError(f"Unknown defense: {defense_type}")
