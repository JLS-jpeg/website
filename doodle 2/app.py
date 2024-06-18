from flask import Flask, render_template, redirect, url_for, session, request
import pymysql
app = Flask(__name__)
app.secret_key = "super secret key"

from collections import defaultdict

d = defaultdict(list)    
d[0].append(1)

if __name__ == '__main__':
    app.run(debug=True)


app.config['MYSQL_HOST'] = 'localhost'  # Adresse de votre base de données MySQL
app.config['MYSQL_PORT'] = 8889  # Port de votre base de données MySQL
app.config['MYSQL_USER'] = 'bastien'  # Nom d'utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'bastien'  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'doodle' # Nom de votre base de données MySQL

# Fonction pour se connecter à la base de données
def connect_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
     
# Fonction pour récupérer un utilisateur depuis la base de données
def get_formateurs(mail):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM Formateurs WHERE mail = %s", (mail,))
    user = cur.fetchone()
    cur.close()
    db.close()
    return user

@app.route('/loginformateurs', methods=['GET', 'POST'])
def loginformateurs():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['MDP']
        user = get_formateurs(mail)
        if user and user['MDP'] == password:
            session['mail'] = mail
            return redirect(url_for('formateurs'))
    return render_template('connectformateurs.jinja')

def get_apprenties(mail):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM Apprenties WHERE mail = %s", (mail,))
    user = cur.fetchone()
    cur.close()
    db.close()
    return user

@app.route('/loginapprenties', methods=['GET', 'POST'])
def loginapprenties():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['MDP']
        user = get_apprenties(mail)
        if user and user['MDP'] == password:
            session['mail'] = mail
            return redirect(url_for('apprenties'))
    return render_template('accueil.jinja')

@app.route('/logout')
def logout():
    session.pop('mail', None)
    return redirect(url_for('connect'))

@app.route('/')
def accueil():
    #page d'accueil
    return render_template('accueil.jinja')

@app.route('/centres.jinja')
def centres():
    #page centres
    return render_template('centres.jinja')

@app.route('/connectformateurs.jinja')
def connect():
    #page de connexion pour les formateurs
    return render_template('connectformateurs.jinja')

@app.route('/espaceformateurs.jinja')
def formateurs():
    #page formateurs
    return render_template('espaceformateurs.jinja')

@app.route('/espaceapprenties.jinja')
def apprenties():
    #page apprenties
    return render_template('espaceapprenties.jinja')