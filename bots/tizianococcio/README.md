# Tiziano's Oyster Sandwich Comedian

**IMPORTANT**: the models I trained are too large to fit onto a GitHub repository. Also using git-lfs does not work, since I'm working on a fork of a repository I don't own.

Please download the desired models and place in the paths `tizianococcio/models/merge-v2` and `tizianococcio/models/merge-v3` respectively. The models can be downloaded from here:
- [merge-v2](https://drive.google.com/drive/folders/1-OFE6e4Ovw4r6dD26qMzUex1bQ0jmh8v?usp=sharing)
- [merge-v3](https://drive.google.com/drive/folders/1_R_haV4shSJcJFk9KfJUBvsbzxAnQLbY?usp=sharing)

In `config.yaml` one can set the name of the generative language model to use. The available models are:
- `merge-v2`: this is trained without conditional generation on mood and joke style, default.
- `merge-v3`: this is trained by prompting the GPT model with a mood and a joke style, it has poorer performance than `merge-v2`.

Also note that different `Presenters` can be used for the user interface. Currently, the following are available:
- `NaivePresenter`: keeps asking the user for a joke style and mood and generates a joke accordingly
- `NarcissusPresenter`: simply generates jokes, with no style or mood prompting, at 5 second intervals.

To start the "interactive mode", `launch_stage()` from the `Bot` class must be called. More ideas for interactivity are included in the PDF report.

Other things to note:
- To rate jokes, `rate_joke()` must be called explicitly.
- See the PDF report for details on the process.
