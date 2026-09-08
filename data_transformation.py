import re
from pathlib import Path

import duckdb
import pandas as pd

DATA_DIR = Path(".data")
DB_PATH = ".data/alphaxbio.duckdb"

con = duckdb.connect(DB_PATH)
con.execute("CREATE SCHEMA IF NOT EXISTS general")
con.execute("""
    CREATE OR REPLACE TABLE general.studies (
        study VARCHAR, source_file VARCHAR, sheet_name VARCHAR, table_name VARCHAR
    )
""")

for path in sorted(DATA_DIR.glob("*.xlsx")):
    study = re.search(r"SUPPL_(.+)$", path.stem).group(1).lower().replace("-", "_")
    con.execute(f'CREATE SCHEMA IF NOT EXISTS "{study}"')

    for sheet in pd.ExcelFile(path).sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        table = re.sub(r"\W+", "_", sheet.strip().lower()).strip("_")
        con.execute(f'CREATE OR REPLACE TABLE "{study}"."{table}" AS SELECT * FROM df')
        con.execute(
            "INSERT INTO general.studies VALUES (?, ?, ?, ?)",
            [study, path.name, sheet, table],
        )

con.sql("SELECT * FROM general.studies").show()
con.sql("SELECT * FROM fin_hit.anthropometrics limit 10").show()

con.close()



