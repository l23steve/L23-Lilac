from lilac.services.operations import placeholder_service


def test_placeholder_service() -> None:
    assert placeholder_service() is True
