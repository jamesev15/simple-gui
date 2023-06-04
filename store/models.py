from os.path import abspath, dirname, join

from sqlalchemy.orm import relationship
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

app = Flask(__name__)

db_path = join(dirname(abspath(__file__)), "instance/", "app.db")
DATABASE_URL = f"sqlite:///{db_path}"  # Ubicación de la base de datos

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BaseModel(db.Model):
    __abstract__ = True
    uuid = db.Column(db.String, primary_key=True)


class UserModel(BaseModel):
    """Tabla de usuarios"""

    __tablename__ = "User"

    name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    phone = db.Column(db.String)

    email = db.Column(db.String)
    password = db.Column(db.String)

    motocycles = relationship(
        "MotocycleModel", back_populates="user", passive_deletes=True
    )


class MotocycleModel(BaseModel):
    """Tabla de motocicletas"""

    __tablename__ = "Motocycle"

    brand = db.Column(db.String)
    capacity = db.Column(db.String)
    year = db.Column(db.String)
    price = db.Column(db.String)
    kind = db.Column(db.String)

    # Relacion de 1 a N entre la tabla usarios y la tabla motocicletas
    user_id = db.Column(
        db.String,
        db.ForeignKey(
            f"{UserModel.__tablename__}.uuid",
            ondelete="CASCADE",
        ),
    )

    user = relationship(UserModel, back_populates="motocycles")


def run_migrations():
    """Funcion para ejecutar las migraciones creadas por alembic"""
    with app.app_context():
        upgrade(directory=join(dirname(abspath(__file__)), "migrations/"))
