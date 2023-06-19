import gpt_2_simple as gpt2
import os

checkpoint_dir = os.path.join(os.getcwd(), "fine-tuning", "checkpoint")
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir, run_name="shortjokes")

text = gpt2.generate(sess, checkpoint_dir=checkpoint_dir, run_name="shortjokes", length=100, top_k=40, return_as_list=True)
print(text)


