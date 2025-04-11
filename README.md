<h1>📝 Blog API</h1>

<p>A simple yet functional **Blog API** built using **FastAPI**, **SQLAlchemy**, **JWT Authentication**, and **SQLite**.</p>
<break>

<h2>🚀 Features</h2>
<ul>
    <li>✅ User Registration</li>
    <li>✅ Secure Login with JWT Tokens</li>
    <li>✅ Create, View, and Delete Blog Posts</li>
    <li>✅ Comment on Posts</li>
    <li>✅ Delete Own Comments</li>
    <li>✅ Full Authentication Flow using OAuth2 and JWT</li>
    <li>✅ Pydantic-powered input validation</li>
    <li>✅ SQLite for local development</li>
</ul>

<h2>🏗️ Tech Stack</h2>
<ul>
    <li>**[FastAPI](https://fastapi.tiangolo.com/)** – High-performance Python web framework</li>
    <li>**SQLAlchemy** – ORM for database interaction</li>
    <li>**SQLite** – Lightweight database for development</li>
    <li>**JWT** – Token-based authentication</li>
    <li>**Passlib** – Secure password hashing</li>
    <li>**Pydantic** – Input validation</li>
    <li>**Uvicorn** – ASGI server for running FastAPI</li>
    <li>**python-multipart** – Required for handling form data</li>
</ul>

<h2>📂 Project Structure</h2>
<p>. ├── db_setup.py # Database models and session setup ├── routes.py # Main FastAPI application and API routes ├── main.py # Optional interactive CLI ├── blog.db # SQLite DB file (auto-generated) ├── README.md # This file</p>

<h2>🛠️ Installation</h2>

<p>1. Clone the repo</p>

<p>```bash
git clone https://github.com/Modeste74/blog-api.git
cd blog-api</p>

<h3>Setting up the environment</h3>

python3 -m venv name_of_env
source venv/bin/activate  # On Linux: name_of_venv/bin/activate

<h3>Install dependencies</h3>
pip install -r requirements.txt

<h3># Running the App</h3>
Start the FastAPI server using Uvicorn:
uvicorn routes:app --reload

<h3>## Optional: Interactive CLI for Local Testing</h3>
<p>Instead of Postman, you can use the terminal-based `main.py` CLI:</p>
<p><strong>`python3 main.py`</strong></p>

<p>You can:</p>
<ul>
    <li>Register and login users</li>
    <li>Create and delete posts</li>
    <li>View all posts and comments</li>
    <li>Add comments</li>
</ul>

<h3>🔐 Authentication Workflow</h3>
<p>Use /register to create an account.</p>

<p>Use /login to get a JWT token.</p>

<P>Use that token in the Authorization header like:</p>
<break>
<p>Authorization: Bearer <your-token></p>

<h3>📌 Future Improvements</h3>
<ul>
    <li>✅ Add update routes for posts/comments</li>
    <li>✅ Add pagination</li>
    <li>✅ Add like/bookmark system</li>
    <li>✅ Dockerize the project</li>
    <li>✅ Deploy to Railway/Render/Heroku</li>
</ul>

<h2>🧑‍💻 Author</h2>
<p>Modeste Ciira</p>
<p><strong>Backend Developer | Python & FastAPI Enthusiast</strong></p>

<a href="https://github.com/Modeste74">GitHub: Modeste74</a>
