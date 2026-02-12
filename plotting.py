import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

def plot_maac(df, sector_name, save_path='maac_curve.png'):
    
    df = df.sort_values("MAC_rs_per_tco2")
    
    cumulative = df["annual_abatement_Mt"].cumsum()
    
    fig, ax = plt.subplots(figsize=(12,6))
    
    start = 0
    annotations = []
    # determine label column (prefer 'measure') and assign colors
    label_col = 'measure' if 'measure' in df.columns else None
    if label_col is not None:
        unique_labels = list(df[label_col].astype(str).unique())
        cmap = plt.get_cmap('tab20')
        color_map = {lab: cmap(i % cmap.N) for i, lab in enumerate(unique_labels)}
    else:
        unique_labels = []
        color_map = {}
    
    for i, row in df.iterrows():
        bar_color = None
        if label_col is not None:
            lab = str(row[label_col])
            bar_color = color_map.get(lab)
        ax.bar(
            start,
            row["MAC_rs_per_tco2"],
            width=row["annual_abatement_Mt"],
            align='edge',
            color=bar_color
        )
        # store center x and MAC value for annotation after autoscaling
        center = start + row["annual_abatement_Mt"] / 2.0
        annotations.append((center, row["MAC_rs_per_tco2"]))
        start += row["annual_abatement_Mt"]
    
    ax.set_xlabel("Cumulative Abatement Potential (MtCO2)")
    ax.set_ylabel("Marginal Abatement Cost (₹/tCO2)")
    ax.set_title(f"MAAC Curve - {sector_name}")
    
    plt.axhline(0)

    # add numeric labels above each bar (skip NaN values)
    ax.relim()
    ax.autoscale_view()
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min if (y_max - y_min) != 0 else 1.0
    offset = y_range * 0.02

    for x_center, mac in annotations:
        if mac is None:
            continue
        try:
            mac_val = float(mac)
        except Exception:
            continue
        if np.isnan(mac_val):
            continue
        if mac_val >= 0:
            va = 'bottom'
            y = mac_val + offset
        else:
            va = 'top'
            y = mac_val - offset
        ax.text(x_center, y, f"{mac_val:.1f}", ha='center', va=va, fontsize=8)

    # add legend outside the plot when labels are available
    if unique_labels:
        handles = [mpatches.Patch(color=color_map[lab], label=lab) for lab in unique_labels]
        ax.legend(handles=handles, title='Measure', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")
