
# Bobert

Final project for my AI class. Bobert is a simple intent-based chatbot using Python, the Natural Language Toolkit (NLTK), TFLearn, and Tensorflow.
## Features

- Chat with Bobert ("hello", "goodbye", etc)

  ![hi_bobert](https://github.com/justbautista/bobert-AI/assets/65434552/4d951d96-ae8a-49bb-b911-58c5f0abba5e)
- Ask Bobert to find a file, Bobert will return the file path

  ![find_file](https://github.com/justbautista/bobert-AI/assets/65434552/d38dd2a7-3c68-430a-b988-dfe374517f87)
- Bobert can tell you the weather in your area for today or tomorrow

  ![weather_today](https://github.com/justbautista/bobert-AI/assets/65434552/2f4843f1-5536-4810-b9ea-486b5bab2c3d)
- Bobert's misunderstanding your intent, correct him

  ![correcting bobert](https://github.com/justbautista/bobert-AI/assets/65434552/a5cd8c19-d1b7-4ed7-a82f-6446f1e90003)
  ![bobert remembered](https://github.com/justbautista/bobert-AI/assets/65434552/f1ebf3c2-cb42-454b-bd78-83d6514ca25d)




## Run Locally

Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

Generate API Key at [OpenWeatherMap](https://openweathermap.org/api) (optional if you don't want to use the weather function)

Clone the project

```bash
  git clone <this project>
```

Create environment

```bash
  conda env create --name <env> --file=environment.yml
```

Activate environment

```bash
  conda activate <env>
```

Go into bobert directory

```bash
  cd bobert
```

Create new .env file or rename .example-env and paste generated API key

```bash
  API_KEY=<Generated OpenWeatherMap API Key>
```

Train Bobert (make sure to train after correcting Bobert)

```bash
  python bobert.py --train
```

