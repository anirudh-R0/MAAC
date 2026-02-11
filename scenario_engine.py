from maac_model import MAACModel

def run_sensitivity(df, discount_rates=[0.08, 0.1, 0.12]):
    
    results = {}
    
    for r in discount_rates:
        model = MAACModel(df, discount_rate=r)
        model.compute_abatement()
        model.compute_mac()
        results[r] = model.df
        
    return results
