from app import app, db
from app.database import Words, Dictionaries, Users, mistakes


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Words': Words,
            'Dictionaries': Dictionaries,
            'Users': Users,
            'mistakes': mistakes}


if __name__ == '__main__':
    app.run()
