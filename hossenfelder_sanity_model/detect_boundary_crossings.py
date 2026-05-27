import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

def detect_symmetry_boundary(csv_path="hossenfelder_sanity_model/cern_conformal_data.csv", plot_path="hossenfelder_sanity_model/conformal_symmetry_breaking.png"):
    print("=============================================================")
    print("   CONFORMAL SYMMETRY BOUNDARY CROSSING DETECTOR")
    print("   Kolmogorov-Smirnov Statistical Testing for 2T-Physics")
    print("=============================================================\n")

    if not os.path.exists(csv_path):
        print(f"Error: Conformal data file not found at {csv_path}. Please run cern_data_miner.py first.")
        return

    # Load simulated data
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} scattering events.")

    # Define energy bins
    bins = [50, 150, 250, 350, 450, 1000]
    bin_labels = ["50-150 GeV", "150-250 GeV", "250-350 GeV", "350-450 GeV", "450+ GeV"]
    
    df['energy_bin'] = pd.cut(df['energy_gev'], bins=bins, labels=bin_labels)

    # Theoretical Conformal Null Hypothesis Distribution
    # Under conformal symmetry, R ~ N(1.0, 0.05)
    mu_null = 1.0
    sigma_null = 0.05
    
    print("Performing Kolmogorov-Smirnov (KS) Test for conformal symmetry H0: R ~ N(1.0, 0.05^2)")
    print(f"{'Energy Bin':<15} | {'Mean R':<8} | {'Std Dev R':<10} | {'KS Stat':<8} | {'p-value':<10} | {'Status'}")
    print("-" * 75)

    detected_boundary_bin = None
    
    plt.figure(figsize=(10, 6))

    for label in bin_labels:
        bin_data = df[df['energy_bin'] == label]['cross_ratio'].values
        if len(bin_data) == 0:
            continue
            
        # Run KS test comparing empirical distribution with normal cdf
        ks_stat, p_val = stats.ks_1samp(bin_data, stats.norm(loc=mu_null, scale=sigma_null).cdf)
        
        mean_r = np.mean(bin_data)
        std_r = np.std(bin_data)
        
        # If p-value < 0.05, conformal H0 is rejected (Symmetry is broken)
        is_symmetry_broken = p_val < 0.05
        status = "BROKEN (Lorentz Phase)" if is_symmetry_broken else "PRESERVED (Conformal Phase)"
        
        if is_symmetry_broken and detected_boundary_bin is None:
            # First energy bin where symmetry is broken from high to low energy
            # Since bins are ordered from low to high:
            # We look for the boundary where it shifts.
            pass

        print(f"{label:<15} | {mean_r:.3f}   | {std_r:.3f}     | {ks_stat:.4f}  | {p_val:.4e} | {status}")
        
        # Plot distribution
        plt.hist(bin_data, bins=50, alpha=0.5, label=f"{label} (p={p_val:.2e})", density=True)

    # Calculate exact boundary by sliding a window of energy
    # We find where p-value transitions below 0.05
    energy_levels = np.linspace(100, 500, 20)
    p_values = []
    
    for E_thresh in energy_levels:
        # Check window centered at E_thresh
        window_data = df[abs(df['energy_gev'] - E_thresh) < 25.0]['cross_ratio'].values
        if len(window_data) > 50:
            _, p_val = stats.ks_1samp(window_data, stats.norm(loc=mu_null, scale=sigma_null).cdf)
            p_values.append(p_val)
        else:
            p_values.append(0.0)
            
    # Find transition point (where p-value crosses 0.05)
    transition_idx = np.where(np.array(p_values) > 0.05)[0]
    if len(transition_idx) > 0:
        E_boundary = energy_levels[transition_idx[0]]
        print(f"\n[ANALYSIS] Critical boundary transition detected at energy: {E_boundary:.1f} GeV")
        print("   Above this scale, conformal symmetry H0 cannot be rejected (Conformal Phase).")
        print("   Below this scale, massive standard model particles break conformal symmetry (Lorentz Phase).")
    else:
        print("\n[ANALYSIS] No clear boundary crossing detected in the energy range.")

    # Theoretical Null PDF Plot
    x = np.linspace(0.5, 1.5, 200)
    plt.plot(x, stats.norm(loc=mu_null, scale=sigma_null).pdf(x), 'k--', linewidth=2, label="Null Conformal H0")
    
    plt.title("Transition of Conformal Momenta Cross-Ratios Across Energy Bins\nSymmetry Breaking Scale Identification")
    plt.xlabel("Conformal Invariant Cross-Ratio (R)")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(plot_path)
    print(f"\nSymmetry-breaking analysis plot saved to {plot_path}")

if __name__ == '__main__':
    detect_symmetry_boundary()
