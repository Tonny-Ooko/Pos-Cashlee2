from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import render_template, redirect, url_for,flash
from flask_login import login_user, current_user, login_required, logout_user
from flask_login import UserMixin
from argon2 import PasswordHasher




app = Flask(__name__, template_folder='.')
db = SQLAlchemy(app)
ph = PasswordHasher()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            ph.verify(self.password_hash, password)
            return True
        except:
            return False

class AuditResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_text = db.Column(db.String(128))



# Your route definitions here
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('audit'))

    from urllib import request
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('audit'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/audit', methods=['GET', 'POST'])
@login_required
def audit():
    from urllib import request
    if request.method == 'POST':
        result_text = request.form.get('result_text')
        audit_result = AuditResult(result_text=result_text)
        db.session.add(audit_result)
        db.session.commit()
        flash('Audit result saved', 'success')

    audit_results = AuditResult.query.all()
    return render_template('audit.html', audit_results=audit_results)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
