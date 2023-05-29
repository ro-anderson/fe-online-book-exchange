from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import httpx
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

# Get the base URL from environment variable or use a default value
BASE_URL = os.environ.get('BASE_URL', 'http://0.0.0.0:5001')

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
        response = await client.post(f"{BASE_URL}/api/users", json=user_data)
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
            response = await client.post("{BASE_URL}/api/donations", json=donation_data)
            success = response.status_code == 200
        else:
            success = False

    return templates.TemplateResponse('donate.html', {"request": request, "success": success})
