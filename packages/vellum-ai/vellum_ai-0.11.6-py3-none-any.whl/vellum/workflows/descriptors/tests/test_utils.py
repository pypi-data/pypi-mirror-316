import pytest

from vellum.workflows.descriptors.utils import resolve_value
from vellum.workflows.state.base import BaseState


class FixtureState(BaseState):
    alpha = 1
    beta = 2

    gamma = "hello"
    delta = "el"

    epsilon = 3
    zeta = {
        "foo": "bar",
    }


@pytest.mark.parametrize(
    ["descriptor", "expected_value"],
    [
        (FixtureState.alpha | FixtureState.beta, 1),
        (FixtureState.alpha & FixtureState.beta, 2),
        (FixtureState.beta.coalesce(FixtureState.alpha), 2),
        (FixtureState.alpha.equals(FixtureState.beta), False),
        (FixtureState.alpha.does_not_equal(FixtureState.beta), True),
        (FixtureState.alpha.less_than(FixtureState.beta), True),
        (FixtureState.alpha.greater_than(FixtureState.beta), False),
        (FixtureState.alpha.less_than_or_equal_to(FixtureState.beta), True),
        (FixtureState.alpha.greater_than_or_equal_to(FixtureState.beta), False),
        (FixtureState.gamma.contains(FixtureState.delta), True),
        (FixtureState.gamma.begins_with(FixtureState.delta), False),
        (FixtureState.gamma.ends_with(FixtureState.delta), False),
        (FixtureState.gamma.does_not_contain(FixtureState.delta), False),
        (FixtureState.gamma.does_not_begin_with(FixtureState.delta), True),
        (FixtureState.gamma.does_not_end_with(FixtureState.delta), True),
        (FixtureState.alpha.is_none(), False),
        (FixtureState.alpha.is_not_none(), True),
        (FixtureState.delta.in_(FixtureState.gamma), True),
        (FixtureState.delta.not_in(FixtureState.gamma), False),
        (FixtureState.alpha.between(FixtureState.beta, FixtureState.epsilon), False),
        (FixtureState.alpha.not_between(FixtureState.beta, FixtureState.epsilon), True),
        (FixtureState.delta.is_blank(), False),
        (FixtureState.delta.is_not_blank(), True),
        (
            FixtureState.alpha.equals(FixtureState.alpha)
            | FixtureState.alpha.equals(FixtureState.beta) & FixtureState.alpha.equals(FixtureState.beta),
            True,
        ),
        (FixtureState.zeta["foo"], "bar"),
    ],
    ids=[
        "or",
        "and",
        "coalesce",
        "eq",
        "dne",
        "less_than",
        "greater_than",
        "less_than_or_equal_to",
        "greater_than_or_equal_to",
        "contains",
        "begins_with",
        "ends_with",
        "does_not_contain",
        "does_not_begin_with",
        "does_not_end_with",
        "is_none",
        "is_not_none",
        "in_",
        "not_in",
        "between",
        "not_between",
        "is_blank",
        "is_not_blank",
        "or_and",
        "accessor",
    ],
)
def test_resolve_value__happy_path(descriptor, expected_value):
    actual_value = resolve_value(descriptor, FixtureState())
    assert actual_value == expected_value
