from flask import Flask, request, jsonify
import openai
from register_file import get_text


# Set up your OpenAI API credentials
openai.api_key = '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'

app = Flask(__name__)


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


@app.route('/chatgpt/getresult/', methods=['POST'])
def chat():
    data = request.get_json()
    company_name = data.get('company_name', '')
    content = data.get('content', '')

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


@app.route('resume/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    get_text(file)
    #   나뉜 텍스트 DB 업로드 필요
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run()
