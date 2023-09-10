"""Main application module."""
import fastapi
import uvicorn

import src.routes as routes

app = fastapi.FastAPI()
routes.register_all_routers(app)


if __name__ == "__main__":
    uvicorn.run(app)
