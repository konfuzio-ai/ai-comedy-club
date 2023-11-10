# these are my own libraries that I have developed ,so I don't think like there's a problem with using them :/

from EasyDel import JAXServer, FlaxLlamaForCausalLM, LlamaConfig
from EasyDel.transform.llama import llama_from_pretrained
from transformers import AutoTokenizer
from fjformer.load import get_float_dtype_by_name
import jax
import gradio as gr
from .utils import seafoam, JOKE_SYSTEM_PROMPT, SCALE_SYSTEM_PROMPT


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

    def create_gradio_ui_instruct(self):
        with gr.Blocks(
                theme=seafoam) as block:
            with gr.Row():
                pred = gr.TextArea(elem_id="EasyDel", label="EasyDel", container=True)

            with gr.Row():
                submit = gr.Button(variant="primary")
                stop = gr.Button(value='Stop ')
                clear = gr.Button(value='Clear Conversation')
                explain_joke = gr.Checkbox(value=True)
            with gr.Column():
                prompt = gr.Textbox(show_label=False, placeholder='Instruct Message', container=False)

            with gr.Row():
                with gr.Accordion('Advanced Options', open=False):
                    max_new_tokens = gr.Slider(value=self.config.max_new_tokens, maximum=10000,
                                               minimum=self.config.max_stream_tokens,
                                               label='Max New Tokens', step=self.config.max_stream_tokens, )

                    greedy = gr.Checkbox(value=False, label='Greedy Search')

            inputs = [prompt, explain_joke, max_new_tokens, greedy]
            sub_event = submit.click(fn=self.process_gradio_instruct, inputs=inputs, outputs=[prompt, pred], )

            def clear_():
                return ''

            clear.click(fn=clear_, outputs=[pred])
            txt_event = prompt.submit(fn=self.process_gradio_instruct, inputs=inputs, outputs=[prompt, pred])

            stop.click(fn=None, inputs=None, outputs=None, cancels=[txt_event, sub_event])

        block.queue()
        return block

    def process_gradio_instruct(self, instruction, explain, max_new_tokens, greedy):
        string = self.format_instruct(instruction=instruction,
                                      system=SCALE_SYSTEM_PROMPT if explain else JOKE_SYSTEM_PROMPT)
        if not self.config.stream_tokens_for_gradio:
            response = ''
            for response, _ in self.process(
                    string=string,
                    greedy=greedy,
                    max_new_tokens=max_new_tokens,
            ):
                pass

        else:
            response = ''
            for response, _ in self.process(
                    string=string,
                    greedy=greedy,
                    max_new_tokens=max_new_tokens,
                    stream=True
            ):
                yield '', response
        return '', response
