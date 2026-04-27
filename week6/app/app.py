from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_LINK")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


def calculate_domain_mix(users):
    domains = []
    for user in users:
        if "@" in user.email:
            domains.append(user.email.split("@", 1)[1].lower())
    counts = Counter(domains)
    total = sum(counts.values())

    top = []
    for domain, count in counts.most_common(4):
        share = round((count / total) * 100) if total else 0
        top.append({"domain": domain, "count": count, "share": share})
    return top


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = User(name=request.form['name'], email=request.form['email'])
        db.session.add(user)
        db.session.commit()
        return redirect('/')

    users = User.query.order_by(User.id.asc()).all()
    total_users = len(users)

    top_domains = calculate_domain_mix(users)
    adoption_score = min(100, 38 + total_users * 6)

    stats = {
        "total_users": total_users,
        "latest_user": users[-1].name if users else "No registrations yet",
        "adoption_score": adoption_score,
        "power_domain": top_domains[0]["domain"] if top_domains else "Not enough data",
    }

    highlights = [
        {
            "title": "Network-ready onboarding",
            "description": "Registrations are fast, clear, and visually guided so first-time visitors complete sign-up quickly.",
        },
        {
            "title": "Pulse analytics",
            "description": "Live counters and domain trends make traction visible to admins, sponsors, and community partners.",
        },
        {
            "title": "Share loops",
            "description": "A built-in referral prompt helps members invite peers, turning your landing page into a growth channel.",
        },
    ]

    resources = [
        {"label": "Register", "href": "#register"},
        {"label": "Pulse", "href": "#pulse"},
        {"label": "Members", "href": "#members"},
        {"label": "Idea Lab", "href": "#idea-lab"},
    ]

    community_tracks = [
        {
            "title": "Career Sprint Pods",
            "badge": "High adoption",
            "description": "Create 2-week peer accountability pods for job prep and interviews.",
        },
        {
            "title": "Local Meet Match",
            "badge": "New",
            "description": "Automatically suggest nearby meetups based on member interests and availability.",
        },
        {
            "title": "Mentor Office Hours",
            "badge": "Sticky",
            "description": "Open weekly micro-sessions where seniors unblock learners in 15-minute slots.",
        },
    ]

    launch_playbook = [
        "Host one monthly themed challenge to attract repeat visitors.",
        "Publish member milestones every Friday to keep social proof visible.",
        "Use referral snippets to invite classmates and teammates in one click.",
    ]

    return render_template(
        'index.html',
        users=users,
        stats=stats,
        highlights=highlights,
        resources=resources,
        top_domains=top_domains,
        community_tracks=community_tracks,
        launch_playbook=launch_playbook,
    )


with app.app_context():
    db.create_all()
    print("Database tables created")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
