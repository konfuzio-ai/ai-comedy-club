import argparse
import transformers

parser = argparse.ArgumentParser()
parser.add_argument('--backend', default='torch', type=str, help="Backend to launch AI With (Available jax/torch)")
parser.add_argument('--bit8', action='store_true', help='Use and load model in 8BIT only for torch')
args = parser.parse_args()


def launch_jax():
    ...


def launch_torch():
    from .torch_serve import PyTorchServer, PytorchServerConfig
    from .utils import PRETRAINED_MODEL
    config = PytorchServerConfig(
        max_length=4096,
        max_new_tokens=1024,
        max_gpu_perc_to_use=0.95
    )

    server = PyTorchServer(config=config)
    load_kw = server.get_model_load_kwargs()
    if args.bit8:
        load_kw['load_in_8bit'] = True
    model = transformers.LlamaForCausalLM.from_pretrained(PRETRAINED_MODEL, **load_kw)
    tokenizer = transformers.LlamaTokenizerFast.from_pretrained(PRETRAINED_MODEL)

    server.model = model
    server.tokenizer = tokenizer

    server.create_gradio_ui_instruct().launch()


def main():
    assert args.backend in ['jax', 'torch'], 'Only Jax and Torch are supported as backends'
    if args.backend == 'jax':
        launch_jax()
    elif args.backend == 'torch':
        launch_torch()
    else:
        raise RuntimeError(f'Unknown Backend : {args.backend}')
