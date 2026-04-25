from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


# Use environment variables with sensible defaults

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_LINK")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

# the above is not a good practice, harcoding everything in one string is bad, not secure


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = User(name=request.form['name'], email=request.form['email'])
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    users = User.query.all()
    stats = {
        "total_users": len(users),
        "latest_user": users[-1].name if users else "No registrations yet",
    }
    highlights = [
        {
            "title": "Fast onboarding",
            "description": "Collect new registrations with a simple, direct form that works well on desktop and mobile.",
        },
        {
            "title": "Clean data view",
            "description": "Keep recent signups visible in one place so the app feels useful immediately after submission.",
        },
        {
            "title": "Deployment ready",
            "description": "Built on Flask and SQLAlchemy, which fits naturally into your existing Docker-based setup.",
        },
    ]
    resources = [
        {"label": "Registration", "href": "#register"},
        {"label": "Community", "href": "#community"},
        {"label": "Members", "href": "#members"},
        {"label": "Docs", "href": "https://flask.palletsprojects.com/"},
    ]
    return render_template(
        'index.html',
        users=users,
        stats=stats,
        highlights=highlights,
        resources=resources,
    )

# Create tables before first request
with app.app_context():
    db.create_all()
    print("✓ Database tables created")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # True means Flask will run in development mode. For ECS, that should normally be debug=False, or better, you should use gunicorn and avoid relying on app.run() for production at all

""" debug=True turns on Flask debug mode.

In practice, it does a few things:

- Auto-reloads the app when code changes
- Shows detailed error pages in the browser
- Exposes traceback and internal app details for easier development

Why it is useful:

- Faster local development
- Easier debugging when something breaks

Why it is bad for production:

- Error pages can reveal sensitive internal details
- It is not meant for secure public deployment
- It can behave unpredictably compared to a production server setup """