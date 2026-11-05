
import os
import streamlit as st
import httpx

API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

st.title("Fredagsbaren")

# Vis succesbesked efter en handling
if "message" in st.session_state:
    st.success(st.session_state.pop("message"))

# Brugerens navn gemmes i session_state
name = st.sidebar.text_input("Dit navn", key="name")

# Hent alle events fra API'et
try:
    response = httpx.get(f"{API_URL}/events", timeout=2)
    events = response.json()

except httpx.ConnectError:
    st.error("API'en kører ikke. Start Flask API'et igen.")
    st.stop()

except httpx.TimeoutException:
    st.error("API'et svarer for langsomt. Prøv igen senere.")
    st.stop()

# Lav en oversigt over events
event_overview = []

for event in events:
    event_overview.append({
        "Titel": event["title"],
        "Dato": event["date"],
        "Antal tilmeldte": len(event["participants"]),
        "Ledige pladser": event["capacity"] - len(event["participants"])
    })

# Vis eventlisten som en tabel
st.dataframe(event_overview)

# Vælg event
if events:
    selected_event = st.selectbox(
        "Vælg event",
        events,
        format_func=lambda event: event["title"]
    )

    # Vis deltagere
    st.write("Deltagere:", selected_event["participants"])

    # Beregn ledige pladser
    ledige_pladser = selected_event["capacity"] - len(selected_event["participants"])

    # Tilmeld
    if st.button("Tilmeld", disabled=ledige_pladser <= 0):
    #if st.button("Tilmeld"):
        if not name.strip():
            st.warning("Du skal indtaste dit navn først.")

        else:
            try:
                response = httpx.post(
                    f"{API_URL}/events/{selected_event['id']}/signups",
                    json={"name": name.strip()}
                )

                response.raise_for_status()

                st.session_state["message"] = "Du er nu tilmeldt!"
                st.rerun()

            except httpx.HTTPStatusError as e:
                error_message = e.response.json()["error"]
                st.error(error_message)

    # Afmeld
    if st.button("Afmeld"):
        if not name.strip():
            st.warning("Du skal indtaste dit navn først.")

        else:
            response = httpx.delete(
                f"{API_URL}/events/{selected_event['id']}/signups/{name.strip()}"
            )

            if response.status_code == 204:
                st.session_state["message"] = "Du er nu afmeldt!"
                st.rerun()
            else:
                st.error("Afmeldingen kunne ikke gennemføres.")

else:
    st.info("Der er ingen events endnu.")

# Opret nyt event
st.subheader("Opret nyt event")

with st.form("create_event"):
    title = st.text_input("Eventets titel")

    date = st.date_input("Dato")

    capacity = st.number_input(
        "Antal pladser",
        min_value=1,
        value=10
    )

    submitted = st.form_submit_button("Opret event")

    if submitted:
        response = httpx.post(
            f"{API_URL}/events",
            json={
                "title": title,
                "date": date.isoformat(),
                "capacity": capacity
            }
        )

        if response.status_code == 201:
            st.session_state["message"] = "Eventet er oprettet!"
            st.rerun()
        else:
            st.error(response.json())
