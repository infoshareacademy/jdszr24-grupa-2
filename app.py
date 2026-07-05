"""Demo webowe modelu fraud detection (zespół Ocean's Four).

Uruchomienie lokalne:
    streamlit run app.py
"""
import streamlit as st

from fraud_model import CATEGORIES, load_or_train, predict_proba_one

st.set_page_config(page_title="Ocean's Four — wykrywanie fraudów", page_icon="💳")

st.title("💳 Wykrywanie oszustw kartowych")
st.caption("Projekt zaliczeniowy — kurs Data Science jdszr24, zespół Ocean's Four. "
           "Model: skalibrowany las losowy trenowany na 10 000 transakcji.")


@st.cache_resource(show_spinner="Trenowanie modelu przy pierwszym uruchomieniu (~15 s)...")
def get_model():
    return load_or_train()


model = get_model()

with st.sidebar:
    st.header("Ustawienia")
    prog = st.slider("Próg decyzyjny", 0.05, 0.95, 0.50, 0.05,
                     help="Powyżej tego ryzyka transakcja jest oznaczana jako podejrzana. "
                          "Analiza kosztowa w notebooku sugeruje próg niższy niż 0.5.")
    st.markdown("---")
    st.markdown("**Najsilniejsze sygnały fraudu:**\n"
                "- niezgodność lokalizacji\n- transakcja zagraniczna\n"
                "- niski trust score urządzenia\n- wysoka aktywność w 24 h\n"
                "- wysoka kwota, godziny nocne")

st.subheader("Dane transakcji")
col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Kwota transakcji", 0.0, 5000.0, 250.0, 10.0)
    hour = st.slider("Godzina transakcji", 0, 23, 14)
    category = st.selectbox("Kategoria sprzedawcy", CATEGORIES, index=3)
    age = st.slider("Wiek posiadacza karty", 18, 69, 40)
with col2:
    trust = st.slider("Trust score urządzenia", 25, 99, 60,
                      help="Ocena zaufania urządzenia, z którego wykonano transakcję")
    velocity = st.slider("Transakcje w ostatnich 24 h", 0, 9, 2)
    foreign = st.toggle("Transakcja zagraniczna")
    mismatch = st.toggle("Lokalizacja niezgodna z profilem")

if st.button("Oceń ryzyko", type="primary", use_container_width=True):
    # zapamiętujemy transakcję między rerunami Streamlita — dzięki temu wynik
    # nie znika przy ruchu suwakiem progu i przelicza się na żywo
    st.session_state["transaction"] = {
        "amount": amount,
        "transaction_hour": hour,
        "merchant_category": category,
        "foreign_transaction": int(foreign),
        "location_mismatch": int(mismatch),
        "device_trust_score": trust,
        "velocity_last_24h": velocity,
        "cardholder_age": age,
    }

if "transaction" in st.session_state:
    risk = predict_proba_one(model, st.session_state["transaction"])

    st.markdown("---")
    m1, m2 = st.columns(2)
    m1.metric("Ryzyko fraudu", f"{risk:.1%}")
    m2.metric("Próg decyzyjny", f"{prog:.0%}")
    st.progress(min(risk, 1.0))

    if risk >= prog:
        st.error("🚨 **Transakcja podejrzana** — rekomendacja: dodatkowa weryfikacja "
                 "(SMS / potwierdzenie w aplikacji) przed realizacją.")
    else:
        st.success("✅ **Transakcja wygląda na prawidłową** — brak podstaw do blokady.")
