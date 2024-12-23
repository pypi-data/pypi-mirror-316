from typing import Optional
import inspect
import os
import shutil
import uuid

from endpoints.container.base_inference_model import BaseInferenceModel
from endpoints.utils import Platform, Recipe


DEFAULT_JOHNSNOWLABS_VERSION = "5.5.0"

current_dir = os.path.dirname(__file__)


def get_default_output_dir(platform: Platform) -> str:
    """
    Generates the default output directory under the user's home folder
    for the given platform.
    """
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".jsl_inference", platform.value, str(uuid.uuid4()))


def _get_requirements(
    johnsnowlabs_version: str = DEFAULT_JOHNSNOWLABS_VERSION,
    additional_packages: list = [],
):
    """
    Generates a list of requirements for the Docker environment.

    Args:
        johnsnowlabs_version (str): The version of the John Snow Labs library.
        additional_packages (list): List of additional Python packages.

    Returns:
        list: A list of requirements.
    """
    return [
        f"johnsnowlabs=={johnsnowlabs_version}",
        "fastapi",
        "uvicorn",
    ] + additional_packages


def _generate_healthcare_nlp_docker_files(
    model_to_serve: str,
    output_dir: str,
    inference: Optional[BaseInferenceModel | str],
    johnsnowlabs_version="5.4.0",
    store_license=True,
    store_model=True,
    language="en",
    additional_packages=[],
    sagemaker=False,
    snowflake=False,
    legacy=False,
):
    if legacy:
        os.makedirs(output_dir, exist_ok=True)

        shutil.copytree(f"{current_dir}/templates/", output_dir, dirs_exist_ok=True)

        with open(f"{output_dir}/requirements.txt", "w+") as f:
            f.write(
                "\n".join(_get_requirements(johnsnowlabs_version, additional_packages))
            )

        with open(f"{output_dir}/Dockerfile", "r+") as f:
            docker_template = f.read()
            f.seek(0)
            f.truncate()
            f.write(
                docker_template.replace(
                    "{{JOHNSNOWLABS_VERSION}}", johnsnowlabs_version
                )
                .replace("{{STORE_LICENSE}}", str(store_license))
                .replace("{{STORE_MODEL}}", str(store_model))
                .replace("{{MODEL_TO_LOAD}}", model_to_serve)
                .replace("{{LANGUAGE}}", language)
            )

        if not sagemaker:
            os.remove(f"{output_dir}/routers/sagemaker.py")
        if not snowflake:
            os.remove(f"{output_dir}/routers/snowflake.py")

        with open(f"{output_dir}/app.py", "a+") as f:
            if sagemaker:
                f.write("from routers import sagemaker\n")
                f.write("app.include_router(sagemaker.router)\n")
            if snowflake:
                f.write("from routers import snowflake\n")
                f.write("app.include_router(snowflake.router)\n")

        if isinstance(inference, str):
            shutil.copy(inference, f"{output_dir}/endpoint_logic.py")
    else:
        pass

    return output_dir


def generate_docker_files(
    model: str,
    recipe: Recipe,
    output_dir: str,
    inference_model: Optional[BaseInferenceModel] | str = None,
    context: dict = {},
    legacy=False,
) -> str:

    if recipe == Recipe.HEALTHCARE_NLP:
        inference_obj = inference_model
        if not legacy:
            from endpoints.johnsnowlabs.inference_model import MedicalNlpInferenceModel

            if inference_model and not issubclass(
                inference_model.__class__, MedicalNlpInferenceModel
            ):
                raise ValueError("Inference class must inherit from MedicalNlpModel")

            inference_obj = inference_model or MedicalNlpInferenceModel()

        return _generate_healthcare_nlp_docker_files(
            model_to_serve=model,
            inference=inference_obj,
            output_dir=output_dir,
            legacy=legacy,
            **context,
        )
    else:
        raise NotImplementedError(f"Recipe '{recipe}' is not implemented.")


def is_valid_output_dir(directory: str) -> bool:
    """
    Validates if the specified directory contains the required Docker files.

    Args:
        directory (str): Path to the directory to validate.

    Returns:
        bool: True if the directory contains the required files, False otherwise.
    """
    if not directory or not os.path.isdir(directory):
        return False

    required_files = ["Dockerfile", "requirements.txt"]
    return all(os.path.isfile(os.path.join(directory, file)) for file in required_files)


def get_inference_model():

    from endpoints.models.explain_clinical_doc_cancer_type_en.docker.oncology_inference_model import (
        OnCologyInferenceModel,
    )

    return OnCologyInferenceModel()
