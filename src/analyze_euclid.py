import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def analyze_euclid_data(file_path):
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records.")

    # Basic filtering
    df = df[df['det_quality_flag'] == 0].copy()
    
    # Calculate shear pseudo-vectors for visualization
    # Convert position_angle to radians
    theta_rad = np.radians(df['position_angle'])
    
    # Pseudo-shear components
    # The length of the line will be proportional to ellipticity
    # Angle is theta
    df['g1'] = df['ellipticity'] * np.cos(theta_rad)
    df['g2'] = df['ellipticity'] * np.sin(theta_rad)
    
    print("Performing basic spatial clustering (DBSCAN)...")
    # Clustering based on spatial coordinates
    # epsilon in degrees. 0.1 degree is 6 arcmin.
    coords = df[['right_ascension', 'declination']].values
    db = DBSCAN(eps=0.1, min_samples=5).fit(coords)
    df['cluster'] = db.labels_
    
    n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    print(f"Found {n_clusters} spatial clusters.")
    
    # Plotting the shear field
    plt.figure(figsize=(12, 8))
    
    # Plot background points
    noise = df[df['cluster'] == -1]
    plt.scatter(noise['right_ascension'], noise['declination'], c='lightgray', s=10, alpha=0.5, label='Noise')
    
    # Plot clusters colored differently
    colors = plt.cm.jet(np.linspace(0, 1, n_clusters))
    for i in range(n_clusters):
        cluster_points = df[df['cluster'] == i]
        plt.scatter(cluster_points['right_ascension'], cluster_points['declination'], c=[colors[i]], s=20, label=f'Cluster {i}')
        
    # Overlay quiver (shear vectors)
    # We plot a line with no arrow head for shear (it's a spin-2 field, not a vector, so head isn't meaningful)
    plt.quiver(df['right_ascension'], df['declination'], df['g1'], df['g2'], 
               headwidth=0, headlength=0, headaxislength=0,
               scale=10, alpha=0.3, color='black', pivot='middle')
    
    plt.title('Euclid Anomalous Lensing Candidates - Shear Field')
    plt.xlabel('Right Ascension (deg)')
    plt.ylabel('Declination (deg)')
    
    plt.tight_layout()
    output_img = 'euclid_shear_map.png'
    plt.savefig(output_img, dpi=300)
    print(f"Saved shear map visualization to {output_img}")

    # Analyze specifically 3D Time hypothesis signature:
    # A standard dark matter halo produces tangential shear (radial coherence).
    # The 3D time hypothesis asks if there are off-axis mass structures, which might 
    # produce shear fields that are coherent across large patches without a defined central mass.
    print("\n--- 3D Time Signature Analysis ---")
    for i in range(n_clusters):
        c_df = df[df['cluster'] == i]
        mean_g1 = c_df['g1'].mean()
        mean_g2 = c_df['g2'].mean()
        mean_e = c_df['ellipticity'].mean()
        
        # If the vectors are perfectly tangential around a center, mean g1 and g2 would be close to 0 
        # (canceling out across the circle).
        # If there's a strong non-zero mean vector in the cluster, it means the shear is 
        # aligned in a specific direction (bulk alignment), which is anomalous for a standard halo.
        bulk_alignment = np.sqrt(mean_g1**2 + mean_g2**2) / mean_e
        
        print(f"Cluster {i}: {len(c_df)} galaxies")
        print(f"  Mean Ellipticity: {mean_e:.3f}")
        print(f"  Bulk Alignment index (0=tangential, 1=fully parallel): {bulk_alignment:.3f}")
        
        if bulk_alignment > 0.5:
            print("  *** ANOMALY DETECTED: Strong parallel coherence. Possible off-axis time mass structure. ***")
        else:
            print("  Likely standard tangential lensing (Dark Matter Halo).")


if __name__ == '__main__':
    analyze_euclid_data('euclid_lensing_candidates.csv')
