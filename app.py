from flask import Flask, render_template, flash, redirect, render_template, jsonify, request,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, EditForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():

    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect('/users/register')

    id = session['uid']
    user = User.query.get_or_404(id)
    posts = feedback.query.all()
    return render_template('home.html', posts=posts)  

@app.route('/users/register', methods=['GET','POST'])
def handle_register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        data = {key:val for key,val in form.data.items() if key != 'csrf_token'}
        user = User.register(**data)
        db.session.add(user)
        db.session.commit()
        session['uid']= user.id
        session['username'] =user.username

        return redirect(f'/users/{user.username}')
    else:
        return render_template('/register.html', form=form)
    
@app.route('/users/<username>')
def render_user_page(username):

    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect(f'/users/register')

    user = User.query.filter_by(username=username).first()
    id = session['uid']

    if user.id != id :
        return redirect(f'/users/register')

    return render_template('profile.html', user=user)

@app.route('/login', methods=['GET','POST'])
def handle_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        session['uid'] = user.id
        session['username'] =user.username
        if user:
            return redirect(f'/users/{user.username}')
        else:
            flash('invalid username or password')
            return redirect('/login')
    
    return render_template('login.html', form = form)

@app.route('/logout')
def handle_logout():
    session.pop('uid')
    session.pop('username')

    return redirect('/login')

@app.route('/feedback', methods=['GET','POST'])
def redirect_to_feedback():
    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect('/users/register')
    
    id = session['uid']
    user = User.query.get_or_404(id)
    form = FeedbackForm()
    if form.validate_on_submit():
        data = {key:val for key,val in form.data.items() if key != 'csrf_token'}
        feedback = Feedback(**data)
        feedback.username = user.username
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'users/{user.username}')
    else:
        return render_template('feedback_form.html', form = form)

@app.route('/feedback/<int:id>/edit', methods=['GET', 'POST'])
def handle_edit_feedback(,id):
    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect('/users/register')

    user = User.query.filter_by(username=username).first()
    uname = session['username']

    if uname != user.username:
        flash('No sneaky stuff!')
        return redirect(f'/users/{uname}')

    feedback = Feedback.query.get_or_404(id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()
        
        return redirect(f'/users/{user.username}')
    else:

        return render_template('edit_feedback.html', form=form)

@app.route('/feedback/<int:id>/delete')
def delete_post(id):
    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect('/users/register')
    
    uname = session['username']
    feedback = Feedback.query.get_or_404(id)

    if uname != feedback.username:
        flash('No sneaky stuff!')
        return redirect(f'/users/{uname}')

    Feedback.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(f'/users/{username}')

@app.route('/users/<username>/delete')
def delete_user(username):
    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect('/users/register')
    
    uname = session['username']
    user = User.query.filter_by(username=username).first()

    if uname != user.username:
        flash('No sneaky stuff!')
        return redirect(f'/users/{uname}')
    
    User.query.filter_by(id=user.id).delete()
    session.pop('uid')
    session.pop('username')
    db.session.commit()
    return redirect('/')

@app.route('/users/<username>/edit', methods=['GET','POST'])
def edit_user(username):
    #no logged in user
    if 'uid' not in session:
        flash('Please Register or Log in')
        return redirect('/users/register')
    
    uname = session['username']
    user = User.query.filter_by(username=username).first()

    #logged in user doesnt match route user
    if uname != user.username:
        flash('No sneaky stuff!')
        return redirect(f'/users/{uname}')

    form = EditForm(obj=user)
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data

        db.session.add(user)
        db.session.commit()
        return redirect(f'/users/{uname}')
    else:
        return render_template('edit_user.html', form=form)



