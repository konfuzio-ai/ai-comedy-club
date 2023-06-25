# Tiziano's Oyster Sandwich Comedian

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
