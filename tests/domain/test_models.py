from lilac.domain.models import BaseModel


def test_base_model_import() -> None:
    assert BaseModel.__name__ == "BaseModel"
