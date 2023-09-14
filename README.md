
# Bobert

Final project for my AI class. Bobert is a simple intent-based chatbot using Python, the Natural Language Toolkit (NLTK), TFLearn, and Tensorflow.
## Features

- Chat with Bobert ("hello", "goodbye", etc)

  ![hi_bobert](https://github.com/justbautista/bobert-AI/assets/65434552/a5c66be1-b899-4b0b-8ecb-610255d75d5c)
- Ask Bobert to find a file, Bobert will return the file path

  ![find_file](https://github.com/justbautista/bobert-AI/assets/65434552/3eb2efd7-c6f2-49e7-8e32-bbf396350dd4)
- Bobert can tell you the weather in your area for today or tomorrow

  ![weather_today](https://github.com/justbautista/bobert-AI/assets/65434552/b16a2e7f-d79b-4b28-981f-219c81bbbff8)
- Bobert's misunderstanding your intent, correct him

  ![correcting bobert](https://github.com/justbautista/bobert-AI/assets/65434552/38ab476e-ec8e-4c96-b80a-7d3aa66dc3d5)
  
  ![bobert corrected himself](https://github.com/justbautista/bobert-AI/assets/65434552/b9a2ba3b-045f-4f68-bb75-138b128a782d)



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

