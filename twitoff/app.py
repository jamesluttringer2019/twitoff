from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route("/")
    def index():
        DB.create_all()
        return render_template('base.html', title="Welcome to TwitOff", users=User.query.all())

    @app.route('/predict', methods=['POST'])
    def predict(user1=None, user2=None, tweet=None, message=''):
        u1 = request.values['u1']
        u2 = request.values['u2']
        tweet = request.values['tweet']
        udict = {1:u1, 0:u2}
        try:
            pred = predict_user(u1, u2, tweet)[0]
            message = f'It is more likely that {udict[pred]} posted this tweet'
        except Exception as e:
            message = f'Error while predicting: {e}'
        return render_template('predict.html', m=message, u1=u1, u2=u2, tweet=tweet)
            
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['username']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} successfully added!'
            tweets = User.query.filter(User.name==name).one().tweets
        except Exception as e:
            message = f'Error while trying to add user {name}: {e}'
            tweets = []
        return render_template('user.html', title=name, message=message, tweets=tweets)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('reset.html')
    
    return app