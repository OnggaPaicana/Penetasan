from distutils.log import debug
from app import create_app, db
from app.models import Tools
from dotenv import load_dotenv
import os


load_dotenv()
app = create_app(os.getenv("FLASK_ENV") or "production")

# make command insert of flask
@app.cli.command()
def insert() -> None:
    """Insert Tools to Database"""
    first_tool = Tools(name="Lampu 1")
    second_tool = Tools(name="Lampu 2")
    third_tool = Tools(name="Lampu 3")
    fourth_tool = Tools(name="Motor")
    fifth_tool = Tools(name="Kipas")

    db.session.add_all([first_tool, second_tool, third_tool, fourth_tool, fifth_tool])
    db.session.commit()
    print("All tools created.")


# make command create table of flask
@app.cli.command()
def create_table() -> None:
    """Create tables"""
    db.create_all()
    print("Table created.")


if __name__ == "__main__":
    app.run(debug=True)
