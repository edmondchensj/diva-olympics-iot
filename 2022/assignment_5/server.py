# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:35:21 2022

@author: User1
"""
try:
	import grovepi
except:
	pass
##1. IMPORT RELEVANT PARAMETERS
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn 
from starlette.responses import HTMLResponse

##TO DO: CUSTOMIZE YOUR WEB PAGE 
LED = 4
WEBSITE_TITLE = 'Your Basic IOT Controller App BY _____' # CHANGE TITLE HERE
WELCOME_MESSAGE = 'Hello! Welcome to your very first created website , to start , you can ...' # CHANGE STRING


class Light(BaseModel):
    LED : int
    is_on : bool = False

    def init(self):
        try:
            grovepi.digitalWrite(LED,0)     # Send LOW to switch off LED
        except: 
            pass
        print("initialized")
        
        return self
    def on(self):
        try: 
            grovepi.digitalWrite(LED,1)  
        except:
            pass
        print("on")
        self.is_on = True

    def off(self):
        try: 
            grovepi.digitalWrite(LED,0)  
        except:
            pass

        print("off")	
        self.is_on = False

light = Light(LED=LED).init()

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return generate_html_response(request)

@app.get("/lights/on", response_class=HTMLResponse)
def on_light(request: Request):
    light.on()
    return generate_html_response(request)

@app.get("/lights/off", response_class=HTMLResponse)
def off_light(request: Request):
    light.off()
    return generate_html_response(request)
    
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

def generate_html_response(request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "light": light,
            "website_title": WEBSITE_TITLE,
            "welcome_message": WELCOME_MESSAGE,
            "status": "ON" if light.is_on else "OFF"
            }
    )

if __name__ == "__main__":
 	run_server()