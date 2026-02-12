import pandas as pd
import numpy as np

class MAACModel:
    
    def __init__(self, df, discount_rate=0.1):
        self.df = df.copy()
        self.r = discount_rate
        
    def capital_recovery_factor(self, n):
        r = self.r
        # handle scalar or array-like `n` (pd.Series, list, np.array)
        import numpy as _np
        if hasattr(n, 'values'):
            n_index = getattr(n, 'index', None)
            n_arr = n.values.astype(float)
            crf_arr = (r * _np.power(1+r, n_arr)) / (_np.power(1+r, n_arr) - 1)
            if n_index is not None:
                import pandas as _pd
                return _pd.Series(crf_arr, index=n_index)
            return crf_arr
        else:
            n_val = float(n)
            return (r * (1+r)**n_val) / ((1+r)**n_val - 1)
    
    def compute_abatement(self):
        self.df["emission_reduction"] = (
            self.df["emission_baseline_tco2_per_t"] -
            self.df["emission_new_tco2_per_t"]
        )
        
        self.df["annual_abatement_Mt"] = (
            self.df["emission_reduction"] *
            self.df["annual_production_t"] *
            self.df["adoption_potential_%"] / 100
        ) / 1e6
        
        return self.df
    
    def compute_mac(self):
        crf = self.capital_recovery_factor(self.df["lifetime"])
        
        self.df["annualized_capex"] = (
            self.df["capex_rs_per_t_capacity"] * crf
        )
        
        self.df["incremental_cost_per_t"] = (
            self.df["annualized_capex"] +
            self.df["opex_rs_per_t"]
        )
        
        self.df["MAC_rs_per_tco2"] = (
            self.df["incremental_cost_per_t"] /
            self.df["emission_reduction"]
        )
        # guard against division by zero or very small reductions
        self.df.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.df.loc[self.df['emission_reduction'] == 0, 'MAC_rs_per_tco2'] = np.nan

        return self.df
