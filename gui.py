import uuid

import streamlit as st
import pandas as pd
from store.crud import (
    create_motocycle,
    create_user,
    check_user,
    get_motocycles,
    delete_motocycle,
    update_motocycle,
)

# Definición de tabs en la application
tab1, tab2, tab3 = st.tabs(["Register", "Login", "Motocycle"])

# Variable de estado que posteriormente cambiará a True
# cuando se haya registrado o logueado el usuario
if "login" not in st.session_state:
    st.session_state.login = False

with tab1:
    # Tab de Registro de un usuario

    st.header("Registro")

    name = st.text_input("Nombre", key="name")
    last_name = st.text_input("Apellidos")
    date_of_birth = st.text_input(
        "Fecha de nacimiento", placeholder="dd/mm/yyyy"
    )
    phone = st.text_input("Teléfono")
    email = st.text_input("Email", key="register_email")
    password = st.text_input(
        "Password", type="password", key="register_password"
    )

    if tab1.button("Register"):
        st.session_state.login = True
        st.session_state.email = email
        create_user(
            **{
                "uuid": str(uuid.uuid4()),
                "name": name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "phone": phone,
                "email": email,
                "password": password,
            }
        )
        st.write("Registrado!")

with tab2:
    # Tab de Login de un usuario existente

    st.header("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", key="login_password", type="password")
    if tab2.button("Login"):
        if check_user(email=email, password=password):
            st.session_state.login = True
            st.session_state.email = email
            st.write("Logued")
        else:
            st.write("No logueado. Verifique su email/password")

with tab3:
    # Tab de Listado, Creacion, Actualizacion y Borrado de motocicletas

    st.header("Motocicletas")
    if st.session_state.login:
        # Listado de motocicletas
        data = get_motocycles(st.session_state.email)
        num_motocycles = len(data["uuid"])
        datos = {
            **{
                "borrar?": [False] * num_motocycles
                if num_motocycles > 0
                else []
            },
            **data,
        }
        # Populacion de una fila para evitar errores de renderizado
        if num_motocycles == 0:
            for k, v in datos.items():
                if k == "borrar?":
                    datos[k].append(False)
                else:
                    datos[k].append("")

        df = pd.DataFrame(datos)
        edited_df = st.data_editor(
            df,
            column_config={
                "borrar?": st.column_config.CheckboxColumn(
                    "borrar?",
                    help="Borrar?",
                    default=False,
                    required=False,
                ),
                "uuid": "Motocycle id",
                "Marca": "Marca",
                "Cilindrada": "Cilindrada",
                "Año": "Año",
                "Precio": "Precio",
                "Tipo": st.column_config.SelectboxColumn(
                    "Tipo",
                    help="Tipo",
                    width="medium",
                    options=[
                        "Deportiva",
                        "Cross",
                        "Trabajo",
                    ],
                ),
            },
            disabled=["uuid"],
            hide_index=True,
            num_rows="dynamic",
        )
        if tab3.button("Guardar"):
            for index, row in edited_df.iterrows():
                motocycle_update = {
                    "brand": row["Marca"],
                    "capacity": row["Cilindrada"],
                    "year": row["Año"],
                    "price": row["Precio"],
                    "kind": row["Tipo"],
                }
                if row["borrar?"]:
                    # borrado de motocicletas
                    delete_motocycle(row["uuid"])
                else:
                    # update de motocicletas
                    if row["uuid"]:
                        update_motocycle(row["uuid"], **motocycle_update)
                    else:
                        # creacion de motocicletas
                        motocycle_create = {
                            "uuid": str(uuid.uuid4()),
                            **motocycle_update,
                        }
                        create_motocycle(
                            user_email=st.session_state.email,
                            **motocycle_create
                        )
            st.write("Cambios procesados!")
            st.experimental_rerun()

    else:
        st.write("Registrese o Loguese!")
