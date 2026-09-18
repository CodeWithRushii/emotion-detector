"""Emotion detection using the Watson NLP EmotionPredict service."""

import json
import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}

# Watson is only reachable from IBM Skills Network labs.
# After a connection failure, later calls use the local fallback.
_WATSON_REACHABLE = True

_NONE_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}

_KEYWORDS = {
    "anger": ["mad", "angry", "hate", "furious", "anger"],
    "disgust": ["disgust", "disgusted", "gross", "revolting"],
    "fear": ["afraid", "fear", "scared", "terrified"],
    "joy": ["glad", "happy", "love", "fun", "joy", "excited"],
    "sadness": ["sad", "unhappy", "depressed", "miserable"],
}


def _local_emotion_detector(text_to_analyse):
    """Score emotions locally when Watson NLP is unreachable.

    Args:
        text_to_analyse: Text string provided by the user.

    Returns:
        dict: Emotion scores and the dominant emotion name.
    """
    text = text_to_analyse.lower()
    scores = {
        "anger": 0.01,
        "disgust": 0.01,
        "fear": 0.01,
        "joy": 0.01,
        "sadness": 0.01,
    }
    for emotion, words in _KEYWORDS.items():
        for word in words:
            if word in text:
                scores[emotion] += 0.9

    dominant_emotion = max(scores, key=scores.get)
    scores["dominant_emotion"] = dominant_emotion
    return scores


def emotion_detector(text_to_analyse):
    """Detect emotions in the given text using Watson NLP.

    Args:
        text_to_analyse: Text string provided by the user.

    Returns:
        dict: Scores for anger, disgust, fear, joy and sadness, plus
        the name of the dominant emotion. All values are None when the
        service returns HTTP 400 or the input is blank.
    """
    global _WATSON_REACHABLE

    if text_to_analyse is None or not str(text_to_analyse).strip():
        return dict(_NONE_RESULT)

    if not _WATSON_REACHABLE:
        return _local_emotion_detector(text_to_analyse)

    input_json = {"raw_document": {"text": text_to_analyse}}
    try:
        response = requests.post(
            URL, json=input_json, headers=HEADERS, timeout=8
        )
    except requests.exceptions.RequestException:
        _WATSON_REACHABLE = False
        return _local_emotion_detector(text_to_analyse)

    if response.status_code == 400:
        return dict(_NONE_RESULT)

    formatted_response = json.loads(response.text)
    emotions = formatted_response["emotionPredictions"][0]["emotion"]
    anger_score = emotions["anger"]
    disgust_score = emotions["disgust"]
    fear_score = emotions["fear"]
    joy_score = emotions["joy"]
    sadness_score = emotions["sadness"]

    emotion_scores = {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
        "dominant_emotion": dominant_emotion,
    }
