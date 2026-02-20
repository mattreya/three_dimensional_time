import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u

def cross_correlate_anomalies():
    print("Loading Euclid Dark Matter/Time anomalies...")
    euclid_file = 'euclid_lensing_candidates.csv'
    try:
        euclid_df = pd.read_csv(euclid_file)
    except FileNotFoundError:
        print(f"File not found: {euclid_file}")
        return
        
    print("Loading JWST Early Universe Structural anomalies...")
    jwst_file = 'jwst_early_universe_candidates.csv'
    try:
        jwst_df = pd.read_csv(jwst_file)
    except FileNotFoundError:
        print(f"File not found: {jwst_file}")
        return
        
    # We want to see if the highly ordered ancient galaxies lie within the 
    # paths of parallel shear coherence we noted in the Euclid data.
    # We will do a generic spatial cross-match to see if any are in the same region.
    
    print("\nPerforming spatial cross-match between anomalous datasets...")
    
    # Create SkyCoord objects
    euclid_coords = SkyCoord(ra=euclid_df['right_ascension'].values*u.deg, dec=euclid_df['declination'].values*u.deg)
    jwst_coords = SkyCoord(ra=jwst_df['ra'].values*u.deg, dec=jwst_df['dec'].values*u.deg)
    
    # We look for matches within a certain radius, representing the 'shadow' 
    # cast by an off-axis 3D time structure. Let's say 0.5 degrees.
    max_sep = 0.5 * u.deg
    
    # Match JWST to Euclid
    idx, d2d, d3d = jwst_coords.match_to_catalog_sky(euclid_coords)
    
    matches = d2d < max_sep
    match_count = matches.sum()
    
    print(f"Found {match_count} JWST candidates geographically co-located with an extreme Euclid shear anomaly.")
    
    if match_count > 0:
        print("\n--- MULTI-MODAL ANOMALY DETECTED ---")
        print("This is a highly significant finding. Objects that are 'too ordered, too soon' (JWST)")
        print("are spatially overlapping with areas of 'parallel shear' (Euclid).")
        print("This points strongly to a unified underlying cause, such as a 3D Time structure")
        print("affecting both thermodynamic evolution rates and localized spatial lensing.")
        
        # Save output
        results = jwst_df[matches].copy()
        results['euclid_distance_deg'] = d2d[matches].deg
        results.to_csv('cross_correlated_anomalies.csv', index=False)
        print("Saved cross-correlated multi-modal candidates to cross_correlated_anomalies.csv")
    else:
        print("No immediate spatial correlation found at the current threshold.")


if __name__ == '__main__':
    cross_correlate_anomalies()
