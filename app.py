from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openai

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Resume'
db = SQLAlchemy(app)

# Set up your OpenAI API credentials
openai.api_key = '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'

# Define your Resume model
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route('/resume/search_keyword', methods=['POST'])
def search_resume():
    data = request.get_json()
    keyword = data.get('keyword', '')

    resumes = Resume.query.filter(Resume.title.ilike(f'%{keyword}%')).all()

    resume_list = []
    for resume in resumes:
        resume_dict = {
            'id': resume.id,
            'title': resume.title,
            'content': resume.content
        }
        resume_list.append(resume_dict)

    return jsonify(resume_list)


@app.route('/all_resume', methods=['GET'])
def get_resume():
    resumes = Resume.query.all()
    resume_list = []
    for resume in resumes:
        resume_dict = {
            'id': resume.id,
            'title': resume.title,
            'content': resume.content
        }
        resume_list.append(resume_dict)
    return jsonify({'resumes': resume_list})        

# Define a function to interact with the ChatGPT model
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the ChatGPT model
        prompt=prompt,
        max_tokens=1000,  # Maximum length of the response
        temperature=0.7,  # Controls the randomness of the response
        n=1,  # Generate a single response
        stop=None,  # Stop generating after reaching a specific token (optional)
        timeout=10  # Maximum time in seconds to wait for the API response
    )
    return response.choices[0].text.strip()

@app.route('/chatgpt/getresult2/', methods=['POST']) #지원동기의 첫번째 검색 결과를 company_name에 맞게 바꿔주라.
def chat():
    data = request.get_json()
    keyword = '지원동기'

    resume = Resume.query.filter(Resume.title.ilike(f'%{keyword}%')).first()

    if resume is None:
        return jsonify({'response': 'No matching resume found'})

    company_name = data.get('company_name', '')
    content = resume.content

    texts = [
        f"아래 내용을 {company_name}의 인재상에 맞게 바꿔줘",
        content
    ]

    prompt = ""
    for i, text in enumerate(texts, start=1):
        prompt += f"[{text}]\n"
        prompt += f"Sample content {i}.\n"
        prompt += "\n"

    response = chat_with_gpt(prompt)
    return jsonify({'response': response})


# @app.route('/chatgpt/getresult/', methods=['POST'])
# def chat():
#     data = request.get_json()
#     company_name = data.get('company_name', '')
#     content = data.get('content', '')

#     texts = [
#         f"아래 내용을 {company_name}의 인재상에 맞게 바꿔줘",
#         content
#     ]

#     prompt = ""
#     for i, text in enumerate(texts, start=1):
#         prompt += f"[{text}]\n"
#         prompt += f"Sample content {i}.\n"
#         prompt += "\n"

#     response = chat_with_gpt(prompt)
#     return jsonify({'response': response})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
