"""Every calculator must declare a health topic with a unique, stable key."""

from __future__ import annotations

import pytest

from app.domain.value_objects.health_topic import HealthTopic
from app.presentation.api.dependencies import get_scoring_engine


def test_every_calculator_declares_a_unique_topic() -> None:
    topics = get_scoring_engine().topics_by_score()

    assert len(topics) == 9
    keys = [topic.key for topic in topics.values()]
    assert len(keys) == len(set(keys))


def test_topic_keys_match_organization_weight_keys() -> None:
    topics = get_scoring_engine().topics_by_score()

    assert {score_id: topic.key for score_id, topic in topics.items()} == {
        "findrisc": "diabetes",
        "stop_bang": "sleep_apnea",
        "phq9": "depression",
        "metabolic_syndrome": "metabolic_syndrome",
        "eoss": "eoss",
        "score2": "cardiovascular",
        "nordic_nmq": "nordic_nmq",
        "audit_c": "audit_c",
        "pss10": "pss10",
    }


@pytest.mark.parametrize("key,label", [("", "Label"), ("key", " ")])
def test_health_topic_rejects_empty_values(key: str, label: str) -> None:
    with pytest.raises(ValueError):
        HealthTopic(key=key, label=label)
