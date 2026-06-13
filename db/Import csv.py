import pandas as pd
import sqlite3

df = pd.read_csv(r"C:\Users\twierzbowski\Downloads\creditcard.csv")
conn = sqlite3.connect("db_creditcard.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)
conn.close()
print("Gotowe:", len(df), "wierszy")