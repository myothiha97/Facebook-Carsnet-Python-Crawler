import pyrebase
from firebase_config import firebase_config

class FirebaseHandler:
     _instance = None

     @staticmethod
     def instance():
          if '_instance' not in FirebaseHandler.__dict__:
               FirebaseHandler._instance = FirebaseHandler()
          return FirebaseHandler._instance


     def __init__(self):
          if FirebaseHandler._instance != None:
               raise Exception("This class is singleton")
          else:
               FirebaseHandler._instance = self
               
          self.firebase = pyrebase.initialize_app(firebase_config)
          self.storage = self.firebase.storage()

     def __repr__(self):
        return (f'{self.__class__.__name__}')

     def store_image_to_firebase(self, count, timestamp, url):
          img = self.storage.child(f'screenshots/{url}_{timestamp}.png').put(f'./screenshots/{count}_{url}_{timestamp}.png')
          bucket = img['bucket']
          name = img['name'].replace('/', '%2F')
          token = img['downloadTokens']
          return f"https://firebasestorage.googleapis.com/v0/b/{bucket}/o/{name}?alt=media&token={token}"
          