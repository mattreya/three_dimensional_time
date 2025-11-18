
import os
import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.coordinates import SkyCoord
from photutils.detection import DAOStarFinder
from itertools import combinations

def analyze_image_for_lensing(fits_path, constellation_name):
    """
    Analyzes a FITS image for signs of gravitational lensing by detecting sources
    and looking for patterns (arcs or multiple images).
    """
    print(f"--- Analyzing {constellation_name} Candidate ---")
    
    if not os.path.exists(fits_path):
        print(f"Error: FITS file not found at {fits_path}")
        return

    try:
        with fits.open(fits_path) as hdul:
            data = hdul[0].data.astype(float)

        # 1. Detect all sources in the image
        mean, median, std = sigma_clipped_stats(data, sigma=3.0)
        daofind = DAOStarFinder(fwhm=4.0, threshold=5.*std)
        sources = daofind(data - median)

        if sources is None:
            print("No significant sources detected.")
            return

        # Sort sources by flux to find the brightest objects
        sources.sort('flux', reverse=True)
        
        print(f"Detected {len(sources)} sources.")

        # 2. Identify the likely central (lensing) object
        # Assume the brightest object near the image center is the primary candidate
        image_center_x = data.shape[1] / 2
        image_center_y = data.shape[0] / 2
        
        central_object = None
        for source in sources:
            dist_to_center = np.sqrt((source['xcentroid'] - image_center_x)**2 + (source['ycentroid'] - image_center_y)**2)
            # Look for the brightest object within the central 25% of the image
            if dist_to_center < (image_center_x / 2):
                central_object = source
                break
        
        if central_object is None:
            # If no object in the center, take the brightest overall
            central_object = sources[0]

        print(f"Identified central object candidate at (x,y): ({central_object['xcentroid']:.2f}, {central_object['ycentroid']:.2f}) with flux: {central_object['flux']:.2f}")

        # 3. Logical Analysis for Lensing Patterns

        # A. Search for potential multiple images (Einstein Cross)
        # Look for a tight cluster of 2-5 sources with similar brightness near the central object.
        potential_cross_candidates = []
        # We consider sources other than the central object itself
        other_sources = [s for s in sources if s['id'] != central_object['id']]

        for group in combinations(other_sources, 4): # Look for groups of 4
            fluxes = [s['flux'] for s in group]
            positions = np.array([[s['xcentroid'], s['ycentroid']] for s in group])
            
            # Check for similar brightness (fluxes within 50% of each other)
            if max(fluxes) / min(fluxes) < 1.5:
                # Check if they are tightly clustered
                max_dist = np.max(np.linalg.norm(positions[:, np.newaxis, :] - positions[np.newaxis, :, :], axis=2))
                # And close to the central object (within 50 pixels)
                mean_pos = np.mean(positions, axis=0)
                dist_to_central = np.linalg.norm(mean_pos - [central_object['xcentroid'], central_object['ycentroid']])

                if max_dist < 100 and dist_to_central < 50:
                    potential_cross_candidates.append(group)

        if potential_cross_candidates:
            print(f"\n[LOGIC] Found {len(potential_cross_candidates)} potential 'Einstein Cross' pattern(s).")
            print("This is based on finding a tight cluster of 4 sources with similar brightness near the central object.")
        else:
            print("\n[LOGIC] No patterns suggestive of an 'Einstein Cross' were found.")

        # B. Search for potential arcs
        # Look for 3 or more sources aligned in an arc around the central object.
        potential_arc_candidates = []
        for group in combinations(other_sources, 5): # Look for groups of 5+ sources
            positions = np.array([[s['xcentroid'], s['ycentroid']] for s in group])
            
            # Calculate distances of each source from the central object
            distances = np.linalg.norm(positions - [central_object['xcentroid'], central_object['ycentroid']], axis=1)
            
            # Check if they are at a similar distance (within 15% of their average distance)
            if np.std(distances) / np.mean(distances) < 0.15:
                # Check if they span an angle (are not just clumped together)
                vectors = positions - [central_object['xcentroid'], central_object['ycentroid']]
                angles = np.arctan2(vectors[:, 1], vectors[:, 0])
                angle_span = np.ptp(np.unwrap(angles)) # Range of angles
                
                if np.degrees(angle_span) > 30: # Require a span of at least 30 degrees
                    potential_arc_candidates.append(group)

        if potential_arc_candidates:
            print(f"\n[LOGIC] Found {len(potential_arc_candidates)} potential 'Gravitational Arc' pattern(s).")
            print("This is based on finding multiple sources arranged in a circular arc around the central object.")
        else:
            print("\n[LOGIC] No patterns suggestive of a 'Gravitational Arc' were found.")


    except Exception as e:
        print(f"An error occurred during analysis: {e}")


if __name__ == "__main__":
    horologium_fits = "three_dimensional_time/2025-09-17/lensing_search/Horologium_candidate.fits"
    draco_fits = "three_dimensional_time/2025-09-17/lensing_search/Draco_candidate.fits"

    analyze_image_for_lensing(horologium_fits, "Horologium")
    print("\n" + "="*50 + "\n")
    analyze_image_for_lensing(draco_fits, "Draco")
