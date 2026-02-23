import pandas as pd
import numpy as np
import json
import os

def ra_dec_to_cartesian(ra_deg, dec_deg, distance=100):
    # Convert RA and Dec from degrees to radians
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)
    
    # Calculate Cartesian coordinates
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)
    
    return x, y, z

def extract_galaxies():
    galaxies = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Euclid Data (Sample a subset to avoid rendering millions of points and lagging the browser)
    euclid_file = os.path.join(base_dir, 'euclid_lensing_candidates.csv')
    if os.path.exists(euclid_file):
        print(f"Loading {euclid_file}...")
        df_euclid = pd.read_csv(euclid_file)
        # Sample 5000 galaxies for performance
        df_sampled = df_euclid.sample(n=min(5000, len(df_euclid)), random_state=42)
        for _, row in df_sampled.iterrows():
            ra = row.get('right_ascension', 0)
            dec = row.get('declination', 0)
            # Add some variability to distance for 3D depth
            dist = 100 + np.random.normal(0, 20)
            x, y, z = ra_dec_to_cartesian(ra, dec, dist)
            galaxies.append({
                'x': x, 'y': y, 'z': z,
                'color': '#88ccff', # Blueish for Euclid
                'size': np.random.uniform(0.5, 1.5)
            })

    # 2. JWST Data
    jwst_file = os.path.join(base_dir, 'jwst_early_universe_candidates.csv')
    if os.path.exists(jwst_file):
        print(f"Loading {jwst_file}...")
        df_jwst = pd.read_csv(jwst_file)
        for _, row in df_jwst.iterrows():
            ra = row.get('ra', 0)
            dec = row.get('dec', 0)
            # JWST early universe, put them further away
            dist = 300 + np.random.normal(0, 50)
            x, y, z = ra_dec_to_cartesian(ra, dec, dist)
            galaxies.append({
                'x': x, 'y': y, 'z': z,
                'color': '#ff4444', # Reddish for early universe
                'size': np.random.uniform(2.0, 4.0)
            })

    # 3. Rubin Data
    rubin_file = os.path.join(base_dir, 'rubin_time_domain_candidates.csv')
    if os.path.exists(rubin_file):
        print(f"Loading {rubin_file}...")
        df_rubin = pd.read_csv(rubin_file)
        for _, row in df_rubin.iterrows():
            ra = row.get('ra', 0)
            dec = row.get('dec', 0)
            dist = 50 + np.random.normal(0, 10)
            x, y, z = ra_dec_to_cartesian(ra, dec, dist)
            galaxies.append({
                'x': x, 'y': y, 'z': z,
                'color': '#ffcc00', # Yellow/gold for time domain anomalies
                'size': np.random.uniform(1.5, 3.0)
            })

    # Define the output directory (public folder of the React app)
    output_dir = os.path.join(base_dir, 'lattice_3d_viz', 'public')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'galaxies.json')
    
    with open(output_file, 'w') as f:
        json.dump(galaxies, f)
        
    print(f"Successfully extracted {len(galaxies)} galaxies to {output_file}")

if __name__ == '__main__':
    extract_galaxies()
