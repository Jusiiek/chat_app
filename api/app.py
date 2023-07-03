import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.app_middlewares import headers_middleware
from config.enviroments import WEB_APP_ADDRESS


def create_app():
	app = FastAPI()
	# app.add_event_handler("shutdown", close_connection)
	app.middleware('http')(headers_middleware)
	app.add_middleware(
		CORSMiddleware,
		allow_origins=[WEB_APP_ADDRESS],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	return app


app = create_app()


@app.on_event('startup')
def get_routes():
	from endpoints import (
		jwt,
		# users
	)

	app.include_router(jwt.router)
	# app.include_router(users.router)


def run_server():
	uvicorn.run(
		app="app:app",
		host="0.0.0.0",
		port=5000,
		reload=True,
	)


if __name__ == "__main__":
	run_server()
