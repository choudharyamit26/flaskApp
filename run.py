import os
from app import create_app

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "run:app", host="0.0.0.0", port=int(os.getenv("PORT", 5000)), reload=True
    )
