"""Demo modelu fraud detection (zespół Ocean's Four).

Uruchomienie:
    streamlit run app.py
"""
import streamlit as st

from fraud_model import CATEGORIES, load_or_train, predict_proba_one

st.title("💳 Wykrywanie oszustw kartowych")


@st.cache_resource(show_spinner="Przygotowanie modelu (pierwszy raz ~1 min)...")
def get_model():
    return load_or_train()


model = get_model()

amount = st.number_input("Kwota transakcji", 0.0, 5000.0, 250.0, 10.0)
hour = st.slider("Godzina transakcji", 0, 23, 14)
category = st.selectbox("Kategoria sprzedawcy", CATEGORIES)
trust = st.slider("Trust score urządzenia", 25, 99, 60)
velocity = st.slider("Transakcje w ostatnich 24 h", 0, 9, 2)
age = st.slider("Wiek posiadacza karty", 18, 69, 40)
foreign = st.checkbox("Transakcja zagraniczna")
mismatch = st.checkbox("Lokalizacja niezgodna z profilem")

if st.button("Oceń ryzyko", type="primary"):
    risk = predict_proba_one(model, {
        "amount": amount,
        "transaction_hour": hour,
        "merchant_category": category,
        "foreign_transaction": int(foreign),
        "location_mismatch": int(mismatch),
        "device_trust_score": trust,
        "velocity_last_24h": velocity,
        "cardholder_age": age,
    })
    st.metric("Ryzyko fraudu", f"{risk:.1%}")
    if risk >= 0.5:
        st.error("🚨 Transakcja podejrzana — skieruj do dodatkowej weryfikacji.")
    else:
        st.success("✅ Transakcja wygląda na prawidłową.")
