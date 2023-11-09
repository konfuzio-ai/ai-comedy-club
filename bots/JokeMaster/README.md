# JokeMaster

## Used Model

the model that I used for JokeMaster is a self FineTuned Version of OpenLlama Models

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