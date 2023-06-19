import gpt_2_simple as gpt2
from datetime import datetime
import os

gpt2.download_gpt2(model_name="355M")
os.chdir("fine-tuning")
file_name = "data.txt"
run_name = "shortjokes"
model_size = '355M'

sess = gpt2.start_tf_sess()

gpt2.finetune(sess,
              dataset=file_name,
              model_name=model_size,
              steps=200,
              restore_from='fresh',
              run_name = run_name,
              print_every=10,
              sample_every=50,
              save_every=50)
             # , learning_rate=.00003)


print(run_name)
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name=run_name)


gpt2.generate(sess, run_name=run_name, temperature=.7, length=100, prefix=None, top_k=40, nsamples=10)

