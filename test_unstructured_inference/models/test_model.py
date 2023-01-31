import pytest

import unstructured_inference.models.base as models
from unstructured_inference.models.unstructuredmodel import ModelNotInitializedError


class MockModel:
    def initialize(self, *args, **kwargs):
        pass


def test_get_model(monkeypatch):

    monkeypatch.setattr(
        models,
        "UnstructuredDetectronModel",
        MockModel,
    )
    assert isinstance(models.get_model("checkbox"), MockModel)


def test_raises_invalid_model():
    with pytest.raises(models.UnknownModelException):
        models.get_model("fake_model")


def test_raises_uninitialized():
    with pytest.raises(ModelNotInitializedError):
        models.UnstructuredDetectronModel().predict(None)
