from flask import render_template, redirect, flash, url_for, request
from app.ref import ref_bp 
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post, Event
from app.ref.forms import EventRegistrationForm, RegistrationForm, EditProfileForm, PostForm, LoginForm, EventBetForm, GetCoinForm
from datetime import datetime
from app import app, db

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = [
        {
            'author': {'username': 'Bran'},
            'body': 'Best game eva!'
        },
        {
            'author': {'username': 'test'},
            'body': 'chat some!'
        }
    ]
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration succeded!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': ''},
    ]
    return render_template('auth/user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form)

@app.route('/event/<eventname>/bet', methods=['GET', 'POST'])
@login_required
def event_bet(eventname):
    form = EventBetForm(current_user.username)
    event = Event.query.filter_by(eventname=eventname).first_or_404()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if form.validate_on_submit():
        if (current_user.coins>form.amount.data):
            if event.amount:
                event.amount = event.amount + form.amount.data
            else:
                event.amount = form.amount.data
            current_user.coins = current_user.coins - form.amount.data
        else:
            return redirect(url_for('shop', username=current_user.username))
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    posts = [
        {'title': event, 'body': ''},
    ]
    return render_template('events/event_bet.html', title='Bet Event', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/set_coins/<username>')
@login_required
def set_coins(username):
    user = User.query.filter_by(username=username).first()
    admin = User.query.filter_by(username='admin').first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if current_user.username != 'admin':
        flash('You are no Admin.')
        return redirect(url_for('user', username=username))
    user.set_coins(user, 10)
    db.session.commit()
    flash('You spent {} some coins!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/event/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventRegistrationForm()
    if form.validate_on_submit():
        event = Event(eventname=form.eventname.data, time_to_bet=form.time_to_bet.data)
        time_to_bet = form.time_to_bet.data
        db.session.add(event)
        db.session.commit()
        flash('Creation succeded!')
        return redirect(url_for('event'))
    return render_template('events/create_event.html', title='CreateEvent', form=form)

@app.route('/event')
@login_required
def event():
    que = Event.query.all()
    eventlist = []
    for eve in que:
        if not eve.amount:
            eve.amount=0
        if not eve.betting_quote:
            eve.betting_quote='(0,5/0,5)'
        eventlist.append({'id': eve.id, 'name': eve.eventname, 'time_to_bet': eve.time_to_bet, 'amount': eve.amount, 'betting_quote': eve.betting_quote})
    post = {'title': event, 'body': eventlist},
    return render_template('events/event.html', posts=post)

@app.route('/event/<eventname>')
@login_required
def event_profile(eventname):
    event = Event.query.filter_by(eventname=eventname).first_or_404()
    posts = [
        {'title': event, 'body': ''},
    ]
    return render_template('events/event_profile.html', event=event, posts=posts)

@app.route('/shop', methods=['Get', 'Post'])
@login_required
def shop():
    form = GetCoinForm(current_user.username)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if form.validate_on_submit():
        user.coins = user.coins + form.amount.data
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template("payment/shop.html", title='Shop', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/hello')
def hello_world():
	return 'Hello, World!'


