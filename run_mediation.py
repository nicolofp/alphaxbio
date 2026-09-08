import duckdb
import pandas as pd
from cmdstanpy import CmdStanModel

FFQ_COLS = [
    "Chocolate_sweets", "Darkbread", "Sweetpastry", "Biscuits_cookies", "Pizza",
    "Hamburger_or_hotdog", "Milk_or_souredmilk", "Icecream", "Cookedvegetables",
    "Fresh_or_gratedvegetables_salad", "Fruit_or_berries", "Juice",
    "Saltysnacks", "Sugarjuicedrink", "Sugarsoftdrink", "Water",
]

con = duckdb.connect(".data/alphaxbio.duckdb", read_only=True)
df = con.execute("""
    SELECT * FROM fin_hit.anthropometrics
    JOIN fin_hit.mental_wellbeing USING (Patient_ID)
    JOIN fin_hit.ffq USING (Patient_ID)
""").fetchdf()
con.close()

df[FFQ_COLS] = (df[FFQ_COLS] - df[FFQ_COLS].mean()) / df[FFQ_COLS].std()

data = {
    "N": len(df),
    "K": len(FFQ_COLS),
    "X": df[FFQ_COLS].to_numpy(),
    "M1": df["z-score (BodyImage)"].to_numpy(),
    "M2": df["Psychological stress z-score"].to_numpy(),
    "Y": df["BMIz"].to_numpy(),
}

model = CmdStanModel(stan_file="stan_compute/mediation_model.stan")
fit = model.sample(data=data, seed=1, chains=4)

summary = fit.summary()
results = pd.DataFrame({
    "ffq_item": FFQ_COLS,
    "cp": summary.loc[[f"cp[{k+1}]" for k in range(len(FFQ_COLS))], "Mean"].values,
    "ie_bodyimage": summary.loc[[f"ie1[{k+1}]" for k in range(len(FFQ_COLS))], "Mean"].values,
    "ie_stress": summary.loc[[f"ie2[{k+1}]" for k in range(len(FFQ_COLS))], "Mean"].values,
    "total_ie": summary.loc[[f"total_ie[{k+1}]" for k in range(len(FFQ_COLS))], "Mean"].values,
    "prop_mediated": summary.loc[[f"prop_mediated[{k+1}]" for k in range(len(FFQ_COLS))], "Mean"].values,
})
print(results.to_string(index=False))

print(summary.filter(like="prop_mediated", axis=0))