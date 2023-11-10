# JokeMaster

## Used Model

the model that I used for JokeMaster is a self FineTuned Version of LLama Models

FineTuned Using [EasyDel](https://github.com/erfanzar/EasyDeL) on a TPU-4-8 Vm

The model can do any given task but for right now and for JokeMaster the model is only has been set up for this task

## Dataset

I have used my own customized UltraChat ... [Here](https://huggingface.co/datasets/erfanzar/UltraChat-Mixin)

## Run With JAX

```shell
python3 launch.py --backend='jax'
```

## Run With Torch

```shell
python3 launch.py --backend='torch'
```

use 8bit

```shell

python3 launch.py --backend='torch' --bit8
```
[Screencast from 2023-11-10 18-06-02.webm](https://github.com/erfanzar/ai-comedy-club/assets/59269023/317a8e8e-a7de-4896-85d0-5dcc5984fb91)
