from flask_sqlalchemy import SQLAlchemy


def sqlalchemy_object(app):
    return SQLAlchemy(app)


def sqlalchemy_database(app, db):
    with app.app_context():
        class Member(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            id_number = db.Column(db.Integer, unique=True, nullable=False)
            firstname = db.Column(db.String, unique=False, nullable=False)
            surname = db.Column(db.String, unique=False, nullable=False)
            mobile = db.Column(db.Integer, unique=False, nullable=False)
            email = db.Column(db.String, unique=True, nullable=False)
            street_address = db.Column(db.String, unique=False, nullable=False)
            province = db.Column(db.String, unique=False, nullable=False)

        db.create_all()
            
        return Member
