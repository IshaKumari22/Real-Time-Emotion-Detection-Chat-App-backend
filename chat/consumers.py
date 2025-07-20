import json
from channels.generic.websocket import AsyncWebsocketConsumer
import tensorflow as tf
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences
from .models import Message, Thread
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

model = tf.keras.models.load_model('saved_model/emotion_model.keras')
tokenizer = joblib.load('saved_model/tokenizer.joblib')
label_encoder = joblib.load('saved_model/label_encoder.joblib')

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f"chat_thread_{self.thread_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')

        # ✅ Emotion prediction
        seq = tokenizer.texts_to_sequences([message_text])
        padded = pad_sequences(seq, maxlen=50)
        prediction = model.predict(padded)
        emotion = label_encoder.inverse_transform([prediction.argmax(axis=1)[0]])[0]

        # ✅ Get actual user instance (resolves LazyObject safely)
        user = await sync_to_async(self._get_user)()

        # ✅ Save to database
        await sync_to_async(self.save_message)(user, message_text, emotion)

        # ✅ Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'emotion': emotion
            }
        )

    def _get_user(self):
        return User.objects.get(id=self.scope['user'].id)

    def save_message(self, user, message_text, emotion):
        thread = Thread.objects.get(id=self.thread_id)
        Message.objects.create(thread=thread, user=user, content=message_text, emotion=emotion)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'emotion': event['emotion']
        }))
