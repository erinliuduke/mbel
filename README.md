# MBEL - Mini-books for Entertainment and Learning

This is a picture book generator app based on the OpenAI API [quickstart tutorial](https://beta.openai.com/docs/quickstart). It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. Follow the instructions below to set up.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.
   
   ```bash 
   git clone https://github.com/mbloom23/mbel-gpt-flask.git
   ```

3. Navigate into the project directory:

   ```bash
   cd mbel-gpt-flask
   ```

4. Create a new virtual environment:

   ```bash
   python -m venv venv
   . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

   ```bash
   export OPENAI_API_KEY='YOUR_API_KEY_HERE'
   ```

8. Run the app:

   ```bash
   flask run
   ```

You should now be able to access the app at the URL displayed in your terminal! Enter a topic or premise for your story in the box, press enter, and wait for the generation to load. Try describing different plot points, characters, or morals for your story.
