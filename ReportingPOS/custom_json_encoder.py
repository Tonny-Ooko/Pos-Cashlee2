# type: ignore
from json import JSONEncoder
from datetime import datetime
import json
from flask import Flask
from .auth_module import User  # Import your User class

app = Flask(__name__)
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()

        return super().default(obj)

#class CustomJSONEncoder(json.JSONEncoder):
   # def default(self, obj):
        #if isinstance(obj, User):
            # Convert User object to a dictionary
            #return {
                #'id': obj.id,
                #'username': obj.username,
               # 'role': obj.role
           # }
        # For other non-serializable objects, use the default serialization
       # return super().default(obj)

# Register the custom JSON encoder with your Flask app
app.json_encoder = CustomJSONEncoder


