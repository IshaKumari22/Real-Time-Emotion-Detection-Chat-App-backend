# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# import tensorflow as tf
# import joblib
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# model = tf.keras.models.load_model('saved_model/emotion_model.keras')
# tokenizer = joblib.load('saved_model/tokenizer.joblib')
# label_encoder = joblib.load('saved_model/label_encoder.joblib')

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add('chatroom', self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard('chatroom', self.channel_name)

#     async def receive(self, text_data):
#         text_json = json.loads(text_data)
#         message = text_json['message']

#         # Predict emotion
#         seq = tokenizer.texts_to_sequences([message])
#         padded = pad_sequences(seq, maxlen=50)
#         prediction = model.predict(padded)
#         emotion = label_encoder.inverse_transform([prediction.argmax(axis=1)[0]])[0]

#         # Broadcast message + emotion
#         await self.channel_layer.group_send(
#             'chatroom',
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'emotion': emotion
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'emotion': event['emotion']
#         }))




from channels.generic.websocket import AsyncWebsocketConsumer

class PersonalChatConsumer(AsyncWebsocketConsumer):

  async def connect(self):


    print("TESTING CONNECTION AND REDIS")
    await self.accept()
