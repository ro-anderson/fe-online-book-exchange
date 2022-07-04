from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request):

    #return templates.TemplateResponse('accordion.html', context={'request': request, 'result': result})
    return templates.TemplateResponse('login.html', {"request": request})


@router.post("/login", response_class=HTMLResponse)
def post_login(request: Request, tag: str = Form(...)):

    return templates.TemplateResponse('login.html', {"request": request})
    #return templates.TemplateResponse('login.html', context={'request': request, 'tag': tag})
