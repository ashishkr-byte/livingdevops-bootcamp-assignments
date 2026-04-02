from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    profile = {
        "name": "Ashish Kumar",
        "title": "Cloud & DevOps Engineer",
        "summary": "I build and automate reliable cloud infrastructure with AWS, CI/CD, and container tooling.",
        "skills": ["AWS", "Terraform", "Docker", "Kubernetes", "Jenkins", "GitHub Actions"],
        "projects": [
            {
                "name": "AWS 3-Tier Deployment",
                "description": "Designed and deployed a scalable 3-tier architecture on AWS using IaC.",
            },
            {
                "name": "CI/CD Pipeline Automation",
                "description": "Built end-to-end CI/CD pipelines with quality checks and automated deployments.",
            },
            {
                "name": "Kubernetes Monitoring Stack",
                "description": "Implemented Prometheus and Grafana dashboards for production observability.",
            },
        ],
    }
    return render_template("index.html", profile=profile)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
