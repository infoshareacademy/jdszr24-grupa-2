# jdszr24-grupa-2 — projekt grupowy Data Science

Projekt grupowy realizowany w ramach kursu Data Science (edycja jdszr24, grupa 2).

## Opis projektu

**Temat: wykrywanie oszustw w transakcjach kartami płatniczymi (fraud detection).**

Zbiór danych: `data/credit_card_fraud_10k.csv` — 10 000 transakcji, 10 kolumn
(kwota, godzina, kategoria sprzedawcy, flagi transakcji zagranicznej i niezgodności
lokalizacji, ocena zaufania urządzenia, liczba transakcji w 24 h, wiek posiadacza karty
oraz zmienna celu `is_fraud`). Klasy są silnie niezbalansowane — oszustwa to **1,5%**
transakcji, dlatego w projekcie stosujemy ważenie klas i metryki odporne na
niezbalansowanie (recall, PR-AUC) zamiast accuracy.

### Przebieg analizy

Cały projekt znajduje się w jednym notebooku **`Ocean's_Four_Project.ipynb`**
(wykresy osadzone w pliku):

1. **Wstępne sprawdzenie danych** — jakość, braki, duplikaty, statystyki opisowe.
2. **EDA** — rozkład klas, rozkłady zmiennych, fraud rate wg cech, korelacje, wnioski.
3. **Przygotowanie danych** *(Sprint 2: DS24G2-11…15)* — selekcja cech (mutual
   information + korelacje), one-hot dla `merchant_category`, cykliczne kodowanie
   sin/cos dla `transaction_hour`, pipeline bez wycieku danych, stratyfikowany
   podział train/test 75/25.
4. **Modelowanie** *(Sprint 2: DS24G2-16…17)* — porównanie strategii obsługi
   niezbalansowania (bez obsługi / `class_weight='balanced'` / undersampling), strojenie
   hiperparametrów (`GridSearchCV`, 5-krotna stratyfikowana CV, metryka average precision),
   ewaluacja, dobór progu decyzyjnego maksymalizującego F1, ważność cech i wnioski biznesowe.

### Wyniki (zbiór testowy, 25% danych)

| Model | Recall | Precision | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| Baseline (dummy) | 0.03 | 0.03 | 0.03 | 0.51 | 0.015 |
| Regresja logistyczna (tuned) | 1.00 | 0.26 | 0.41 | 0.99 | 0.68 |
| **Las losowy (tuned)** | **0.92** | **1.00** | **0.96** | **1.00** | **0.99** |

Las losowy po strojeniu, z progiem dobranym pod maksimum F1, osiąga na zbiorze testowym
recall 0.95 przy precyzji 1.00 (F1 = 0.97) — wynik bliski ideału, bo dane są syntetyczne
i zawierają niemal deterministyczną regułę fraudu (na rzeczywistych danych transakcyjnych
wyniki byłyby niższe). Najsilniejsze sygnały oszustwa:
niezgodność lokalizacji, transakcja zagraniczna, niski trust score urządzenia,
wysoka aktywność w 24 h i wysoka kwota. Wykresy — w notebooku.

## Zespół

| Imię i nazwisko | GitHub |
|---|---|
| Tomasz Wierzbowski | [@TomaszWu14](https://github.com/TomaszWu14) |
| Kuba Kaczmarczyk | [@kubamkaczmarczyk](https://github.com/kubamkaczmarczyk) |
| Aleksandra Michalska | [@AMIAleksandra](https://github.com/AMIAleksandra) |

## Struktura repozytorium

```
├── Ocean's_Four_Project.ipynb   # cały projekt: EDA, przygotowanie danych, modele
├── data/
│   └── credit_card_fraud_10k.csv
├── requirements.txt
└── README.md
```

Katalog `data/processed/` (podzielone zbiory train/test) tworzy się przy uruchomieniu
notebooka i jest ignorowany przez git.

## Uruchomienie środowiska

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

> Jeśli aktywacja zgłosi błąd o „execution policy", wykonaj raz
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` i spróbuj ponownie.
> Po aktywacji prompt zaczyna się od `(.venv)` — upewnij się, że nie masz aktywnego
> środowiska innego projektu (w razie czego najpierw `deactivate`).

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Zasady współpracy

1. **Nie pracujemy bezpośrednio na `main`** — każdy tworzy własną gałąź (np. `eda-tomasz`, `model-ania`).
2. Zmiany trafiają do `main` przez **pull request** — najlepiej z krótkim review drugiej osoby.
3. Duże pliki danych trzymamy poza gitem — w repo jest tylko mały zbiór projektowy `data/credit_card_fraud_10k.csv`.
4. Przed rozpoczęciem pracy: `git pull origin main`, żeby mieć aktualny stan.
