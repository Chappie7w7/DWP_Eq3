from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # Crea las tablas definidas


if __name__ == "__main__":
    app.run(debug=True)
