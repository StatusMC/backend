"""Main application module."""
import fastapi
import uvicorn

import src.middlewares as middlewares
import src.routes as routes

app = fastapi.FastAPI()
middlewares.register_middlewares(app)
routes.register_all_routers(app)


if __name__ == "__main__":
    uvicorn.run(app)
