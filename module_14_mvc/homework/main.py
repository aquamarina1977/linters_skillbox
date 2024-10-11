from routes import app
from models import init_db, DATA

if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
