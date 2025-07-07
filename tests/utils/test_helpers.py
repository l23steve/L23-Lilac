from lilac.utils.helpers import helper, sanitize_filename


def test_helper() -> None:
    assert helper() is True


def test_sanitize_filename() -> None:
    assert sanitize_filename("my bucket/v1") == "my_bucket_v1"
