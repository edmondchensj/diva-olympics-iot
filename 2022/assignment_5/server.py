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
from fastapi import FastAPI
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
		grovepi.digitalWrite(LED,1)  
		print("on")
		self.is_on = True
		
	def off(self):
		grovepi.digitalWrite(LED,0)  
		print("off")	
		self.is_on = False






light_app = FastAPI()
@light_app.get("/", response_class=HTMLResponse)
async def root():
    return generate_html_response()


@light_app.get("/lights/on", response_class=HTMLResponse)
def on_light():
    light.on()
    return generate_html_response()

@light_app.get("/lights/off", response_class=HTMLResponse)
def off_light():
    light.off()
    return generate_html_response()



def run_server():
	uvicorn.run(light_app, host="0.0.0.0", port=8080)
	

def generate_html_response() -> HTMLResponse:
    state = "ON" if light.is_on else "OFF"
    html_content = f"""
    <html>
        <head>
            <title>{WEBSITE_TITLE}</title>
        </head>
        <body>
		<hr class="solid">		
			Welcome Message : {WELCOME_MESSAGE}		
        <br>
		<hr class="solid">		
        <br>
            System Message: Status of light is {state}
        <br>
        <br>
<button onclick="location.href='/lights/on'" type="button">ON
</button>
<button onclick="location.href='/lights/off'" type="button">OFF
</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
	

light = Light(LED=LED).init()

if __name__ == "__main__":
 	run_server()