import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def process_candidates(file_path="euclid_lensing_candidates.csv"):
    """
    Loads the Euclid lensing candidates, performs initial exploration,
    and identifies potential morphological anomalies.
    """
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return

    print("\n--- Initial Data Exploration ---")
    print("DataFrame Info:")
    df.info()
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nDescriptive Statistics for numerical columns:")
    print(df.describe())

    plots_dir = "2025-11-17_analysis/euclid_plots"
    os.makedirs(plots_dir, exist_ok=True)

    print("\n--- Anomaly Detection: Ellipticity Outliers ---")
    # Ellipticity ranges from 0 (circular) to 1 (highly elongated)
    # We are looking for objects with unusually high or low ellipticity.

    # High Ellipticity (top 5%)
    high_ellipticity_threshold = df['ellipticity'].quantile(0.95)
    high_ellipticity_candidates = df[df['ellipticity'] > high_ellipticity_threshold]
    print(f"High Ellipticity threshold (top 5%): > {high_ellipticity_threshold:.3f}")
    print(f"Found {len(high_ellipticity_candidates)} candidates with high ellipticity.")
    if not high_ellipticity_candidates.empty:
        print("\nHigh Ellipticity Candidates (first 5):")
        print(high_ellipticity_candidates.head())
        high_ellipticity_candidates.to_csv(os.path.join(plots_dir, "high_ellipticity_candidates.csv"), index=False)


    # Low Ellipticity (bottom 5%) - these would be very circular objects
    low_ellipticity_threshold = df['ellipticity'].quantile(0.05)
    low_ellipticity_candidates = df[df['ellipticity'] < low_ellipticity_threshold]
    print(f"\nLow Ellipticity threshold (bottom 5%): < {low_ellipticity_threshold:.3f}")
    print(f"Found {len(low_ellipticity_candidates)} candidates with low ellipticity.")
    if not low_ellipticity_candidates.empty:
        print("\nLow Ellipticity Candidates (first 5):")
        print(low_ellipticity_candidates.head())
        low_ellipticity_candidates.to_csv(os.path.join(plots_dir, "low_ellipticity_candidates.csv"), index=False)


    # Visualization of Ellipticity Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['ellipticity'].dropna(), bins=50, color='skyblue', edgecolor='black')
    plt.axvline(high_ellipticity_threshold, color='red', linestyle='dashed', linewidth=1, label=f'High Ellipticity Threshold ({high_ellipticity_threshold:.3f})')
    plt.axvline(low_ellipticity_threshold, color='blue', linestyle='dashed', linewidth=1, label=f'Low Ellipticity Threshold ({low_ellipticity_threshold:.3f})')
    plt.title('Distribution of Ellipticity')
    plt.xlabel('Ellipticity')
    plt.ylabel('Number of Objects')
    plt.legend()
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(os.path.join(plots_dir, 'ellipticity_distribution.png'))
    plt.close() # Close the plot to free memory

    print("\n--- Anomaly Detection: Point-like Probability Analysis ---")
    # For now, let's just visualize its distribution
    plt.figure(figsize=(8, 5))
    df['point_like_prob'].dropna().hist(bins=30, color='lightgreen', edgecolor='black')
    plt.title('Point-like Probability Distribution')
    plt.xlabel('Point-like Probability')
    plt.ylabel('Number of Objects')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(os.path.join(plots_dir, 'point_like_prob_distribution.png'))
    plt.close()

    print("\n--- Spatial Distribution (RA, Dec) ---")
    plt.figure(figsize=(12, 8))
    plt.scatter(df['right_ascension'], df['declination'], s=5, alpha=0.5, c=df['ellipticity'], cmap='viridis')
    plt.colorbar(label='Ellipticity')
    plt.title('Spatial Distribution of Candidates (Color by Ellipticity)')
    plt.xlabel('Right Ascension (degrees)')
    plt.ylabel('Declination (degrees)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(plots_dir, 'spatial_distribution.png'))
    plt.close()

    print(f"\nPlots and candidate lists saved to the '{plots_dir}' directory.")


if __name__ == "__main__":
    process_candidates()
