from fastapi import FastAPI
from .database import engine
from .routers import post,user,auth,vote
from . import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app=FastAPI()

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/",response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>InteractHub API</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: #f1f5f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }

            .container {
                background: rgba(30, 41, 59, 0.6);
                padding: 50px;
                border-radius: 16px;
                backdrop-filter: blur(12px);
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                max-width: 700px;
            }

            h1 {
                font-size: 3rem;
                margin-bottom: 15px;
            }

            p {
                font-size: 1.2rem;
                color: #cbd5e1;
                margin-bottom: 30px;
                background: linear-gradient(90deg, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .links a {
                display: inline-block;
                margin: 10px;
                padding: 12px 22px;
                background: linear-gradient(90deg, #38bdf8, #6366f1);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .links a:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
            }

            .footer {
                margin-top: 40px;
                font-size: 0.9rem;
                color: #94a3b8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 InteractHub API</h1>
            <p>Production-style RESTful backend built with FastAPI & PostgreSQL.</p>

            <div class="links">
                <a href="/docs">Swagger Docs</a>
                <a href="/redoc">ReDoc</a>
            </div>

            <div class="footer">
                "Stay hungry, Stay foolish."
                <br>
                ~ Steve Jobs
            </div>
        </div>
    </body>
    </html>
    """
