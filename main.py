from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
import requests
from datetime import datetime
from databases import sqlalchemy_object, sqlalchemy_database
from forms import ContactForm, JoinForm
from news import MakeSoup
from requests.exceptions import ConnectionError
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "SSSHHHHHHHHH It's a secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///member.db"

Bootstrap(app)

db = sqlalchemy_object(app)
Member = sqlalchemy_database(app, db)


def data(file, lst):
    with open(f"static/manifesto/{file}.txt") as file:
        contents = file.read()
        altered_contents = contents.split("%")
        more_altered_contents = [content.replace("\n", "").split("*") for content in altered_contents]

        links = lst

        for num in range(len(links)):
            lst = more_altered_contents[num]
            link = links[num]

            lst.append(link)
    return more_altered_contents


def current_year():
    date_time = datetime.now()
    year = date_time.strftime("%Y")
    return year


def detect_connection_error(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            return abort(503, "Failed to connect to news24 server please check your network.")
    return wrapper_func


@app.route("/")
@detect_connection_error
def home():
    images = [f"IMG-20230501-WA00{num}.jpg" for num in [23, 27, 31, 33, 34, 38]]

    links = [
            "https://c0.wallpaperflare.com/preview/931/296/849/business-idea-planning-board-business-plan.jpg",
            "https://st2.depositphotos.com/1760420/7223/i/450/depositphotos_72232193-stock-photo-different-people-matching-three-puzzle.jpg",
            "https://images.flatworldknowledge.com/carpenter_2_0-28123/carpenter_2_0-28123-fig021.jpg",
            "https://iea.imgix.net/3a99e1d9-6b91-4882-9111-652d6cfabcb1/Getty1366044287.jpg?auto=compress%2Cformat&fit=min&q=80&rect=0%2C0%2C7360%2C4912&w=760&fit=crop&fm=jpg&q=70&auto=format&h=507",
            "https://www.tktcambridge.com/wp-content/uploads/2019/01/scheme-768x569.jpg",
            "https://www.salesforce.com/content/dam/blogs/eu/2022/future-growth-plan.png"
            ]

    makesoup = MakeSoup()
    all_news_data = makesoup.collected_data
    some_news_data = [all_news_data[article] for article in [f"article{num + 1}" for num in range(3)]]
    
    return render_template(
        "home.html",
        images=images,
        data_lst=data("SRCManifest", links),
        articles=some_news_data,
        current_year=current_year()
        )


@app.route("/leadership")
def leadership():
    with open("static/manifesto/name-and-story.txt") as file:
        contents = file.read()
        altered_contents = contents.split("%")
        more_altered_contents = [content.replace("\n", "").split("*") for content in altered_contents]

    links1 = [
        "https://cdn-icons-png.flaticon.com/512/709/709699.png",
        "https://cdn-icons-png.flaticon.com/512/709/709699.png"
        ]
    
    links2 = [
        "https://cdn-icons-png.flaticon.com/512/709/709699.png",
        "https://cdn-icons-png.flaticon.com/512/709/709699.png"
        ]

    links3 = [
        "https://cdn-icons-png.flaticon.com/512/709/709699.png",
        "https://cdn-icons-png.flaticon.com/512/709/709699.png"
        ]
    

    positions = ["OUR PROVINCIAL CHAIRS", "OUR EXECUTIVE TEAM", "OUR SENATE"]
    carousel_ids = ["provincial-chairs-carousel", "executives-carousel", "senates-carousel"]
    
    all_data = [
        data("provincial-chairs",links1),
        data("executive-team",links2),
        data("senate",links3)
            ]

    data_num = len(all_data)
        
    return render_template(
        "leadership.html",
        member_info=more_altered_contents,
        positions=positions,
        data_lst=all_data,
        data_num=data_num,
        carousel_ids=carousel_ids,
        current_year=current_year()
        )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("MESSAGE SENT.")
    return render_template("contact.html", form=form)


def test_if_int(string):
    try:
        int(string)
        return False
    except ValueError:
        return True


@app.route("/join", methods=["GET", "POST"])
def join():
    form = JoinForm()
    id_numbers = [data.id_number for data in db.session.query(Member).all()]
    emails = [data.email for data in db.session.query(Member).all()]

    if form.validate_on_submit():
        if test_if_int(form.id_number.data):
            flash("Invalid ID number")
        elif test_if_int(form.mobile.data):
            flash("Invalid mobile number")
        elif int(form.id_number.data) in id_numbers:
            flash("ID number is already in database")
        elif form.email.data in emails:
            flash("Email is already in database")
        else:
            member = Member(
                id_number=int(form.id_number.data),
                firstname=form.firstname.data,
                surname=form.surname.data,
                mobile=int(form.mobile.data),
                email=form.email.data,
                street_address=form.street_address.data,
                province=form.province.data
            )
            db.session.add(member)
            db.session.commit()
            return redirect(url_for("home"))
        
    return render_template("join.html", form=form)


@app.route("/news")
@detect_connection_error
def news():
    makesoup = MakeSoup()
    all_news_data = makesoup.collected_data
    modified_news_data = [all_news_data[article] for article in [f"article{num + 1}" for num in range(len(all_news_data))]]
    return render_template("news.html", articles=modified_news_data)

    
@app.route("/read-more/<num>")
def read_more(num):
    
    render_template("read-more.html")


if __name__ == "__main__":
    app.run(debug=True)
