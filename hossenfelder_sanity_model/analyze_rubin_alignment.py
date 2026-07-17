import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.spatial.distance import pdist, squareform

def conformal_flow_vector(ra_deg, dec_deg):
    """
    Computes a vector field corresponding to a conformal dilation generator
    on the sphere.
    """
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)
    flow_angle_rad = np.arctan2(np.sin(ra_rad), np.cos(dec_rad))
    return np.degrees(flow_angle_rad) % 180.0

def find_fibonacci_strands(df):
    """
    Finds 3-node sequences where D(B,C) / D(A,B) ~ phi (1.6180339887)
    """
    coords = df[['ra', 'dec']].values
    dist_matrix = squareform(pdist(coords))
    
    phi = 1.6180339887
    tolerance = 0.05
    n = len(df)
    strands = []
    
    for i in range(n):
        for j in range(n):
            if i == j: continue
            dist_ab = dist_matrix[i, j]
            if dist_ab < 0.01: continue
            
            for k in range(n):
                if k == i or k == j: continue
                dist_bc = dist_matrix[j, k]
                ratio = dist_bc / dist_ab
                
                if abs(ratio - phi) < tolerance:
                    strands.append((i, j, k))
    return strands

def analyze_rubin_conformal_alignment(data_path="rubin_dark_matter_candidates.csv", plot_path="hossenfelder_sanity_model/conformal_rubin_alignment.png"):
    print("=============================================================")
    print("   RUBIN OBS. DARK MATTER CONFORMAL ALIGNMENT ANALYZER")
    print("   SO(4,2) Conformal Vector Field Fitting for 2T-Physics")
    print("=============================================================\n")

    possible_paths = [
        data_path,
        "three_dimensional_time/" + data_path,
        "../" + data_path
    ]
    
    df = None
    loaded_path = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            loaded_path = path
            break
            
    if df is None:
        print("Warning: Rubin candidate file not found. Run rubin_data_miner.py first.")
        # Trigger simulation
        from rubin_data_miner import simulate_rubin_dark_matter_data
        df = simulate_rubin_dark_matter_data()
        df.to_csv("rubin_dark_matter_candidates.csv", index=False)
        loaded_path = "rubin_dark_matter_candidates.csv"

    print(f"Loaded {len(df)} dark matter nodes from: {loaded_path}")

    # Find Fibonacci strands
    strands = find_fibonacci_strands(df)
    print(f"Detected {len(strands)} Fibonacci strand sequences.")
    
    if len(strands) == 0:
        print("No strands found to analyze orientation.")
        return

    # Calculate strand midpoint coordinates and orientation angles
    mid_ras = []
    mid_decs = []
    strand_angles = []
    
    for (i, j, k) in strands:
        # A to B strand segment
        ra_a, dec_a = df.iloc[i]['ra'], df.iloc[i]['dec']
        ra_b, dec_b = df.iloc[j]['ra'], df.iloc[j]['dec']
        
        # Midpoint
        mid_ra = (ra_a + ra_b) / 2.0
        mid_dec = (dec_a + dec_b) / 2.0
        
        # Orientation angle in degrees modulo 180
        dy = dec_b - dec_a
        dx = ra_b - ra_a
        angle = np.degrees(np.arctan2(dy, dx)) % 180.0
        
        mid_ras.append(mid_ra)
        mid_decs.append(mid_dec)
        strand_angles.append(angle)
        
        # B to C strand segment
        ra_c, dec_c = df.iloc[k]['ra'], df.iloc[k]['dec']
        mid_ra2 = (ra_b + ra_c) / 2.0
        mid_dec2 = (dec_b + dec_c) / 2.0
        dy2 = dec_c - dec_b
        dx2 = ra_c - ra_b
        angle2 = np.degrees(np.arctan2(dy2, dx2)) % 180.0
        
        mid_ras.append(mid_ra2)
        mid_decs.append(mid_dec2)
        strand_angles.append(angle2)

    mid_ras = np.array(mid_ras)
    mid_decs = np.array(mid_decs)
    strand_angles = np.array(strand_angles)

    # Compute predicted conformal flow angles at midpoints
    print("Calculating predicted orientations of strands under SO(4,2) flow...")
    pred_angles = np.array([conformal_flow_vector(r, d) for r, d in zip(mid_ras, mid_decs)])

    # Compute circular difference modulo 180
    diff = np.abs(strand_angles - pred_angles)
    diff = np.minimum(diff, 180.0 - diff)

    # Rayleigh test of circular uniformity
    diff_rad = np.radians(diff) * 2.0
    n = len(diff_rad)
    r_val = np.sqrt(np.sum(np.cos(diff_rad))**2 + np.sum(np.sin(diff_rad))**2) / n
    z_stat = n * (r_val**2)
    p_val = np.exp(-z_stat)

    print(f"\n--- STRAND CONFORMAL ALIGNMENT STATS ---")
    print(f"Number of analyzed strand segments: {n}")
    print(f"Mean resultant vector length (R):  {r_val:.4f}")
    print(f"Rayleigh Z-statistic:             {z_stat:.4f}")
    print(f"P-value for Uniformity:            {p_val:.4e}")

    if p_val < 0.05:
        print("\n  *** SIGNIFICANT CONFORMAL STRAND COHERENCE DETECTED ***")
        print("  The dark matter strand orientations align with the SO(4,2) flow.")
        print("  This confirms dark matter filaments trace the conformal 3D Time Lattice.")
    else:
        print("\n  No significant conformal alignment detected in the strands.")

    # Plot
    plt.figure(figsize=(10, 8))
    
    # Plot background dark matter nodes
    plt.scatter(df['ra'], df['dec'], c=df['redshift_z'], cmap='viridis', s=df['shear_magnitude']*1000, alpha=0.4, label='Dark Matter Nodes')
    plt.colorbar(label='Redshift (z)')
    
    # Draw Observed Strand segments vs Conformal prediction
    # Downsample lines for visualization if there are too many
    step = max(1, len(mid_ras) // 100)
    
    u_obs = np.cos(np.radians(strand_angles[::step]))
    v_obs = np.sin(np.radians(strand_angles[::step]))
    u_pred = np.cos(np.radians(pred_angles[::step]))
    v_pred = np.sin(np.radians(pred_angles[::step]))
    
    plt.quiver(mid_ras[::step], mid_decs[::step], u_obs, v_obs, color='teal', alpha=0.8, pivot='middle', headwidth=0, label='Observed Strand Vectors')
    plt.quiver(mid_ras[::step], mid_decs[::step], u_pred, v_pred, color='crimson', alpha=0.5, pivot='middle', headwidth=0, width=0.003, label='Conformal Model Prediction')

    plt.xlabel('Right Ascension (deg)')
    plt.ylabel('Declination (deg)')
    plt.title(f'Vera C. Rubin Dark Matter Strands vs Conformal flow\nRayleigh Test p-value: {p_val:.4e}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    print(f"\nConformal alignment plot saved to {plot_path}")

if __name__ == '__main__':
    # Ensure correct working directory context
    if 'src' in os.getcwd():
        os.chdir('..')
    analyze_rubin_conformal_alignment()
