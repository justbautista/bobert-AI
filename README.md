
# Bobert

Final project for my AI class. Bobert is a simple intent-based chatbot using Python, the Natural Language Toolkit (NLTK), TFLearn, and Tensorflow.
## Features

- Chat with Bobert ("hello", "goodbye", etc)
- Ask Bobert to find a file, Bobert will return the file path
- Bobert can tell you the weather in your area for today or tomorrow
- Bobert's misunderstanding your intent, correct him




## Run Locally

Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

Generate API Key at [OpenWeatherMap](https://openweathermap.org/api) (optional if you don't want to use the weather function)

Clone the project

```bash
  git clone
```

Create environment

```bash
  conda env create --name <env> --file=environment.yml
```

Activate environment

```bash
  conda activate <env>
```

Create new .env file or rename .example.env and paste generated API key

```bash
  API_KEY=<Generated OpenWeatherMap API Key>
```

Train Bobert

```bash
  python bobert.py --train
```

