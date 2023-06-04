import uuid
from sqlalchemy.orm import Session

from store.base import connect
from store.crud import (
    get_user,
    create_user,
    check_user,
    create_motocycle,
    get_motocycles,
)

with Session(connect()) as session:
    user = get_user(session, email="james@gmail.com")

    if not user:
        user_info = {
            "uuid": str(uuid.uuid4()),
            "name": "james",
            "last_name": "espichan vilca",
            "date_of_birth": "15/02/1994",
            "phone": "940410178",
            "email": "james@gmail.com",
            "password": "jamesev",
        }
        create_user(session, **user_info)
    else:
        # user = check_user(session, email="james@gmail.com", password="jamesev")
        # if user:
        #     motocycle_info = {
        #         "uuid": str(uuid.uuid4()),
        #         "brand": "Martin",
        #         "capacity": "103",
        #         "year": "2023",
        #         "price": "20000",
        #         "kind": "B",
        #     }
        #     create_motocycle(
        #         session, user_email="james@gmail.com", **motocycle_info
        #     )
        motocycles = get_motocycles(db=session, user_email="james@gmail.com")
