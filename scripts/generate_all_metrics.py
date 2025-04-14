import itertools
from subprocess import PIPE, Popen
import os

current_env = os.environ.copy()
def execute_script(execute_cmd):

    with Popen(execute_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, env=current_env) as p:
        output, error = p.communicate()
        if p.returncode == 0:
            return output
        else:
            raise Exception(error)

# we are forcing the number of layers to be 2 to reduce the size of the model as we do not care about output, but just consistency between cpu and aiu
def execute_generate_metrics(model_id, max_new_tokens, batch_size, seq_length, default_dtype):
    execute_cmd = [
        'python3',
        "/tmp/aiu-fms-testing-utils/scripts/generate_metrics.py",
        "--architecture=hf_pretrained",
        f"--variant={model_id}",
        f"--tokenizer={model_id}",
        f"--max_new_tokens={max_new_tokens}",
        f"--min_pad_length={seq_length}",
        f"--batch_size={batch_size}",
        f"--default_dtype={default_dtype}",
        "--output_dir=/tmp/aiu-fms-testing-utils/output/",
        "--sharegpt_path=/mnt/aiu-models-en-shared/granite-20b-code-cobol-v1/sharegpt/share_gpt.json",
        "--num_test_tokens_per_sequence=1024",
    ]
    return execute_script(execute_cmd)

model_ids = ["/ibm-dmf/models/watsonx/shared/granite-20b-code-cobol-v1/20240603"]

max_new_tokens = [128]
batch_sizes = [1,8]
sequence_lengths = [64, 2048]
default_dtypes = ["fp16"]

tests = list(itertools.product(model_ids, max_new_tokens, batch_sizes, sequence_lengths, default_dtypes))

for model_id, max_new_token, batch_size, sequence_length, default_dtype in tests:
    print("testing ", "model_id-", model_id, ", max_new_tokens-", max_new_token, ", batch_size-",batch_size, ", seq_length-",sequence_length, ", default_dtype-", default_dtype)
    execute_generate_metrics(model_id, max_new_token, batch_size, sequence_length, default_dtype)