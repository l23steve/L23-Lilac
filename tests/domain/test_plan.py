from lilac.domain.models import Resource
from lilac.domain.plan import diff_resources


def _res(name: str, props: dict | None = None, ignore: bool = False) -> Resource:
    return Resource(
        resource_type=name,
        namespace="ns",
        depends_on=[],
        properties=props or {},
        ignore=ignore,
    )


def test_diff_create_update_delete() -> None:
    desired = [_res("a", {"x": 1}), _res("b", {"y": 2})]
    actual = [_res("a", {"x": 2}), _res("c", {"z": 3})]

    actions = diff_resources(desired, actual)

    assert len(actions) == 3
    assert {a.action for a in actions} == {"create", "update", "delete"}


def test_diff_ignore_flag() -> None:
    desired = [_res("a", ignore=True)]
    actual = []

    actions = diff_resources(desired, actual)

    assert actions == []


def test_diff_ignores_details() -> None:
    desired = [_res("a", {"x": 1, "details": {"something": 1}})]
    actual = [_res("a", {"x": 1, "details": {"something": 2}})]

    actions = diff_resources(desired, actual)

    assert actions == []


def test_diff_multiple_resources_same_type() -> None:
    desired = [_res("a", {"name": "one"}), _res("a", {"name": "two"})]
    actual = [_res("a", {"name": "one"}), _res("a", {"name": "two"})]

    actions = diff_resources(desired, actual)

    assert actions == []


def test_diff_multiple_resources_update() -> None:
    desired = [
        _res("a", {"name": "one", "region": "us"}),
        _res("a", {"name": "two", "region": "eu"}),
    ]
    actual = [
        _res("a", {"name": "one", "region": "us"}),
        _res("a", {"name": "two", "region": "us"}),
    ]

    actions = diff_resources(desired, actual)

    assert len(actions) == 1
    assert actions[0].action == "update"
    assert actions[0].resource.properties["name"] == "two"
