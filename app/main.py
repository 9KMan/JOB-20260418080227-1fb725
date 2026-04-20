from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import schools, students, guardians, agents, scholarships, payments, webhooks

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Payment Integration + Sponsorship Platform API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schools.router)
app.include_router(students.router)
app.include_router(guardians.router)
app.include_router(agents.router)
app.include_router(scholarships.router)
app.include_router(payments.router)
app.include_router(webhooks.router)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)