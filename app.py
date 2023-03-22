from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from psycopg2 import IntegrityError
from models import Feedback, connect_db, db, User
from forms import RegistrationForm, LoginForm, FeedbackForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "auth123"

connect_db(app)
db.create_all()

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)


@app.route('/')
def home():
    "render home template"
    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("User name taken, pick another.")
            render_template()

        db.session.commit()

        session['username'] = new_user.username
        flash("Welcome")

        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"welcome back, {user.username}", "primary")
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    flash("goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>')
def secret(username):
    user = User.query.filter_by(username=username)
    feed = db.session.query(Feedback).filter_by(username=username).all()

    if "username" not in session:
        flash("Please login first!")
        return redirect('/')
    else:
        return render_template('user_details.html', user=user, feed=feed)


@app.route('/users/<username>/delete', methods=["GET", "POST"])
def delete_user(username):
    if "username" not in session:
        flash("Please login first!")
        return redirect('/')

    user = User.query.filter_by(username=username)

    for u in user:
        user = u

    if username == session['username']:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash('user succesfully deleted', 'success')
        return redirect('/')
    flash('you dont have permission')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):

    form = FeedbackForm()
    if "username" not in session:
        flash("please login first!")
        return redirect('/')

    if session["username"] != username:
        flash("You can only add feedback to your own account!")
        return redirect('/')

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feed = Feedback(title=title, content=content, username=username)
        db.session.add(new_feed)
        db.session.commit()
        flash('feedback added succefully')
        return redirect(f'/users/{username}')
    return render_template("add_feedback.html", form=form)


@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def update_feedback(id):
    feed = db.session.query(Feedback).filter_by(id=id).first()

    if "username" not in session:
        flash("please login first!")
        return redirect('/')

    if session["username"] != feed.username:
        flash("You can only add feedback to your own account!")
        return redirect('/')

    form = FeedbackForm(obj=feed)
    if form.validate_on_submit():
        form.populate_obj(feed)
        db.session.commit()
        flash("feedback updated succefully")
        return redirect(f'/users/{feed.username}')
    return render_template("update_feedback.html", form=form)


@app.route('/feedback/<int:id>/delete')
def delete_a_feedback(id):

    if "username" not in session:
        flash("please login")
        return redirect('/login')
    feed = Feedback.query.get_or_404(id)
    if feed.username == session['username']:
        db.session.delete(feed)
        db.session.commit()
        flash('Feedback succesfully deleted', "success")
        return redirect(f'/users/{feed.username}')
    return redirect('/')
