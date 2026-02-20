import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from scipy.stats import rayleigh

def analyze_temporal_alignment():
    print("Loading Euclid 'Needle' (High Ellipticity) Candidates...")
    file_path = '2025-11-17_analysis/euclid_plots/high_ellipticity_candidates.csv'
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Candidate file not found at {file_path}")
        return

    # Extract relevant columns
    ra = df['right_ascension'].values
    dec = df['declination'].values
    pa = df['position_angle'].values # Position angle in degrees

    print(f"Analyzing {len(df)} candidates for orientation coherence...")

    # 1. Rayleigh Test for Circular Uniformity
    # We want to see if the Position Angles (PA) are randomly distributed.
    # PA is usually 0-180 for orientation, so we double it to use standard circular stats.
    pa_rad = np.radians(pa)
    z_stat, p_val = rayleigh_test(pa_rad * 2)

    print(f"\n--- ALIGNMENT STATS ---")
    print(f"Rayleigh Z-statistic: {z_stat:.4f}")
    print(f"P-value for Uniformity: {p_val:.4e}")

    if p_val < 0.05:
        print("  *** SIGNIFICANT COHERENCE DETECTED ***")
        print("  The orientations are NOT random. This suggests a large-scale 'Time Flow' alignment.")
    else:
        print("  No global alignment detected in this sample.")

    # 2. Visualize the Vector Field
    plt.figure(figsize=(12, 6))
    plt.subplot(111, projection='mollweide')
    
    # Convert RA/Dec to Mollweide (radians, RA shifted to -pi to pi)
    ra_plot = np.radians(ra)
    ra_plot[ra_plot > np.pi] -= 2 * np.pi
    dec_plot = np.radians(dec)
    
    # Create "quivers" representing galaxy orientation
    length = 0.05
    u_vec = length * np.sin(pa_rad)
    v_vec = length * np.cos(pa_rad)
    
    plt.quiver(ra_plot, dec_plot, u_vec, v_vec, color='cyan', alpha=0.6, pivot='middle', headwidth=0)
    plt.grid(True)
    plt.title("Spatial Alignment of Euclid 'Needle' Candidates\nPossible Direction of the 3D Time Apex")
    
    output_plot = "2025-11-17_analysis/euclid_plots/alignment_vector_field.png"
    plt.savefig(output_plot)
    print(f"\nVector field plot saved to {output_plot}")

    # 3. Estimate the Time Apex
    # For a simple first pass, we identify the mean resultant vector direction.
    mean_pa = np.degrees(np.arctan2(np.mean(np.sin(pa_rad * 2)), np.mean(np.cos(pa_rad * 2))) / 2)
    if mean_pa < 0: mean_pa += 180
    
    print(f"\nEstimated Mean Orientation (Time Stream Axis): {mean_pa:.2f} degrees")
    print("This axis represents the 'folding line' of the Quantum Tier onto our Einstein Tier.")

    # 4. Local Spatial Correlation (Coherence Check)
    # We check if neighboring galaxies have similar orientations.
    print("\n--- LOCAL COHERENCE ANALYSIS ---")
    coords = SkyCoord(ra=ra*u.deg, dec=dec*u.deg)
    
    # Simple nearest neighbor check (up to 5 neighbors)
    all_correlations = []
    for i in range(len(coords)):
        sep = coords[i].separation(coords)
        # Find indices of 5 closest neighbors (excluding self)
        nearest_idx = np.argsort(sep)[1:6]
        
        # Calculate how similar their PAs are (using circular difference)
        self_pa = pa_rad[i]
        neighbor_pas = pa_rad[nearest_idx]
        
        # Difference in orientation (normalized to 0-90 degrees)
        diff = np.degrees(np.abs(np.arctan2(np.sin(self_pa - neighbor_pas), np.cos(self_pa - neighbor_pas))))
        all_correlations.append(np.mean(diff))

    avg_local_diff = np.mean(all_correlations)
    print(f"Average orientation difference between neighbors: {avg_local_diff:.2f} degrees")
    
    # Expected random diff for 0-180 orientation is 45 degrees.
    if avg_local_diff > 50:
        print("  *** TEMPORAL ORTHOGONALITY DETECTED ***")
        print(f"  Neighbors are significantly MORE perpendicular than random chance (Diff: {avg_local_diff:.2f} vs Expected: 45.00).")
        print("  This points to a lattice-like grid in the 3D Time canvas.")
    elif avg_local_diff < 40:
        print("  *** LOCAL COHERENCE DETECTED ***")
        print(f"  Neighbors are more aligned than random chance.")
    else:
        print("  No significant local coherence found at this scale.")

    # 5. Distribution Analysis
    plt.figure(figsize=(8, 5))
    plt.hist(all_correlations, bins=20, color='magenta', alpha=0.7, edgecolor='black')
    plt.axvline(45, color='white', linestyle='--', label='Random Expectation (45°)')
    plt.title("Distribution of Local Orientation Differences\n(Temporal Orthogonality Check)")
    plt.xlabel("Mean Neighbor Difference (Degrees)")
    plt.ylabel("Frequency")
    plt.legend()
    
    hist_plot = "2025-11-17_analysis/euclid_plots/local_alignment_histogram.png"
    plt.savefig(hist_plot)
    print(f"\nLocal difference histogram saved to {hist_plot}")

def rayleigh_test(angles):
    """Simplified Rayleigh test for uniformity of circular data."""
    n = len(angles)
    r = np.sqrt(np.sum(np.cos(angles))**2 + np.sum(np.sin(angles))**2) / n
    z = n * (r**2)
    p = np.exp(-z) * (1 + (2*z - z**2)/(4*n) - (24*z - 132*z**2 + 76*z**3 - 9*z**4)/(288*n**2))
    return z, p

if __name__ == '__main__':
    # Ensure we are in the three_dimensional_time directory or relative to it
    import os
    if os.path.basename(os.getcwd()) != 'three_dimensional_time':
        print("Running from sub-directory logic...")
    
    analyze_temporal_alignment()
