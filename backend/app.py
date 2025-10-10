# backend/app.py
from backend.database import init_app, db
from backend.models import User, Task 
from backend.routes.auth import auth_bp
from backend.routes.tasks import tasks_bp
from flask_cors import CORS

app = init_app()

# --- CORS con soporte para cookies
CORS(app, supports_credentials=True)

# --- Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tasks_bp, url_prefix='/api')

@app.route("/")
def home():
    return "To-Do Pro API funcionando. Versión actual: Octubre 2025"

if __name__ == "__main__":
    app.run(debug=False)
