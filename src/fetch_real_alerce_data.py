import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from alerce.core import Alerce

# Initialize the ALeRCE client
alerce = Alerce()

def fetch_and_analyze_real_rubin_data():
    print("--- Fetching Real LSST/ZTF Transient Data via ALeRCE API ---")
    
    # We query the ALeRCE ZTF/LSST broker for recent transients.
    # While full 7 million object Rubin streams are not public, ALeRCE 
    # provides public APIs to a filtered database.
    try:
        print("Querying ALeRCE database for recent high-probability transients...")
        # Get the most recent transients detected (e.g. last 24-48 hours)
        # We query for basic objects (can't ask for generic unclassified noise easily,
        # Request maximum page size of any object without strict classifier filtering
        objects = alerce.query_objects(
            format='pandas', 
            page_size=2000, 
            order_by='firstmjd',
            order_mode='DESC'
        )
        
        if len(objects) == 0:
            print("No recent objects found in public API slice.")
            return

        print(f"Successfully retrieved {len(objects)} recent transients.")
        
        # 2. Analyze the spatial distribution (RA, Dec)
        # If the 51-degree geometric "Snap" is happening, we might see a bias
        # in the spatial localization of these transients towards the Cygnus axis.
        ra = objects['meanra'].values
        dec = objects['meandec'].values
        
        print("\n--- Analysing Real Transient Distribution vs. The 51-Degree Lattice Shift ---")
        
        # In a perfectly random universe, RA and Dec of transients (like SN) should be isotopic.
        # But if the Time Lattice is physically shifting the observation field by 51 degrees,
        # the detected distribution will be skewed.
        
        plt.figure(figsize=(10, 6))
        plt.scatter(ra, dec, alpha=0.6, color='blue', edgecolors='white')
        plt.title(f"Spatial Distribution of {len(objects)} Real Transients\n(via ALeRCE API on March 17)")
        plt.xlabel("Right Ascension (Degrees)")
        plt.ylabel("Declination (Degrees)")
        
        # Highlight Cygnus Region (Roughly RA 300, Dec 40)
        # This is where the 51-degree Temporal Pivot is anchored (from previous SAR 126 analysis)
        plt.scatter([300], [40], color='red', marker='*', s=300, label="Theoretical Pivot Hinge (Cygnus Vector)")
        plt.legend()
        plt.grid(True)
        
        output_dir = "2026-03-17"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        out_plot = os.path.join(output_dir, "real_alerce_transient_distribution.png")
        plt.savefig(out_plot)
        print(f"Data mapping saved to {out_plot}")
        
    except Exception as e:
        print(f"Error querying ALeRCE API: {e}")

if __name__ == '__main__':
    fetch_and_analyze_real_rubin_data()
