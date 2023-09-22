import gradio as gr
import subprocess
import sys
from pathlib import Path

from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("PY007/TinyLlama-1.1B-intermediate-step-240k-503B")
tokenizer = AutoTokenizer.from_pretrained("PY007/TinyLlama-1.1B-Chat-v0.2")
async def generate(prompt, model_name, seed=0, temperature=0.5, num_tokens=256):
    # stream stout
    prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    out = tokenizer.encode(prompt)[1:]
    out_str = ' '.join(map(str, out))
    process = subprocess.Popen(
        [
            "mojo",
            "llama2.mojo",
            Path(model_name),
            "-s",
            str(seed),
            "-n",
            str(num_tokens),
            "-t",
            str(temperature),
            "-id",
            out_str,
            "-tk",
            "../llama2.c/tok_tl-chat.bin"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    text = ""
    for char in iter(lambda: process.stdout.read(1), b""):
        char_decoded = char.decode("utf-8", errors="ignore")
        text += char_decoded
        yield text


with gr.Blocks() as demo:
    gr.Markdown(
        """
# llama2.🔥
## [Mojo](https://docs.modular.com/mojo/) implementation of [llama2.c](https://github.com/karpathy/llama2.c) by [@tairov](https://github.com/tairov)
Source: https://github.com/tairov/llama2.mojo
    """
    )
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt", placeholder="Add your prompt here...")
            seed = gr.Slider(
                minimum=0,
                maximum=2**53,
                value=0,
                step=1,
                label="Seed",
                randomize=True,
            )
            temperature = gr.Slider(
                minimum=0.0, maximum=2.0, step=0.01, value=0.5, label="Temperature"
            )
            num_tokens = gr.Slider(
                minimum=1, maximum=256, value=256, label="Number of tokens"
            )
            model_name = gr.Dropdown(
                ["stories15M.bin", "stories42M.bin", "stories110M.bin", "../llama2.c/tl-chat.bin", "../llama2.c/tl.bin"],
                value="../llama2.c/tl-chat.bin",
                label="Model Size",
            )
            with gr.Row():
                stop = gr.Button("Stop")
                run = gr.Button("Run")
        with gr.Column(scale=2):
            output_text = gr.Textbox(label="Generated Text")

    # update maximum number of tokens based on model size
    model_name.change(
        lambda x: gr.update(maximum=1024)
        if x == "stories110M.bin" or x == "stories42M.bin"
        else gr.update(maximum=256),
        model_name,
        num_tokens,
        queue=False,
    )
    click_event = run.click(
        fn=generate,
        inputs=[prompt, model_name, seed, temperature, num_tokens],
        outputs=output_text,
    )
    stop.click(fn=None, inputs=None, outputs=None, cancels=[click_event])

demo.queue()
demo.launch(server_name="0.0.0.0")
