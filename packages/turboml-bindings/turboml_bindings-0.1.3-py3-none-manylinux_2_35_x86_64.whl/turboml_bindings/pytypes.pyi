"""
This file contains interfaces for types provided by our native `pytypes` module.
"""

from __future__ import annotations
import numpy
import numpy.typing

class InputData:
    numeric: list[float]
    categ: list[int]
    text: list[str]
    images: list[str]
    time_tick: int
    label: int
    key: str

    @staticmethod
    def random() -> InputData:
        """Creates a random InputData instance."""
        pass

class OutputData:
    @staticmethod
    def random() -> OutputData:
        """Creates a random OutputData instance."""
        pass

    def set_score(self, score: float):
        """Sets the score."""
        pass

    def set_predicted_class(self, predicted_class: int):
        """Sets the predicted class."""
        pass

    def feature_scores(self) -> numpy.typing.NDArray[numpy.float32]:
        """Returns a mutable array of feature scores.
        Note that any resizing of the array should be done using the
        `resize_feature_scores` method
        """
        pass

    def append_feature_score(self, score: float):
        """Appends a feature score to the end of the array.
        Note that this method should not be used in conjunction with
        `resize_feature_scores`.
        """
        pass

    def resize_feature_scores(self, size: int):
        """Resizes the feature scores array to the specified size."""
        pass

    def class_probabilities(self) -> numpy.typing.NDArray[numpy.float32]:
        """Returns a mutable array of class probabilities.
        Note that any resizing of the array should be done using the
        `resize_class_probabilities` method.
        """
        pass

    def append_class_probability(self, probability: float):
        """Appends a class probability to the end of the array.
        Note that this method should not be used in conjunction with
        `resize_class_probabilities`.
        """
        pass

    def resize_class_probabilities(self, size: int):
        """Resizes the class probabilities array to the specified size."""
        pass

    def text_output(self) -> str:
        """Returns the text output as a string."""
        pass

    def set_text_output(self, text: str):
        """Sets the text output to the specified string."""
        pass

    def embeddings(self) -> numpy.typing.NDArray[numpy.float32]:
        """Returns a numpy array of embeddings.
        Note that any resizing of the array should be done using the
        `resize_embeddings` method.
        """
        pass

    def append_embedding(self, embedding: float):
        """Appends an embedding to the end of the array.
        Note that this method should not be used in conjunction with
        `resize_embeddings`.
        """
        pass

    def resize_embeddings(self, size: int):
        """Resizes the embeddings array to the specified size."""
        pass
