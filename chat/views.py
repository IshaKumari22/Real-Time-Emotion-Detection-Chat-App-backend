from rest_framework.decorators import api_view
from rest_framework.response import Response
import tensorflow as tf
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model and preprocessors once
model = tf.keras.models.load_model('saved_model/emotion_model.keras')
tokenizer = joblib.load('saved_model/tokenizer.joblib')
label_encoder = joblib.load('saved_model/label_encoder.joblib')

@api_view(['POST'])
def predict_emotion(request):
    text = request.data.get('text')
    if not text:
        return Response({"error": "No text provided"}, status=400)

    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=50)
    pred = model.predict(padded)
    emotion_index = pred.argmax(axis=1)[0]
    emotion = label_encoder.inverse_transform([emotion_index])[0]

    return Response({"emotion": emotion})
