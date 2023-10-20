from flask import Flask, request, jsonify
from scripts.sentiment_analysis import SA
from scripts.ner import NER


# Create app
app = Flask(__name__)


# Start page
@app.route('/')
def hello():
    return '<h1>The application is running!</h1>'


# Handle GET and POST request parameters saving them as SA object properties
def sa(request, obj_SA: SA) -> None:
    # Parameters visible in url
    if request.method == "GET":
        # Save parameters in object properties
        obj_SA.text = request.args.get("text")
        obj_SA.pos_threshold = request.args.get("pos_threshold")
        obj_SA.neg_threshold = request.args.get("neg_threshold")
        obj_SA.threshold = request.args.get("threshold")
    # Request source type: JSON
    elif request.method == "POST":
        # Load parameters in json format and save them in object properties
        data = request.get_json()
        obj_SA.text = data["text"]
        if "pos_threshold" in data:
            obj_SA.pos_threshold = data["pos_threshold"]
        if "neg_threshold" in data:
            obj_SA.neg_threshold = data["neg_threshold"]
        if "threshold" in data:
            obj_SA.threshold = data["threshold"]


# Handle GET and POST request parameters saving them as NER object properties
def ner(request, obj_NER: NER) -> None:
    # Parameters visible in url
    if request.method == "GET":
        # Save parameters in object properties
        obj_NER.text = request.args.get("text")
        obj_NER.tags = request.args.get("labels")
        if obj_NER.tags is not None:
            obj_NER.tags = obj_NER.tags.split(",")
    # Request source type: JSON
    elif request.method == "POST":
        # Load parameters in json format and save them in object properties
        data = request.get_json()
        obj_NER.text = data["text"]
        if "labels" in data:
            obj_NER.tags = data["labels"]


# For all Sentiment Analysis models the arguments will be converted to dictionary to resolve problem where
# thresholds are not specified, and calling, for example, "obj_SA.vader(text, pos_threshold, neg_threshold)"
# would be like calling "obj_SA.vader(text, None, None)", that is different to calling "obj_SA.vader(text)"
# because it doesn't take into consideration default values of thresholds.
#
# Pass the arguments as keyword arguments from a dictionary using argument unpacking.
# Keyword arguments are passed as a dict using the ** operator.
# Filter out the arguments with None as their value using dictionary comprehensions.
#
# Source: https://stackoverflow.com/questions/52494128/call-function-without-optional-arguments-if-they-are-none
# Argument unpacking: https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
# Dictionary comprehensions: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions


# Sentiment Analysis with Vader model
# Decorator: route definition to /sentiment/vader address
@app.route("/sentiment/vader", methods=["GET", "POST"])
# Connect sa_vader() function to route
def sa_vader():
    # Create SA object and assign request attributes to object properties
    obj_SA = SA()
    sa(request, obj_SA)
    # Save properties values in a dictionary
    kwargs = dict(
        text=obj_SA.text,
        pos_threshold=obj_SA.pos_threshold,
        neg_threshold=obj_SA.neg_threshold,
    )
    # Run model (filter out the arguments with None as their value)
    retvalue = obj_SA.vader(**{k: v for k, v in kwargs.items() if v is not None})
    # Return results in json format
    return jsonify(retvalue)


# Sentiment Analysis with TextBlob model
# Decorator: route definition to /sentiment/textblob address
@app.route("/sentiment/textblob", methods=["GET", "POST"])
# Connect sa_textBlob() function to route
def sa_textBlob():
    # Create SA object and assign request attributes to object properties
    obj_SA = SA()
    sa(request, obj_SA)
    # Save properties values in a dictionary
    kwargs = dict(
        text=obj_SA.text,
        pos_threshold=obj_SA.pos_threshold,
        neg_threshold=obj_SA.neg_threshold,
    )
    # Run model (filter out the arguments with None as their value)
    retvalue = obj_SA.textBlob(**{k: v for k, v in kwargs.items() if v is not None})
    # Return results in json format
    return jsonify(retvalue)


# Sentiment Analysis with Flair model
# Decorator: route definition to /sentiment/flair address
@app.route("/sentiment/flair", methods=["GET", "POST"])
# Connect sa_flair() function to route
def sa_flair():
    # Create SA object and assign request attributes to object properties
    obj_SA = SA()
    sa(request, obj_SA)
    # Save properties values in a dictionary
    kwargs = dict(
        text=obj_SA.text,
        threshold=obj_SA.threshold
    )
    # Run model (filter out the arguments with None as their value)
    retvalue = obj_SA.flair(**{k: v for k, v in kwargs.items() if v is not None})
    # Return results in json format
    return jsonify(retvalue)


# NER with Spacy model
# Decorator: route definition to /ner/spacy address
@app.route("/ner/spacy", methods=["GET", "POST"])
# Connect ner_spacy() function to route
def ner_spacy():
    # Create NER object and assign request attributes to object properties
    obj_NER = NER()
    ner(request, obj_NER)
    # Run model
    return obj_NER.spacy(obj_NER.text, obj_NER.tags)


# NER with NLTK model
# Decorator: route definition to /ner/nltk address
@app.route("/ner/nltk", methods=["GET", "POST"])
# Connect ner_nltk() function to route
def ner_nltk():
    # Create NER object and assign request attributes to object properties
    obj_NER = NER()
    ner(request, obj_NER)
    # Handle 'ORGANIZATION' label
    if not obj_NER.tags is None and "ORG" in obj_NER.tags:
        obj_NER.tags.remove("ORG")
        obj_NER.tags.append("ORGANIZATION")
    # Run model
    return obj_NER.nltk(obj_NER.text, obj_NER.tags)


# NER with Flair model
# Decorator: route definition to /ner/flair address
@app.route("/ner/flair", methods=["GET", "POST"])
# Connect ner_flair() function to route
def ner_flair():
    # Create NER object and assign request attributes to object properties
    obj_NER = NER()
    ner(request, obj_NER)
    # Run model
    return obj_NER.flair(obj_NER.text, obj_NER.tags)


if __name__ == "__main__":
    app.run()
