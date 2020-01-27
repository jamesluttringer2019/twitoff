from flask import Flask, render_template
from .models import DB, User, Tweet
from random import sample

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
    DB.init_app(app)

    @app.route("/")
    def index():
        username = sample(user_list, 1)[0]
        tweet = Tweet(text=(sample(tweet_list, 1)[0]))
        if DB.session.query(User.query.filter(User.name==username).exists()).scalar()==False:
            user = User(name=username)
        else:
            user = User.query.filter_by(name=username).first()
            pass
        
        user.tweets.append(tweet)
        DB.session.add(user)
        DB.session.commit()
        return "Index Page"
    
    @app.route('/hello')
    def hello():
        return render_template('base.html', title='hello')
    
    return app

user_list = ['elonmusk', 'yourmom', 'shrek', 'steve']

tweet_list = [
    'today is a good day',
    'my head hurts',
    'I want to go home',
    'get out of my swamp',
    'party?',
    'Cybertruck lol'
]