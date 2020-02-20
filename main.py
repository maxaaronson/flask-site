import site
import sys
site.addsitedir('/home/amset/webapps/max_flask/venv/lib/python3.5/site-packages')

from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   jsonify,
                   session as login_session,
                   g,
                   make_response)
from db_setup import Base, Projects, Education, Work_Experience, About, User
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user
from forms import LoginForm


app = Flask(__name__)

engine = create_engine(open('/home/amset/webapps/max_flask/htdocs/db_connect').readline())
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


################################################################
# Admin views
################################################################
class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

admin = Admin(app, name='Max\'s Site', template_mode='bootstrap3')

admin.add_view(MyModelView(Projects, session))
admin.add_view(MyModelView(About, session))
admin.add_view(MyModelView(Education, session))
admin.add_view(MyModelView(Work_Experience, session))
admin.add_view(MyModelView(User, session))

##################################################
# Routing
##################################################
@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        prog_array = {""}
        if (request.form.get('Java') == "on"):
            prog_array.add('Java')
        if (request.form.get('JS') == "on"):
            prog_array.add('JS')
        if (request.form.get('Python') == "on"):
            prog_array.add('Python')
        print(prog_array)
        projects = session.query(Projects).filter(Projects.type.in_(prog_array))
    else:
        projects = session.query(Projects)
    return render_template("main.html", projects=projects)

@app.route("/about/")
def about():
    return render_template("about.html",
        about=session.query(About))

@app.route("/resume/")
def resume():
    return render_template("resume.html",
        work_experience=session.query(Work_Experience).order_by(desc(Work_Experience.id)),
        education=session.query(Education))

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/game/")
def game():
    filename = request.args.get('filename', None)
    return render_template(filename)


####################################################
# Login code
###################################################
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'you-will-never-guess'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print("user loader called with id " + user_id)
    user = session.query(User).filter(User.id==user_id).first()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    #print(current_user)
    if current_user.is_authenticated:
        print(current_user)
        return "already logged in"
    form = LoginForm()
     #print(form.validate_on_submit())
     #print(form.errors)
    if form.validate_on_submit():
        user = session.query(User).filter(User.user_name==form.username.data).first()
        if user is None or not user.checkPassword(form.password.data):
            #print("username is .............:")
            #print(user)
            flash('Invalid username or password')
            return render_template('login.html', title='Sign In', form=form)
        login_user(user)
        return redirect(url_for('main'))
    return render_template('login.html', title='Sign In', form=form)

###########################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)


