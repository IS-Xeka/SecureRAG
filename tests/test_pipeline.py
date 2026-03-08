import pandas as pd
from main import secure_rag

df = pd.read_csv("tests/test_queries.csv")

for _, row in df.iterrows():

    query = row["query"]

    result = secure_rag(query)

    print("\nQuery:", query)
    print("Result:", result)