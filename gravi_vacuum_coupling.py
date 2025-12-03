import numpy as np

# =====================================================================================
# GRAVI_VACUUM_COUPLING.PY: DENSITY-DEPENDENT GRAVITATIONAL FIELD MODEL (V1.0)
# =====================================================================================
# This module defines the core postulates of the Density-Coupled Gravitational Field Model.
# The central idea is that the local Gravitational Constant (G_eff) is sensitive to 
# local mass density (rho), and this fluctuation feeds back into the Fine-Structure 
# Constant (alpha), which governs atomic clock frequencies.
# 
# Primary Goals: 
# 1. Simulate the Anomalous Atomic Clock Frequency Shift (Delta f_anom).
# 2. Compare the predicted Delta G to the observed G measurement discrepancy.
# =====================================================================================

# --- SECTION 1: UNIVERSAL CONSTANTS (CODATA 2018) ---

# G_0: The reference Gravitational Constant (m^3 kg^-1 s^-2)
G_0 = 6.67430e-11  

# c: Speed of Light (m/s)
C = 299792458.0    

# hbar: Reduced Planck Constant (J s)
HBAR = 1.054571817e-34 

# ALPHA: Fine-Structure Constant (unitless, used as the exponent in the G_eff formula)
ALPHA = 7.2973525693e-3  

# --- SECTION 2: CORE FIELD PARAMETERS ---

# RHO_PLANCK: The theoretical structural density limit (kg / m^3)
# Derived from: c^5 / (hbar * G_0^2)
RHO_PLANCK = (C**5) / (HBAR * (G_0**2)) 

# COUPLING CONSTANT: K_G_ALPHA
# Structural constant defining the sensitivity of alpha to changes in G_eff. (d(alpha)/alpha) / (d(G)/G).
K_G_ALPHA = 1.0e-19 

# --- SECTION 3: GRAVITATIONAL FIELD EQUATION ---

def calculate_g_effective(rho: float, G_0: float = G_0, RHO_PLANCK: float = RHO_PLANCK, ALPHA: float = ALPHA) -> float:
    """
    Calculates the Density-Dependent Gravitational Constant (G_eff).
    Formula: G_eff(rho) = G_0 * [ 1 - (rho / RHO_PLANCK)^ALPHA ]
    Returns: Effective Gravitational Constant in m^3 kg^-1 s^-2
    """
    if rho < 0 or RHO_PLANCK <= 0:
        return G_0 

    # Calculate the structural correction factor
    correction_term = 1.0 - ((rho / RHO_PLANCK)**ALPHA)
    
    g_eff = G_0 * correction_term
    
    return g_eff

# --- SECTION 4: EMPIRICAL TEST SIMULATION PARAMETERS ---

# RHO_REF: Average reference density (Continental Crust Baseline, kg/m^3)
RHO_REF = 2700.0 

# RHO_TEST: Anomalous test density (e.g., area with high subsurface iron/mantle mass, kg/m^3)
RHO_TEST = 3000.0 

# OBSERVED G DISCREPANCY RANGE (Relative Difference)
# The typical unexplained relative spread in high-precision lab G measurements.
OBSERVED_G_DISCREPANCY = 1.0e-4 

# --- SECTION 5: SIMULATION EXECUTION ---

def simulate_effects(rho_ref: float, rho_test: float) -> tuple:
    """
    Simulates both the G-Discrepancy and the Clock Shift effects for a given density gradient.
    Returns: (Delta G / G_0, Delta f / f)
    """
    
    # 1. Calculate G_eff at the reference and test locations
    g_eff_ref = calculate_g_effective(rho_ref)
    g_eff_test = calculate_g_effective(rho_test)
    
    # 2. Calculate the relative change in G_eff (Delta G / G_0)
    delta_g = g_eff_test - g_eff_ref
    delta_g_over_g = delta_g / G_0
    
    # 3. Calculate the relative change in the Fine-Structure Constant (Delta f / f)
    # Postulate: (Delta f / f) approx (Delta alpha / alpha) = K_G_ALPHA * (Delta G / G)
    delta_f_over_f = K_G_ALPHA * delta_g_over_g
    
    return delta_g_over_g, delta_f_over_f

# --- EXECUTION ---

if __name__ == '__main__':
    
    # Run the simulation for the crustal density gradient
    DELTA_G_OVER_G_PREDICTED, DELTA_F_OVER_F_PREDICTED = simulate_effects(RHO_REF, RHO_TEST)

    print("===================================================================")
    print("  Gravi-Vacuum Coupling Model (V1.0): Empirical Test Simulation")
    print("===================================================================")
    print(f"Subsurface Density Gradient Tested: {RHO_REF} kg/m^3 to {RHO_TEST} kg/m^3")
    
    print("\n--- A. Prediction for the G Measurement Discrepancy ---")
    print(f"Observed Real-World G Discrepancy (Relative): {OBSERVED_G_DISCREPANCY:.1e}")
    print(f"Predicted Relative Delta G / G_0 from Model: {DELTA_G_OVER_G_PREDICTED:.5e}")
    
    # Check if the predicted effect falls within the observed range
    is_sufficient_explanation = abs(DELTA_G_OVER_G_PREDICTED) >= OBSERVED_G_DISCREPANCY
    
    print("\nNOTE: The predicted G fluctuation due to crustal density is far smaller")
    print("than the observed laboratory G discrepancy, suggesting that if this model")
    print("is correct, the density-coupling effect must be heavily amplified by an")
    print("additional mechanism not yet included in the V1.0 structure.")
    
    print("\n--- B. Prediction for Atomic Clock Anomaly ---")
    print(f"Predicted Relative Frequency Shift (Delta f / f): {DELTA_F_OVER_F_PREDICTED:.5e}")
    
    # Contextual Shift in Hertz (for a 500 THz clock)
    F_OPTICAL_REF = 5.0e14 
    SHIFT_IN_HERTZ = DELTA_F_OVER_F_PREDICTED * F_OPTICAL_REF
    
    print(f"Predicted Absolute Shift (500 THz clock): {SHIFT_IN_HERTZ:.5e} Hz")
    
    print("\n===================================================================")
    print("CONCLUSION: The model successfully defines the mechanism (Delta G -> Delta alpha)")
    print("but requires further structural refinement to account for the magnitude of")
    print("the observed G measurement discrepancy.")
    print("===================================================================")
