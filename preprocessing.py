# fin_hit         (ST003687_SUPPL_Fin-HIT.xlsx)
#   age_sex                          475 × 3
#   anthropometrics                  475 × 5
#   lifestyle                        475 × 3
#   mental_wellbeing                 475 × 4
#   ffq                              475 × 17
#   ffq_codebook                      15 × 6
#   targeted_metabolomics_data       474 × 30
#   untargeted_metabolomics_data     475 × 3599
#   untargeted_compid               3598 × 5
#   microbiome_data                 4862 × 316

import duckdb
import pandas as pd

DB_PATH = ".data/alphaxbio.duckdb"
con = duckdb.connect(DB_PATH)

# schemas = con.execute("SELECT DISTINCT table_schema FROM information_schema.columns WHERE table_schema NOT IN ('information_schema','pg_catalog','main') ORDER BY 1").fetchall()
# for (schema,) in schemas:
#     tables = con.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema='{schema}' ORDER BY table_name").fetchall()
#     print(f'{schema}:')
#     for (t,) in tables:
#         ncols = con.execute(f"SELECT count(*) FROM information_schema.columns WHERE table_schema='{schema}' AND table_name='{t}'").fetchone()[0]
#         nrows = con.execute(f'SELECT count(*) FROM \"{schema}\".\"{t}\"').fetchone()[0]
#         print(f'  {t}: {nrows} rows x {ncols} cols')

# df = con.sql("SELECT * FROM fin_hit.anthropometrics LIMIT 10").fetch_arrow_table().to_pandas()  # via Arrow

df_anthropometrics = con.execute("SELECT * FROM fin_hit.anthropometrics").fetchdf()
df_age_sex = con.execute("SELECT * FROM fin_hit.age_sex").fetchdf()
df_lifestyle = con.execute("SELECT * FROM fin_hit.lifestyle").fetchdf()
df_mental_wellbeing = con.execute("SELECT * FROM fin_hit.mental_wellbeing").fetchdf()
df_ffq = con.execute("SELECT * FROM fin_hit.ffq").fetchdf()
df_ffq_codebook = con.execute("SELECT * FROM fin_hit.ffq_codebook").fetchdf()

df = con.execute("""
    SELECT *
    FROM fin_hit.age_sex
    JOIN fin_hit.anthropometrics USING (Patient_ID)
    JOIN fin_hit.lifestyle USING (Patient_ID)
    JOIN fin_hit.mental_wellbeing USING (Patient_ID)
    JOIN fin_hit.ffq USING (Patient_ID)
""").fetchdf()

con.close()
print(df.columns) 

df[['z-score (RSES)', 'z-score (BodyImage)', 
    'Psychological stress z-score', 'BMIz']].corr()

ffq_cols = [
    "Chocolate_sweets", "Darkbread", "Sweetpastry", "Biscuits_cookies", "Pizza",
    "Hamburger_or_hotdog", "Milk_or_souredmilk", "Icecream", "Cookedvegetables",
    "Fresh_or_gratedvegetables_salad", "Fruit_or_berries", "Juice",
    "Saltysnacks", "Sugarjuicedrink", "Sugarsoftdrink", "Water",
]
df[ffq_cols] = (df[ffq_cols] - df[ffq_cols].mean()) / df[ffq_cols].std()

