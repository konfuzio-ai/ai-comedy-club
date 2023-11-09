# these are my own libraries that I have developed ,so I don't think like there's a problem with using them :/

from EasyDel import JAXServer, FlaxLlamaForCausalLM, LlamaConfig
from EasyDel.transform.llama import llama_from_pretrained
from transformers import AutoTokenizer
from fjformer.load import get_float_dtype_by_name
import jax


class JokeMasterJaxServe(JAXServer):
    @classmethod
    def load_from_torch(cls, repo_id, config=None):
        with jax.default_device(jax.devices('cpu')[0]):
            param, config_model = llama_from_pretrained(
                repo_id
            )

        tokenizer = AutoTokenizer.from_pretrained(repo_id)
        model = FlaxLlamaForCausalLM(
            config=config_model,
            dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
            param_dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
            precision=jax.lax.Precision('fastest'),
            _do_init=False
        )
        return cls.load_from_params(
            config_model=config_model,
            model=model,
            config=config,
            params=param,
            tokenizer=tokenizer,
            add_params_field=True,
            do_memory_log=False
        )

    @classmethod
    def load_from_jax(cls, repo_id, checkpoint_path, config_repo=None, config=None):
        from huggingface_hub import hf_hub_download
        path = hf_hub_download(repo_id, checkpoint_path)
        tokenizer = AutoTokenizer.from_pretrained(repo_id)
        config_model = LlamaConfig.from_pretrained(config_repo or repo_id)
        model = FlaxLlamaForCausalLM(
            config=config_model,
            dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
            param_dtype=get_float_dtype_by_name(config['dtype'] if config is not None else 'fp16'),
            precision=jax.lax.Precision('fastest'),
            _do_init=False
        )
        return cls.load(
            path=path,
            config_model=config_model,
            model=model,
            config=config,
            tokenizer=tokenizer,
            add_params_field=True,
            do_memory_log=False
        )

    @classmethod
    def run(cls, repo_id, config=None):
        server = cls.load_from_torch(
            repo_id=repo_id,
            config=config)
        return server
