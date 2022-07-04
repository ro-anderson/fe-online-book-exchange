from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.library.helpers import *
from app.routers import twoforms, unsplash, accordion, login, signup, donate


app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

#app.include_router(unsplash.router)
#app.include_router(twoforms.router)
#app.include_router(accordion.router)
app.include_router(login.router)
app.include_router(signup.router)
app.include_router(donate.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)