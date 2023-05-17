from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config.enviroments import WEB_APP_ADDRESS


def create_app():
	app = FastAPI()
	app.middleware('http')

	app.add_middleware(
		CORSMiddleware,
		allow_origins=[WEB_APP_ADDRESS],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	return app


	