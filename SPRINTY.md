# Plan sprintów projektu — wykrywanie oszustw kartowych (Ocean's Four)

Dokument opisuje wszystkie sprinty projektu zaliczeniowego: zakres zadań, kryteria
akceptacji, status wykonania i miejsce realizacji (sekcje notebooka
`Ocean's_Four_Project.ipynb` lub pliki w repo).

**Legenda statusów:** ✅ zrobione · 🔶 w trakcie / do decyzji zespołu · ⬜ do zrobienia

---

## Sprint 1 — Start projektu, dane i eksploracja

| Zadanie | Opis | Status | Gdzie |
|---|---|---|---|
| Wybór tematu i zbioru danych | Temat: wykrywanie oszustw w transakcjach kartowych. Zbiór: Credit Card Fraud Detection (Kaggle, wersja 10 tys. transakcji). | ✅ | README, sekcja wstępna notebooka |
| Konfiguracja repozytorium | Struktura repo, `.gitignore`, `requirements.txt`, zasady współpracy (gałąź per osoba → PR → review). | ✅ | README |
| Wstępne sprawdzenie danych | Rozmiar, typy, braki danych, duplikaty, statystyki opisowe; usunięcie `transaction_id`. | ✅ | notebook, sekcja 3 |
| Eksploracyjna analiza danych (EDA) | Rozkład klas (1,5% fraudów), rozkłady zmiennych, fraud rate wg cech (kategoria, godzina, transakcje zagraniczne, lokalizacja), korelacje, wnioski. | ✅ | notebook, sekcje 4.1–4.7 |

---

## Sprint 2 — Przygotowanie danych i pierwsze modele (DS24G2-11…17)

