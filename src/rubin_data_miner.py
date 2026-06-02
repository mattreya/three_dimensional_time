import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

def simulate_rubin_dark_matter_data():
    print("Simulating Rubin Observatory Dark Matter Shear Catalog...")
    np.random.seed(1618) # Seed with Golden Ratio theme
    
    n_clusters = 50
    # Simulate RA and Dec
    ra = np.random.uniform(0, 5, n_clusters)
    dec = np.random.uniform(-5, 0, n_clusters)
    
    # Simulate redshift (z) and mass/shear
    z = np.random.uniform(0.1, 1.5, n_clusters)
    shear_magnitude = np.random.uniform(0.01, 0.1, n_clusters)
    
    # Inject Fibonacci strands (force some distances to be golden ratio)
    phi = 1.6180339887
    
    # To make sure we detect it, let's create a known strand
    ra[0], dec[0] = 1.0, -1.0
    ra[1], dec[1] = 1.0 + 0.1, -1.0
    ra[2], dec[2] = 1.0 + 0.1 + 0.1 * phi, -1.0
    ra[3], dec[3] = 1.0 + 0.1 + 0.1 * phi + 0.1 * (phi**2), -1.0
    
    # Inject temporal delay anomalies in redshift
    # Normal cosmological redshift should be smooth, we inject sharp orthogonal jumps
    z[1] = z[0] + 0.05
    z[2] = z[1] + 0.05 * phi
    z[3] = z[2] + 0.05 * (phi**2)
    
    df = pd.DataFrame({
        'cluster_id': [f"RDM_{i}" for i in range(n_clusters)],
        'ra': ra,
        'dec': dec,
        'redshift_z': z,
        'shear_magnitude': shear_magnitude
    })
    return df

def analyze_fibonacci_strands(df):
    print("\n--- ANALYZING FIBONACCI STRAND LAYOUTS ---")
    # Calculate pairwise distances
    coords = df[['ra', 'dec']].values
    dist_matrix = squareform(pdist(coords))
    
    phi = 1.6180339887
    tolerance = 0.05
    
    detected_strands = []
    
    # Simple algorithm to find 3-node sequences where D(B,C) / D(A,B) ~ phi
    n = len(df)
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
                    detected_strands.append((i, j, k))
                    
    print(f"Detected {len(detected_strands)} potential Fibonacci strand sequences.")
    return detected_strands, dist_matrix

def analyze_fractional_temporal_delays(df, strands):
    print("\n--- ANALYZING FRACTIONAL TEMPORAL DELAYS ---")
    # Check if the redshift delays across the strands also follow the orthogonal layout
    phi = 1.6180339887
    tolerance = 0.1
    temporal_anomalies = 0
    
    for (i, j, k) in strands:
        dz_ab = abs(df.iloc[j]['redshift_z'] - df.iloc[i]['redshift_z'])
        dz_bc = abs(df.iloc[k]['redshift_z'] - df.iloc[j]['redshift_z'])
        
        if dz_ab > 0.001:
            ratio = dz_bc / dz_ab
            if abs(ratio - phi) < tolerance:
                temporal_anomalies += 1
                
    print(f"Detected {temporal_anomalies} strands with confirmed fractional temporal delays matching the 3D Time Lattice.")
    return temporal_anomalies

def visualize_strands(df, strands):
    plt.figure(figsize=(10, 8))
    plt.scatter(df['ra'], df['dec'], c=df['redshift_z'], cmap='viridis', s=df['shear_magnitude']*1000, alpha=0.6, label='Dark Matter Nodes')
    plt.colorbar(label='Redshift (z)')
    
    plotted = False
    for (i, j, k) in strands:
        # Draw lines for the strand
        plt.plot([df.iloc[i]['ra'], df.iloc[j]['ra'], df.iloc[k]['ra']], 
                 [df.iloc[i]['dec'], df.iloc[j]['dec'], df.iloc[k]['dec']], 
                 'r--', linewidth=1.5, alpha=0.8, label='Fibonacci Strand' if not plotted else "")
        plotted = True
        
    plt.xlabel('Right Ascension (deg)')
    plt.ylabel('Declination (deg)')
    plt.title('Vera C. Rubin Dark Matter Structure\nFibonacci Strand and Temporal Delay Detection')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_plot = "rubin_dark_matter_strands.png"
    plt.savefig(output_plot)
    print(f"\nSaved strand visualization to {output_plot}")

def run_rubin_pipeline():
    df = simulate_rubin_dark_matter_data()
    output_file = "rubin_dark_matter_candidates.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved simulated catalog to {output_file}")
    
    strands, dist_matrix = analyze_fibonacci_strands(df)
    analyze_fractional_temporal_delays(df, strands)
    visualize_strands(df, strands)

if __name__ == '__main__':
    run_rubin_pipeline()
