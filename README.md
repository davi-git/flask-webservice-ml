# RESTful Web Service to run Machine Learning Models
## Overview
This repository was born as an educative project during an internship.

The App creates a Flask webservice containing different endpoints that can be called through HTTP RESTful API requests.

The App can be used for two different tasks:

1. Apply Sentiment Analysis on a given text with three different models
2. Apply Named Entity Recognition (NER) on a given text with three different models

## Table of contents
- [Requirements and installation](#install)
- [How to use](#use)
    - [Sentiment Analysis](#sentiment)
    - [Named Entity Recognition](#ner)
- [Credits](#credits)
- [License](#license)

## <a name="install"></a>Requirements and installation
The App is ready to be containerized in *Docker* and to be used. You just need to create a *Docker image* (using **Dockerfile** in the root) and then create a *Docker container*.\
To be sure the application will work properly, some libraries need to be installed. The project contains a **requirements.txt** file that will be launched with **Dockerfile** and it will take care of the fulfilment of these requirements.\
The only requirement for the App to work properly and to be able to build a Docker image is to have **Python 3.8+** and **Docker** both installed on the machine from which the App is run.
To download them go to the [Python download page][1] and to the [Docker download page][2] and follow the instructions.

When you've installed **Python** and **Docker**, run the Docker service and, in order to prepare the application for the first use, follow the procedure below (about 10 GB of free space is required):

1. fork this repository
2. clone the forked repository
3. in a terminal navigate to the "**flask-webservice-ml**" folder of the cloned repository
4. type `docker build --tag docker-app .` (this will take a while)
5. type `docker run -d -p 5000:5000 docker-app`

At this point, if everything went well, a server should have been started on local machine and now you can start issuing http requests to it.\
If you want to verify if it's running, head over to http://localhost:5000 and you should see the message ***"The application is running!"***.

## <a name="use"></a>How to use
The application can be used while the Flask server is running (see [below](#start-server) the command to start the server).

The following are the endpoints with their respective goals:

Endpoint | Purpose
--- | ---
sentiment/vader | Apply Vader Model for Sentiment Analysis on a given text
sentiment/textblob | Apply TextBlob Model for Sentiment Analysis on a given text
sentiment/flair | Apply Flair Model for Sentiment Analysis on a given text
ner/spacy | Apply SpaCy Model for Named Entity Recognition on a given text
ner/nltk | Apply NLTK Model for Named Entity Recognition on a given text
ner/flair | Apply Flair Model for Named Entity Recognition on a given text

We'll see how to use it for each task in a minute! But first let's see how you start the server every time you want to use the App and stop it when you don't need it.

To start the Flask server you can simply start the Docker container from a terminal. Below you can find the only three simple Docker commands you should know to start and stop the container:

<a name="start-server"></a>
- `docker ps` --> show a list of currently running containers (with `-a` option you will see all the containers, not just those running)
- `docker start <container_id>` --> run the container with specified ID (you can find the ID in the list of containers)
- `docker stop <container_id>` --> stop the container with specified ID

For a more exhaustive list of commands and a more extensive use of Docker refer to the [Docker official guide][3].

And now let's see the App functionalities!

***
### <a name="sentiment"></a>How to apply Sentiment Analysis to text
The Sentiment Analysis endpoints return a response - given a text and, optionally, the thresholds to apply to the classifier - with the sentiment of the text as either "*positive*", "*negative*" or "*neutral*" and the relative score calculated by the algorithm.\
The endpoints accept both **GET** and **POST** methods. The input of **POST** method needs to be in *JSON* format.

The following are the ***input*** parameters accepted from each model and the default values of optional ones:

Parameter | Description | Vader | TextBlob | Flair
--- | --- |:---:|:---:|:---:
**text** | Text to analyze | x | x | x
**pos_threshold** | Threshold used to classify positive cases (set as '*positive*' all cases where score is upper than '**pos_threshold**') | 0.3 | 0.2
**neg_threshold** | Threshold used to classify negative cases (set as '*negative*' all cases where score is lower than '**neg_threshold**') | -0.3 | -0.1
**threshold** | Threshold used to classify neutral cases (set as '*neutral*' all cases where score is lower than '**threshold**') |   |   | 0.65

Below are some examples of valid input for each model with both GET and POST methods:

Model | POST | GET
--- | --- | ---
Vader | `{"text": "This product is good!", "pos_threshold": 0.5, "neg_threshold": -0.4}` | `http://localhost:5000/sentiment/vader?text=This%20product%20is%20good!&pos_threshold=0.5&neg_threshold=-0.4`
TextBlob | `{"text": "This product is good!", "neg_threshold": -0.2}` | `http://localhost:5000/sentiment/textblob?text=This%20product%20is%20good!&neg_threshold=-0.2`
Flair | `{"text": "This product is good!", "threshold": 0.7}` | `http://localhost:5000/sentiment/flair?text=This%20product%20is%20good!&threshold=0.7`

The ***output*** will be returned in *JSON* format and will contain the information below:

- a string representing the sentiment of the text as either "*positive*", "*negative*" or "*neutral*";
- a score:
    - in Vader and TextBlob models the score ranges from -1 (most negative) to 1 (most positive)
    - in Flair model the score ranges from 0 to 1 (the higher the score the higher the strength of the sentiment the Model extracted)

> [!NOTE]
> Flair looks for the model on local server and if it wasn't find it will be installed. In this case it will take a while. Anyway, Flair execution is in general slower than other Sentiment Analysis models.
***
### <a name="ner"></a>How to apply Named Entity Recognition to text
The NER endpoints return a response - given a text and, optionally, the labels to consider - with the entities (such as persons, organizations, locations, etc.) found in the text by the algorithm.\
The endpoint accepts both **GET** and **POST** methods. The input of **POST** method needs to be in *JSON* format.

The following are the ***input*** parameters accepted:

Parameter | Description | Default
--- | --- |:---:
**text** | Text to analyze
**labels** *[Optional]* | List of labels being filtered by the function | '*None*' (return all the labels generated by the Model)

This is an example of valid input 

- with POST method:
```JSON
{
    "text": "Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist. He is currently the chairman and CEO of Berkshire Hathaway",
    "labels": [
        "ORG",
        "PERSON"
    ]
}
```

- with GET method:

    `http://localhost:5000/ner/nltk?text=Warren%20Edward%20Buffett%20(born%20August%2030,%201930)%20is%20an%20American%20business%20magnate,%20investor,%20and%20philanthropist.%20He%20is%20currently%20the%20chairman%20and%20CEO%20of%20Berkshire%20Hathaway&labels=ORG,PERSON`

The ***output*** will be a dictionary of lists, where:

- *keys* are the labels generated by the Model (eventually filtered on labels specified in '**labels**' parameter);
- *values* are the lists of entities the Model found in the text to which it assigned a label.

> [!NOTE]
> Flair looks for the model on local server and if it wasn't find it will be installed. In this case it will take a while. Anyway, Flair execution is in general slower than other NER models.
***
### <a name="credits"></a>Credits
I want to thank my colleagues, Tundra Parisi and Carlson Kouebe, our mentor Ricardo Matamoros and Social Thingum Srl for making this project possible and giving me the opportunity to learn so much from this work.
***
### <a name="license"></a>License
This project is licensed under the terms of the [MIT license](LICENSE)

[1]: https://www.python.org/downloads/
[2]: https://docs.docker.com/engine/install/
[3]: https://docs.docker.com/engine/reference/commandline/cli/
