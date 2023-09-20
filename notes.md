# Additional readme (delete before merge)
## New features
- In bots/gpt2tuned you can find fine-tuning folder which contains all the instruments to learn tuned gpt2 model (on labeled shortjokes.csv dataset)
- In api/ folder there is a small backend (FastAPI) + Jinja2 template, after run of api.py the generated jokes will be displayed
- Jokes can be evaluated by classifiers and length criteria
## Problems 
- Fine-tuning requires a lot of resources (GPU+memory), so I've used our university JupyterHub. Guess it is better to deploy it on AWS or hugging-face
- I can show how modified model generate the jokes on our JupyterHub (they look pretty logical but still offensive)
- Some classifier parameters must be changed (need more time to play with them)
- THERE IS NO OFFENSIVE FILTER. Unfortunately,I didn't add anyone but found suitable solution - https://developers.perspectiveapi.com/

## Things to do
- Due to PEP, it is better to use .toml files for builds - https://peps.python.org/pep-0518/
- Solve all the problems
- Classify jokes using NLP methods
- Expand web interface
- Maybe containerization. Docker-compose with ML part + Web

### 

