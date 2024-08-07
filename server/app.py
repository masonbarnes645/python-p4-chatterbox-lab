from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource


from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app)
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

class GetMessages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]
        return make_response(jsonify(messages), 200)
    
    def post(self):
        data = request.get_json()
        newMessage = Message(**data)
        try:
            db.session.add(newMessage)
            db.session.commit()
            return make_response(newMessage.to_dict(), 201)
        except:
            db.rollback()


api.add_resource(GetMessages, '/messages')

class DeletePatch(Resource):
    def patch(self,id):
        data = request.get_json()
        message = db.session.get(Message, id)

        try:
            for attr, value in data.items():
                setattr(message, attr, value)
            
            return make_response(message.to_dict(), 201)

        except:
            pass

    def delete(self, id):
        message = db.session.get(Message, id)
        db.session.delete(message)
        db.session.commit()
        return make_response('', 204)

api.add_resource(DeletePatch,'/messages/<int:id>')



if __name__ == '__main__':
    app.run(port=5555)



# for attr, value in data.items()
#     setattr(message, attr, value)