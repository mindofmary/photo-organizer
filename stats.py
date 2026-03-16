import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def gerar_estatisticas(folder):

    data = []

    for p in Path(folder).iterdir():

        if p.is_dir():

            count = len(list(p.iterdir()))

            data.append({
                "mes":p.name,
                "ficheiros":count
            })

    df = pd.DataFrame(data)

    df = df.sort_values("mes")

    plt.bar(df["mes"],df["ficheiros"])

    plt.xticks(rotation=45)

    plt.title("Fotos por mês")

    plt.tight_layout()

    plt.show()