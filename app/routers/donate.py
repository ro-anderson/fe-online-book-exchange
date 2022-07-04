from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/donate", response_class=HTMLResponse)
def get_donate(request: Request):

    #return templates.TemplateResponse('accordion.html', context={'request': request, 'result': result})
    return templates.TemplateResponse('donate.html', {"request": request})


@router.post("/donate", response_class=HTMLResponse)
def post_donate(request: Request, tag: str = Form(...)):

    return templates.TemplateResponse('donate.html', {"request": request})
    #return templates.TemplateResponse('login.html', context={'request': request, 'tag': tag})