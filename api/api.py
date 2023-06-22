import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Kaustubh Demo",
                                                     "placeholder": "This is the demo for using FastAPI with Jinja "
                                                                     "templates"})


if __name__ == "__main__":
    uvicorn.run("api:app", host='127.1.1.1', port=8001, reload=True)

