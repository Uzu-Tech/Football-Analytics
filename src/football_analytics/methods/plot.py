import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Sequence, Optional

def line_plot(
    df: pd.DataFrame,
    x_name: str,
    y_name: str,
    category: Optional[str] = None,
    bound_names: Optional[Sequence[str]] = None,
):
    df = pd.DataFrame(df)
    df.sort_values(by=x_name)

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=df,
        x=x_name,
        y=y_name,
        hue=category,
    )

    if (category is not None or bound_names is None):
        return
    
    plt.errorbar(
        df[x_name],
        df[y_name],
        yerr=[
            df[y_name] - df[bound_names[0]],
            df[bound_names[1]] - df[y_name]
        ],
        fmt='none',
        capsize=4,
        alpha=0.5
    )
