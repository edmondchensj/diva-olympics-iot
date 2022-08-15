# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:35:21 2022

@author: User1
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 
from starlette.responses import HTMLResponse
class Light(BaseModel):
	gpio : int
	is_on : bool = False
	def init(self):
# 		GPIO.setup(self.gpio, GPIO.OUT)
		print("init")
		
		return self
	def on(self):
# 	        GPIO.output(self.gpio, GPIO.HIGH)
		print("on")
		self.is_on = True
		
	def off(self):
# 	        GPIO.output(self.gpio, GPIO.LOW)
		print("off")	
		self.is_on = False

light = Light(gpio=15).init()

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
            <title>Your Basic IOT Controller App</title>
        </head>
        <body>
            Lights are now turned : {state}
        <br>
<button onclick="location.href='/lights/on'" type="button">ON
</button>
<button onclick="location.href='/lights/off'" type="button">OFF
</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
	
if __name__ == "__main__":
 	run_server()