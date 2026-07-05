"""Ocena ryzyka fraudu dla pojedynczej transakcji z linii poleceń.

Przykład:
    python predict.py --kwota 950 --godzina 3 --kategoria Travel \
        --zagraniczna --niezgodna-lokalizacja --trust 30 --transakcje-24h 6 --wiek 45
"""
import argparse

from fraud_model import CATEGORIES, load_or_train, predict_proba_one


def main():
    p = argparse.ArgumentParser(
        description="Ocena ryzyka oszustwa dla pojedynczej transakcji kartowej.")
    p.add_argument("--kwota", type=float, required=True, help="kwota transakcji")
    p.add_argument("--godzina", type=int, required=True, choices=range(24),
                   metavar="0-23", help="godzina transakcji")
    p.add_argument("--kategoria", choices=CATEGORIES, required=True,
                   help="kategoria sprzedawcy")
    p.add_argument("--zagraniczna", action="store_true",
                   help="transakcja zagraniczna")
    p.add_argument("--niezgodna-lokalizacja", action="store_true",
                   help="lokalizacja niezgodna z profilem klienta")
    p.add_argument("--trust", type=int, required=True, metavar="25-99",
                   help="ocena zaufania urządzenia (25-99)")
    p.add_argument("--transakcje-24h", type=int, required=True, metavar="N",
                   help="liczba transakcji w ostatnich 24 h")
    p.add_argument("--wiek", type=int, required=True, help="wiek posiadacza karty")
    p.add_argument("--prog", type=float, default=0.5,
                   help="próg decyzyjny (domyślnie 0.5)")
    args = p.parse_args()

    print("Wczytywanie modelu (pierwsze uruchomienie trenuje go ~15 s)...")
    model = load_or_train()

    transaction = {
        "amount": args.kwota,
        "transaction_hour": args.godzina,
        "merchant_category": args.kategoria,
        "foreign_transaction": int(args.zagraniczna),
        "location_mismatch": int(args.niezgodna_lokalizacja),
        "device_trust_score": args.trust,
        "velocity_last_24h": args.transakcje_24h,
        "cardholder_age": args.wiek,
    }

    risk = predict_proba_one(model, transaction)
    print(f"\nRyzyko fraudu: {risk:.1%}  (próg decyzyjny: {args.prog:.2f})")
    if risk >= args.prog:
        print("Decyzja: 🚨 PODEJRZANA — skieruj do dodatkowej weryfikacji")
    else:
        print("Decyzja: ✅ transakcja wygląda na prawidłową")


if __name__ == "__main__":
    main()
