import pandas as pd
import numpy as np

class MAACModel:
    
    def __init__(self, df, discount_rate=0.1):
        self.df = df.copy()
        self.r = discount_rate
        
    def capital_recovery_factor(self, n):
        r = self.r
        return (r * (1+r)**n) / ((1+r)**n - 1)
    
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
        
        return self.df
