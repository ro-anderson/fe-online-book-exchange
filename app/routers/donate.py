from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import httpx

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/donate", response_class=HTMLResponse)
def get_donate(request: Request):

    #return templates.TemplateResponse('accordion.html', context={'request': request, 'result': result})
    return templates.TemplateResponse('donate.html', {"request": request, "success":None})

@router.post("/donate", response_class=HTMLResponse)
async def post_donate(request: Request, nome: str = Form(...), email: str = Form(...), titulo: str = Form(...)):
    user_data = {
        "name": nome,
        "email": email,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("http://0.0.0.0:5001/api/users", json=user_data)
        if response.status_code == 200:
            print(f"\nresponse: {response.json()}\n")
            user_id = response.json()["data"]["id"]
            donation_data = {
                "name": titulo,
                "category": "book",
                "user_information": {
                    "user_id": user_id
                },
            }
            response = await client.post("http://0.0.0.0:5001/api/donations", json=donation_data)
            success = response.status_code == 200
        else:
            success = False

    return templates.TemplateResponse('donate.html', {"request": request, "success": success})