| Zadanie | Opis | Kryteria akceptacji | Status | Gdzie |
|---|---|---|---|---|
| DS24G2-11 Selekcja cech | Ocena przydatności cech korelacją z celem i informacją wzajemną (mutual information). | Ranking cech w notebooku; decyzja co zostaje/wypada z uzasadnieniem. | ✅ | sekcja 5.1 |
| DS24G2-12 Kodowanie `merchant_category` | One-hot encoding zmiennej nominalnej (`OneHotEncoder`, `drop='first'` przeciw współliniowości). | Pokazane kategorie i kolumny po zakodowaniu; uzasadnienie wyboru metody. | ✅ | sekcja 5.2 |
| DS24G2-13 Transformacja `transaction_hour` | Cykliczne kodowanie godziny parą sin/cos (23:00 i 0:00 mają być „blisko siebie"). | Wizualizacja godziny na okręgu + fraud rate wg godziny; wzór w notebooku. | ✅ | sekcja 5.3 |
| DS24G2-14 Przygotowanie danych do uczenia | Jeden `ColumnTransformer` (one-hot + sin/cos + standaryzacja) uczony tylko na zbiorze treningowym — bez wycieku danych. | Podgląd danych po transformacji; transformer używany w pipeline'ach modeli. | ✅ | sekcja 5.4 |
| DS24G2-15 Podział train/test | Stratyfikowany podział 75/25 po `is_fraud`. | Identyczny fraud rate w train i test; zapis do `data/processed/`. | ✅ | sekcja 5.5 |
| DS24G2-16 Trenowanie i strojenie modeli | Modele: baseline (dummy), regresja logistyczna, las losowy; strojenie `GridSearchCV`. | Najlepsze parametry wypisane; wynik CV podany. | ✅ | sekcja 6.2 |
| DS24G2-17 Obsługa niezbalansowanych danych | Porównanie strategii: bez obsługi / `class_weight='balanced'` / undersampling 1:1, dla obu modeli. | Tabela porównawcza metryk; decyzja o strategii z uzasadnieniem (wybrano ważenie klas). | ✅ | sekcja 6.1 |

---

## Sprint 3 — Ewaluacja i interpretacja modeli

| Zadanie | Opis | Kryteria akceptacji | Status | Gdzie |
|---|---|---|---|---|
| Strojenie hiperparametrów z walidacją krzyżową | `GridSearchCV` dla regresji logistycznej (C) i lasu losowego (n_estimators, max_depth, min_samples_leaf); 5-krotna stratyfikowana CV, metryka average precision. | Siatki parametrów zdefiniowane; najlepsze parametry i wynik CV w notebooku. | ✅ | sekcja 6.2 |
| Ewaluacja metrykami dla klas niezbalansowanych | Porównanie modeli na zbiorze testowym: recall, precision, F1, ROC-AUC, PR-AUC; uzasadnienie, czemu nie accuracy. | Tabela zbiorcza; wskazany najlepszy model wg PR-AUC. | ✅ | sekcja 6.3 |
| Macierze pomyłek oraz krzywe ROC i precision-recall | Wizualizacja jakości klasyfikacji wszystkich modeli; na krzywej PR zaznaczony poziom baseline. | Wykresy w notebooku z komentarzem interpretującym. | ✅ | sekcja 6.3 |
| Dobór progu decyzyjnego | Analiza kompromisu precision–recall w funkcji progu; wybór progu maksymalizującego F1. | Wybrany próg z uzasadnieniem; classification report i macierz pomyłek po zmianie progu. | ✅ | sekcja 6.4 (oraz 6.8 — wariant kosztowy) |
| Analiza ważności cech i interpretacja modelu | Ważność cech lasu losowego + współczynniki regresji logistycznej; porównanie rankingów i zgodność z EDA. | Wykres ważności; lista najsilniejszych sygnałów fraudu. | ✅ | sekcja 6.5 |
| *(nadprogram)* Porównanie z XGBoost | Gradient boosting z `scale_pos_weight`; porównanie z tuned lasem losowym. | Wiersz w tabeli metryk; wniosek, który model zostaje. | ✅ | sekcja 6.6 |
| *(nadprogram)* Kalibracja prawdopodobieństw | Kalibracja Platta (sigmoid, 5-CV); krzywa kalibracji i Brier score przed/po (0.0046 → 0.0011). | Wykres kalibracji; poprawa Brier score wykazana. | ✅ | sekcja 6.7 |
| *(nadprogram)* Analiza kosztowa progu | Koszt FN = średnia kwota fraudu (216 zł), koszt FP = 5 zł (weryfikacja); krzywa kosztu vs próg, próg kosztowo-optymalny vs F1 vs 0.5. | Wykres kosztu; rekomendacja progu dla biznesu. | ✅ | sekcja 6.8 |

---

## Sprint 4 — Finalizacja i prezentacja wyników

| Zadanie | Opis | Kryteria akceptacji | Status | Gdzie |
|---|---|---|---|---|
| Wybór modelu finalnego i walidacja końcowa | Model finalny: skalibrowany las losowy (parametry z GridSearchCV) + próg wg analizy kosztowej/F1. Pełna powtarzalność (random_state=42, `requirements.txt`). | Jednoznacznie wskazany model z kompletem metryk; notebook wykonuje się od początku do końca na czystym środowisku. | ✅ | sekcje 6.3–6.8, 7 |
| Wnioski biznesowe i rekomendacje | Rekomendacje w języku biznesowym: kiedy kierować transakcję do weryfikacji, jak przesuwać próg, ograniczenia modelu (dane syntetyczne). | Min. 3 konkretne rekomendacje; opisane ograniczenia. | ✅ | sekcja 7 |
| Raport końcowy — README | Opis problemu i zbioru, przebieg analizy, tabela wyników, instrukcja środowiska i demo. | README czytelne dla osoby spoza zespołu; instrukcje działają. | ✅ | README |
| Demo predykcji | Ocena ryzyka pojedynczej transakcji: CLI (`predict.py`) i aplikacja webowa (`streamlit run app.py`) z suwakiem progu. | Oba dema działają lokalnie po `pip install -r requirements.txt`. | ✅ | `predict.py`, `app.py`, `fraud_model.py` |
| Prezentacja na zaliczenie | 10–15 slajdów: problem i dane → EDA → przygotowanie danych → modele i metryki → próg/koszty → demo → wnioski. Podział ról na 3 osoby. | Slajdy gotowe i przećwiczone; każdy omawia swój fragment. | ⬜ | — |
| Porządki końcowe i review | Merge gałęzi `Tomasz_Wierzbowski` do `main` repo grupy po review Kuby i Aleksandry; decyzja zespołu co do pliku `creditcard.csv` (duży, do usunięcia z gita?). | Wszystko na `main` przez PR z review; brak zbędnych plików. | 🔶 | repo grupy |

---

## Stan projektu w skrócie

- **Zrobione:** dane + EDA, pełne przygotowanie danych, modele ze strojeniem i obsługą
  niezbalansowania, ewaluacja z doborem progu (w tym kosztowym), kalibracja, XGBoost,
  dema CLI + Streamlit, dokumentacja.
- **Do zrobienia:** prezentacja na zaliczenie, merge do `main` repo grupy po review,
  zamknięcie zadań w Jirze (odnośniki do sekcji notebooka są w tabelach powyżej).
