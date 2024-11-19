# run.py
from ks import create_app  # Импортируем из пакета ks

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

