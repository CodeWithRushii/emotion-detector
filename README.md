# Emotion Detection

**Project name:** Emotion Detection  
**Repository:** final_project / oaqjp-final-project-emb-ai  
**Author:** CodeWithRushii

Final project for the IBM Coursera course **Developing AI Applications with Python and Flask**.

This web application analyzes customer feedback text and detects these emotions using the Watson NLP Emotion Predict function:

- anger
- disgust
- fear
- joy
- sadness

It also returns the **dominant emotion**.

## Features

- Emotion detection with Watson NLP
- Packaged Python module: `EmotionDetection`
- Flask web app on `localhost:5000`
- Unit tests for joy, anger, disgust, sadness, and fear
- Blank-input error handling
- Pylint score: **10.00/10**

## Project structure

```text
final_project/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── static/
│   └── mywebscript.js
├── templates/
│   └── index.html
├── server.py
├── test_emotion_detection.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/CodeWithRushii/emotion-detector.git
cd emotion-detector
pip install -r requirements.txt
```

## Run the web application

```bash
python server.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

- Flask route: `/emotionDetector`
- Query parameter: `textToAnalyze`

Example:

```text
http://127.0.0.1:5000/emotionDetector?textToAnalyze=I%20think%20I%20am%20having%20fun
```

Example response:

```text
For the given statement, the system response is 'anger': 0.01, 'disgust': 0.01, 'fear': 0.01, 'joy': 0.91 and 'sadness': 0.01. The dominant emotion is joy.
```

## Use the package in Python

```python
from EmotionDetection.emotion_detection import emotion_detector

print(emotion_detector("I love this new technology."))
```

Output format:

```python
{
    "anger": anger_score,
    "disgust": disgust_score,
    "fear": fear_score,
    "joy": joy_score,
    "sadness": sadness_score,
    "dominant_emotion": "joy"
}
```

## Run unit tests

```bash
python test_emotion_detection.py
```

| Statement | Dominant emotion |
| --- | --- |
| I am glad this happened | joy |
| I am really mad about this | anger |
| I feel disgusted just hearing about this | disgust |
| I am so sad about this | sadness |
| I am really afraid that this will happen | fear |

## Error handling

If the Watson service returns status code `400`, or the user submits blank text, all emotion values are `None`.

The web app then displays:

```text
Invalid text! Please try again!
```

## Static code analysis

```bash
python -m pylint server.py
```

Expected result:

```text
Your code has been rated at 10.00/10
```

## Watson NLP API

- URL: `https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict`
- Header: `grpc-metadata-mm-model-id: emotion_aggregated-workflow_lang_en_stock`
- Input: `{ "raw_document": { "text": text_to_analyse } }`

Note: The IBM Skills Network Watson endpoint works inside the Coursera lab. Outside the lab, the app uses a local fallback with the same output format.

## License

This project uses the Apache License 2.0.
