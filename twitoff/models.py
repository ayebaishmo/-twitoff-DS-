from flask_sqlalchemy import SQLAlchemy

# Create a DB object from SQLAlchemy class 
DB =SQLAlchemy()

#Making a user table using SQLAlchemy
class User(DB.Model):
    # create a user Table with SQLAlchemy
    #id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    username = DB.Column(DB.String, nullable=False)

    
class Tweet(DB.Model):
    # we kep track if tweets for each user
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
