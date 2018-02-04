from flask import request, redirect, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import time




app = Flask(__name__)
app.debug = True # This line helps us see what's going on when there's ;an error!
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mtfhkoorbaejkj:34a0e9e67baee29c0c860a9823647b4470b403052a5931bc7d0e981d784fae16@ec2-50-16-231-2.compute-1.amazonaws.com:5432/dbj3vbbsjfgepd                                                                                                                   v cc'
db = SQLAlchemy(app)

current_user =  "Not Logged In"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable = False)
    degree = db.Column(db.String(80))
    name=db.Column(db.String(80), nullable = False)
    password=db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user = db.Column(db.String(30), nullable= False)
	title = db.Column(db.String(30), nullable = False)
	question = db.Column(db.String(80), nullable = False)
	time = db.Column(db.String(80), nullable = False)
	reply = db.relationship('Reply', backref='question')
	def __repr__(self):
		return '<Question %r>' % self.title

class Reply(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
	user = db.Column(db.String(30), nullable= False)
	reply = db.Column(db.String(80), nullable = False)
	time = db.Column(db.String(80), nullable = False)
	def __repr__(self):
		return '<Reply %r>' % self.reply

#db.drop_all()
db.create_all()





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        new_user = User()
        new_user.name = request.form.get('name')
        new_user.degree = request.form.get('degree')
        new_user.username = request.form.get('username')
        new_user.password = request.form.get('pwd')
        db.session.add(new_user)
        db.session.commit() #bug is here
        #print(3)
        #print(User.query.all())
        global current_user
        current_user = new_user
        return render_template("user.html", current_user=current_user)
    elif request.method=='GET':
        return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='GET':
		return render_template('login.html', current_user="s")
	elif request.method=='POST':
		password_attempt = request.form.get('pwd')
		user = User.query.filter_by(username=request.form.get('username')).first()
		if user:
			if password_attempt != user.password:
				print("Incorrect password")
				return render_template('incorrect_pwd.html')
			else:
				global current_user
				current_user = user
				return render_template('user.html', current_user=user)
		else:
			print("Username not found")
			return render_template("no_username.html")

	



@app.route('/question', methods=['GET', 'POST'])
def question():
	if request.method=='POST':
		new_question = Question()
		global current_user
		new_question.user = str(current_user)
		new_question.title = request.form.get('title')
		new_question.question = request.form.get('question')
		localtime = time.localtime(time.time())
		new_question.time = str(localtime[1])+"/"+str(localtime[2])+"/"+str(localtime[0])+" at "+str(localtime[3])+":"+str(localtime[4])
		db.session.add(new_question)
		db.session.commit() #bug is here
		all_questions = Question.query.all()
		all_replies = Reply.query.all()
		return render_template("q&a.html",all_replies=all_replies, all_questions=all_questions, current_user=current_user)
	elif request.method=='GET':
		all_questions = Question.query.all()
		all_replies = Reply.query.all()
		return render_template('q&a.html',all_replies=all_replies, all_questions=all_questions, current_user=current_user)


@app.route('/reply/<question_id>', methods=['POST'])
def reply(question_id): #pass it current question as a parameter, question.id
	new_reply = Reply()
	new_reply.question_id = question_id
	new_reply.user = str(current_user)
	new_reply.reply = request.form.get('reply')
	localtime = time.localtime(time.time())
	new_reply.time = str(localtime[1])+"/"+str(localtime[2])+"/"+str(localtime[0])+" at "+str(localtime[3])+":"+str(localtime[4])
	db.session.add(new_reply)
	db.session.commit()
	all_questions = Question.query.all()
	all_replies = Reply.query.all()
	return render_template('q&a.html',all_replies=all_replies, all_questions=all_questions, current_user=current_user)




@app.route('/logout')
def logout():
	global current_user
	current_user = "Not Logged In"
	return render_template('login.html', current_user=current_user)


@app.route('/user')
def user():
	#questions = Question.query.filter_by(user=current_user).first()
	#print("questions:", questions)
	return render_template('user.html', current_user=current_user)

@app.route('/')
def main():
	return render_template('main.html', current_user=current_user)

@app.route('/neurotransmitters')
def neurotransmitters():
	return render_template('neurotransmitters.html', current_user=current_user)

@app.route('/brain-anatomy')
def brain_anatomy():
	return render_template('brain_anatomy.html', current_user=current_user)


@app.route('/incorrect-password')
def incorrect_password():
	return render_template('incorrect_pwd.html')

if __name__ == "__main__":
    app.run()




# What happens if username is not in the database when user logs in
# Loging in when password is incorrect (Not entering else)
# Show html according to javascript if statements (if user is logged in display post question form and show username)
# Reply thing