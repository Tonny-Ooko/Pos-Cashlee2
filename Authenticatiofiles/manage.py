from app import app, db

@app.cli.command("initdb")
def initdb_command():
    db.create_all()
    print("Initialized the database.")
