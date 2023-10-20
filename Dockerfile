# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN [ "python", "-c", "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); \
    nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')" ]

COPY Docker-app/app.py app.py
COPY Docker-app/scripts scripts/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
