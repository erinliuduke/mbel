import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# NOTE: MUST ADD YOUR API KEY AS AN ENV VARIABLE
openai.api_key = os.getenv("OPENAI_API_KEY")
sys_msg = "You are MBEL, an assistant that generates children\'s stories based on the user\'s input prompt. Stories should be less than 500 words and use simple vocabulary."
model = "gpt-3.5-turbo"
size = '256x256'


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        story = request.form["story"]
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": story}
            ]
        )
        text = response['choices'][0]['message']['content']

        sentences = text.split('.')
        num_chunks = 4
        chunk_size = len(sentences) // num_chunks
        chunks = [sentences[i:i+chunk_size] for i in range(0, len(sentences), chunk_size)]
        
        text_chunks = []
        image_urls = []
        for chunk in chunks:
            image_prompt = '.'.join(chunk)+'.'
            response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size='256x256'
            )
            url = response['data'][0]['url']
            text_chunks.append(image_prompt)
            image_urls.append(url)

        return render_template("index.html", result=text_chunks, image_urls=image_urls)

    result = request.args.get("result")
    return render_template("index.html", result=result)