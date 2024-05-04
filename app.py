import sqlite3
from flask import Flask, g, request, render_template, redirect, url_for

app = Flask(__name__)
app.config['DATABASE'] = 'bkb_drills.db'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create tables if they don't exist
def create_tables():
    with app.app_context():
        db = get_db()
        c = db.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS Drill_Descriptions (
                        id INTEGER PRIMARY KEY,
                        NumPlayers INTEGER,
                        TypeOfDrill TEXT,
                        Court TEXT,
                        Kind TEXT,
                        Name TEXT,
                        Goal TEXT,
                        Description TEXT,
                        Details TEXT,
                        Variations TEXT
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS bkb_drill (
                        id INTEGER PRIMARY KEY,
                        Date TEXT,
                        DrillID INTEGER,
                        FOREIGN KEY (DrillID) REFERENCES Drill_Descriptions(id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS Season (
                        id INTEGER PRIMARY KEY,
                        Drills_id INTEGER,
                        Time TEXT,
                        Duration TEXT
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS Cycles (
                        id INTEGER PRIMARY KEY,
                        Month TEXT,
                        Cycle TEXT,
                        Date TEXT,
                        Session_Type TEXT,
                        Session_Number INTEGER
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS Goals (
                        id INTEGER PRIMARY KEY,
                        Goal_id INTEGER,          
                        Type_of_Goal TEXT,
                        Name_of_Goal TEXT,
                        Specificity TEXT,
                        Date_Session TEXT
                    )''')

        db.commit()

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Add drill route
@app.route('/add_drill', methods=['GET', 'POST'])
def add_drill():
    if request.method == 'POST':
        num_players = request.form['num_players']
        type_of_drill = request.form['type_of_drill']
        court = request.form['court']
        kind = request.form['kind']
        name = request.form['name']
        goal = request.form['goal']
        description = request.form['description']
        details = request.form['details']
        variations = request.form['variations']

        db = get_db()
        c = db.cursor()

        c.execute('''INSERT INTO Drill_Descriptions
                     (NumPlayers, TypeOfDrill, Court, Kind, Name, Goal, Description, Details, Variations)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (num_players, type_of_drill, court, kind, name, goal, description, details, variations))
        db.commit()

        return redirect(url_for('index'))

    return render_template('add_drill.html')

# Add workout route
@app.route('/add_workout', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        date = request.form['date']
        drill_id = request.form['drill_name']

        db = get_db()
        c = db.cursor()

        c.execute('''INSERT INTO bkb_drill (Date, DrillID) VALUES (?, ?)''', (date, drill_id))
        db.commit()

        return redirect(url_for('index'))

    db = get_db()
    c = db.cursor()
    c.execute('''SELECT Name FROM Drill_Descriptions''') # Get all drills
    drills = c.fetchall()

    return render_template('add_workout.html', drills=drills)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=30873, host='0.0.0.0')
