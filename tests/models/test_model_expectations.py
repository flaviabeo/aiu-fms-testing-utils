from fms.models import get_model
import pytest
import torch

from fms.testing._internal.model_test_suite import (
    ModelConsistencyTestSuite,
    ModelFixtureMixin,
)
import os

model_dir = os.environ.get("FMS_TESTING_MODEL_DIR", "/mnt/aiu-models-en-shared/models")
# FMS_TESTING_MODEL_DIR=/mnt/aiu-models-en-shared/models
LLAMA_194M = f"{model_dir}/llama-194m"
GRANITE_7B_BASE = f"{model_dir}/granite-7b-base"
GRANITE_8B_CODE_BASE = f"{model_dir}/granite-8b-code-base"
GRANITE_3_8B_CODE_BASE = f"{model_dir}/granite-3-8b-base"
GRANITE_COBOL_20B = "/ibm-dmf/models/watsonx/shared/granite-20b-code-cobol-v1/20240603"

models = [LLAMA_194M, GRANITE_7B_BASE, GRANITE_8B_CODE_BASE, GRANITE_3_8B_CODE_BASE, GRANITE_COBOL_20B]

class AIUModelFixtureMixin(ModelFixtureMixin):

    @pytest.fixture(scope="class", autouse=True)
    def uninitialized_model(self, model_id):
        aiu_model = get_model(
            "hf_configured",
            model_id,
            device_type="cpu",
            unfuse_weights=True,
            nlayers=3
        )
        torch.compile(aiu_model, backend="sendnn")
        return aiu_model
    
    @pytest.fixture(scope="class", autouse=True, params=models)
    def model_id(self, request):
        return request.param

class TestAIUModels(
    ModelConsistencyTestSuite,
    AIUModelFixtureMixin,
):

    # x is the main parameter for this model which is the input tensor
    _get_signature_params = ["x"]

    def test_model_unfused(self, model, signature):
        pytest.skip("All AIU models are already unfused")