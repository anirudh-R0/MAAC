import matplotlib.pyplot as plt
import numpy as np

def plot_maac(df, sector_name, save_path='maac_curve.png'):
    
    df = df.sort_values("MAC_rs_per_tco2")
    
    cumulative = df["annual_abatement_Mt"].cumsum()
    
    fig, ax = plt.subplots(figsize=(12,6))
    
    start = 0
    
    for i, row in df.iterrows():
        ax.bar(
            start,
            row["MAC_rs_per_tco2"],
            width=row["annual_abatement_Mt"],
            align='edge'
        )
        start += row["annual_abatement_Mt"]
    
    ax.set_xlabel("Cumulative Abatement Potential (MtCO2)")
    ax.set_ylabel("Marginal Abatement Cost (₹/tCO2)")
    ax.set_title(f"MAAC Curve - {sector_name}")
    
    plt.axhline(0)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")
