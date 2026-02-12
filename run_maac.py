import pandas as pd

from maac_model import MAACModel
from plotting import plot_maac


def main():
    df = pd.read_csv('data/steel_measures.csv')

    model = MAACModel(df, discount_rate=0.1)
    df = model.compute_abatement()
    df = model.compute_mac()

    df_sorted = df.sort_values('MAC_rs_per_tco2')
    df_sorted.to_csv('maac_results.csv', index=False)

    plot_maac(df_sorted, sector_name='Steel', save_path='maac_curve.png')
    print('Wrote maac_results.csv and maac_curve.png')


if __name__ == '__main__':
    main()
