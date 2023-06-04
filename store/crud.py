from sqlalchemy.orm import Session
from store.models import UserModel, MotocycleModel
from store.base import connect
import pandas as pd


def get_user(email: str):
    """Funcion para obtener un usuario en base al email"""
    with Session(connect()) as db:
        return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(**kwargs):
    """Funcion para crear un usuario"""
    with Session(connect()) as db:
        user = UserModel(**kwargs)
        db.add(user)
        db.commit()


def check_user(email: str, password: str):
    """Funcion para verificar el email y password en el login"""
    with Session(connect()) as db:
        return (
            db.query(UserModel)
            .filter(UserModel.email == email, UserModel.password == password)
            .first()
        )


def create_motocycle(user_email: str, **kwargs):
    """Funcion para crear una motocicleta para un usuario"""
    with Session(connect()) as db:
        user = get_user(email=user_email)
        if not user:
            raise ValueError("User not defined")

        motocycle = MotocycleModel(user_id=user.uuid, **kwargs)
        db.add(motocycle)
        db.commit()


def get_motocycles(user_email: str):
    """Funcion para obtener motocicletas en base al email de un usuario"""
    user = get_user(email=user_email)
    if not user:
        raise ValueError("User not defined")

    motocycles_data = {
        "Marca": [],
        "Cilindrada": [],
        "Año": [],
        "Precio": [],
        "Tipo": [],
        "uuid": [],
    }
    with Session(connect()) as db:
        for motocycle in (
            db.query(MotocycleModel)
            .filter(MotocycleModel.user_id == user.uuid)
            .all()
        ):
            motocycles_data["uuid"].append(motocycle.uuid)
            motocycles_data["Marca"].append(motocycle.brand)
            motocycles_data["Cilindrada"].append(motocycle.capacity)
            motocycles_data["Año"].append(motocycle.year)
            motocycles_data["Precio"].append(motocycle.price)
            motocycles_data["Tipo"].append(motocycle.kind)

    return motocycles_data


def delete_motocycle(motocycle_uuid: str) -> bool:
    """Funcion para borrar una motocicleta"""
    with Session(connect()) as db:
        motocycle = (
            db.query(MotocycleModel)
            .filter(
                MotocycleModel.uuid == motocycle_uuid,
            )
            .first()
        )
        if motocycle:
            db.delete(motocycle)
            db.commit()
            return True
        return False


def update_motocycle(motocycle_uuid: str, **kwargs):
    """Funcion para actualizar una motocicleta"""
    with Session(connect()) as db:
        db.query(MotocycleModel).filter(
            MotocycleModel.uuid == motocycle_uuid
        ).update(
            {
                MotocycleModel.brand: kwargs.get("brand", ""),
                MotocycleModel.capacity: kwargs.get("capacity", ""),
                MotocycleModel.year: kwargs.get("year", ""),
                MotocycleModel.price: kwargs.get("price", ""),
                MotocycleModel.kind: kwargs.get("kind", ""),
            }
        )
        db.commit()
