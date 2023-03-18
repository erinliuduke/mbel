import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# NOTE: MUST ADD YOUR API KEY AS AN ENV VARIABLE
openai.api_key = os.getenv("OPENAI_API_KEY")
sys_msg = "You are MBEL, an assistant that generates children\'s stories based on the user\'s input prompt. Stories should be less than 500 words and use simple vocabulary."
model = "gpt-3.5-turbo"


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
        return redirect(url_for("index", result=text))

    result = request.args.get("result")
    return render_template("index.html", result=result)