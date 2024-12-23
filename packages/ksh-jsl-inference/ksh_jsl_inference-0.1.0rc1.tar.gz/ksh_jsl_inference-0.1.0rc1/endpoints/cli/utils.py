from endpoints.container.base_inference_model import BaseInferenceModel
from typing import Optional
import os
import importlib
from logging import getLogger


logger = getLogger(__name__)


def get_inference_model_from_path(
    inference_model: str, legacy: bool = False
) -> Optional[BaseInferenceModel] | str:
    """
    Load the inference model.
    If legacy=True, the inference logic is loaded from the specified path.
    """
    if legacy:
        if os.path.isfile(inference_model):
            return inference_model
        raise ValueError("Inference model path is required.")
    else:
        if not inference_model:
            raise ValueError("Inference model is required.")

        logger.info(f"Loading inference model: {inference_model}")
        module_name, class_name = inference_model.rsplit(".", 1)
        module = importlib.import_module(module_name)
        inference_class = getattr(module, class_name)
        return inference_class()
