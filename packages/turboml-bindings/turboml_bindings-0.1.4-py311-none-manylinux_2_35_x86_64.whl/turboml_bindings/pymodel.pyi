"""
This file contains interfaces for types provided by our `pymodel` module.
"""

from turboml_bindings.pytypes import InputData, OutputData

def create_model_from_config(
    config_json: str,
    input_config_json: str,
) -> "Model":
    """Creates a model from the given configuration and returns a Model instance."""
    pass

class Model:
    def predict_one(self, input_data: InputData) -> OutputData:
        """Predicts using the model."""
        pass

    def learn_one(self, input_data: InputData) -> None:
        """Trains the model on a single data point."""
        pass

    def serialize(self) -> bytes:
        """Serializes the model and returns bytes."""
        pass

    def __eq__(self, other: "Model") -> bool:
        """Compares two models for equality."""
        pass

    def __repr__(self) -> str:
        """Returns a string representation of the model."""
        pass
