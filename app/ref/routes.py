from flask import render_template, redirect, flash, url_for, request
from app.ref import ref_bp
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Post, Event, Bet
from app.ref.forms import EventRegistrationForm, RegistrationForm, EditProfileForm, PostForm, LoginForm, EventBetForm, GetCoinForm, EventWinningForm
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
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


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
    return render_template('auth/user.html', title='Profile', user=user, posts=posts)



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
        diff = event.time_to_bet - datetime.utcnow()
        if diff.days>0:
            if (current_user.coins>form.amount.data):
                if event.amount:
                    event.amount = event.amount + form.amount.data
                else:
                    event.amount = form.amount.data
                current_user.coins = current_user.coins - form.amount.data
                winna = User.query.filter_by(username=form.betwinner.data).first_or_404()
                abet = Bet(user=current_user, winner=winna, event=event, amount=form.amount.data)
                db.session.add(abet)
                db.session.commit()
                return redirect(url_for('event'))
            else:
                return redirect(url_for('shop', username=current_user.username))
        else:
            flash('Event {} already ended.'.format(eventname))
            return redirect(url_for('event'))
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
    return render_template('events/create_event.html', title='CreateEvent', form=form)


@app.route('/add_challenger', methods=['POST'])
def add_challenger():
    challName='challenger0'
    event = Event(
        eventname=request.form['eventname'],
        time_to_bet=request.form['time_to_bet'],
    )
    for num in range(0, int(request.form['challenger'])):
        challDb = User.query.filter_by(username=request.form[challName]).first_or_404()
        event.add_challenger(challDb)
        challName=challName.replace(str(num), str(num+1))
    db.session.add(event)
    db.session.commit()
    flash('Creation succeded!')
        
    return redirect(url_for('event'))


@app.route('/event/validate_events', methods=['GET', 'POST'])
@login_required
def validate_events():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    event = Event.query.all()
    if current_user.username != 'admin':
        flash('You are no Admin.')
        return redirect(url_for('event'))
    else:
        for one_event in event:
            diff = one_event.time_to_bet - datetime.utcnow()
            if diff.days < 0 and one_event.winsetted:
                val_ev = Event.query.filter_by(eventname=one_event.eventname).all()
                for od_ev in val_ev:
                    betsonev = Bet.query.filter_by(event_id=od_ev.id)
                    if betsonev:
                        for bettings in betsonev:
                            winnerinbet = User.query.get(bettings.winner_id)
                            if winnerinbet in od_ev.winners and bettings.betonloose is False:
                                bettings.user.coins = bettings.user.coins + bettings.amount * 2
                                db.session.delete(bettings)
                            elif winnerinbet not in od_ev.winners and bettings.betonloose is True:
                                bettings.user.coins = bettings.user.coins + bettings.amount * 2
                                db.session.delete(bettings)
                            else:
                                db.session.delete(bettings)
                    db.session.delete(od_ev)
                    db.session.commit()
    return redirect(url_for('event'))


@app.route('/event/<eventname>/validate_event', methods=['GET', 'POST'])
@login_required
def validate_event(eventname):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    eventDb = Event.query.filter_by(eventname=eventname).first_or_404()
    import pdb;pdb.set_trace()
    if current_user.username != 'admin':
        flash('You are no Admin.')
        return redirect(url_for('event'))
    else:
        diff = eventDb.time_to_bet - datetime.utcnow()
        if diff.days < 0 and eventDb.winsetted:
            betsonev = Bet.query.filter_by(event_id=eventDb.id)
            if betsonev:
                for bettings in betsonev:
                    winnerinbet = User.query.get(bettings.winner_id)
                    if winnerinbet in evenDb.winners and bettings.betonloose is False:
                        bettings.user.coins = bettings.user.coins + bettings.amount * 2
                        db.session.delete(bettings)
                    elif winnerinbet not in eventDb.winners and bettings.betonloose is True:
                        bettings.user.coins = bettings.user.coins + bettings.amount * 2
                        db.session.delete(bettings)
                    else:
                        db.session.delete(bettings)
            db.session.delete(eventDb)
            db.session.commit()
        elif not eventDb.winsetted:
            flash('No Winner determined yet')
    return redirect(url_for('event'))


@app.route('/<eventname>/put_winner', methods=['GET', 'POST'])
@login_required
def put_winner(eventname):
    form = EventWinningForm(eventname)
    if request.method == 'GET':
        form.eventname.data = eventname
    return render_template('events/put_winner.html', title='PutWinner', form=form)

@app.route('/add_winner', methods=['POST'])
@login_required
def add_winner():
    winnerName='winner0'
    eventDb = Event.query.filter_by(eventname=request.form['eventname']).first_or_404()
    for num in range(0, int(request.form['winner'])):
        winnerDb = User.query.filter_by(username=request.form[winnerName]).first_or_404()
        eventDb.add_winner(winnerDb)
        winnerName=winnerName.replace(str(num), str(num+1))
    eventDb.winsetted=True
    db.session.add(eventDb)
    db.session.commit()
    flash('Winner set!')
        
    return redirect(url_for('event'))


@app.route('/event')
@login_required
def event():
    que = Event.query.all()
    eventlist = []
    if que:
        for eve in que:
            challengerlist = []
            for dudes in eve.challengers:
                challengerlist.append(dudes.username)
            if not eve.amount:
                eve.amount = 0
            if not eve.betting_quote:
                eve.betting_quote = '(0,5/0,5)'
            eventlist.append({
                'id': eve.id,
                'name': eve.eventname,
                'time_to_bet': eve.time_to_bet,
                'amount': eve.amount,
                'challenger': challengerlist
            })
        post = {'title': event, 'body': eventlist},
        return render_template('events/event.html', posts=post)
    else:
        return redirect(url_for('create_event'))


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
    return render_template("payment/shop.html", title='Deposit', form=form)

@app.route('/impressum/')
def impressum():
    return render_template('impressum.html')

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


