from flask import Flask
from models import db, Resume

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Resume'  # Replace with your MySQL database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Example usage
with app.app_context():
    # Create a new resume entry
    new_resume = Resume(title='My Resume', content='Lorem ipsum dolor sit amet.')
    db.session.add(new_resume)
    db.session.commit()

    # Retrieve all resume entries
    resumes = Resume.query.all()
    for resume in resumes:
        print(resume.title, resume.content)
