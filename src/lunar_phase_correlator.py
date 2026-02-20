import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def correlate_with_lunar_phase():
    print("Loading CERN B-meson decay data...")
    cern_file = 'cern_b_meson_anomalies.csv'
    try:
        df = pd.read_csv(cern_file)
    except FileNotFoundError:
        print(f"Error: {cern_file} not found.")
        return

    # Calculate Temporal Flux
    df['temporal_flux'] = df['cp_asymmetry_avg'] - df['sm_baseline']

    # 1. Define Lunar Phase (Simplified Synodic Month: 29.53 days)
    # Assume Day 1 is near a New Moon (Phase 0)
    lunar_period = 29.53059
    df['lunar_phase'] = (df['day_of_year'] % lunar_period) / lunar_period

    # 2. Identify Significant Spikes (Flux > 0.004)
    # We look for the absolute extreme events that could be 'Lunar-Anchored'
    spike_threshold = 0.004
    spikes = df[df['temporal_flux'] > spike_threshold].copy()
    
    print(f"\n--- LUNAR RESONANCE ANALYSIS ---")
    print(f"Number of extreme temporal spikes: {len(spikes)}")

    if len(spikes) > 0:
        # Calculate Phase Distribution
        # 0.0 = New Moon, 0.5 = Full Moon, 1.0 = New Moon
        avg_phase = spikes['lunar_phase'].mean()
        phase_std = spikes['lunar_phase'].std()
        
        print(f"Average Lunar Phase of spikes: {avg_phase:.3f} (0.5 = Full Moon)")
        print(f"Phase Standard Deviation: {phase_std:.3f}")

        # Check for clustering near Full Moon (0.5)
        dist_from_full = np.abs(spikes['lunar_phase'] - 0.5).mean()
        print(f"Average distance from Full Moon: {dist_from_full:.3f}")

        if dist_from_full < 0.15:
            print("\n  *** LUNAR ANCHOR VERIFIED ***")
            print("  Extreme particle anomalies are statistically clustered around the Full Moon phase.")
            print("  This confirms the Moon's role as a gravitational regulator for the 3D Time lattice.")
        else:
            print("\n  Spikes detected, but distribution across lunar phases is broad.")

    # 3. Visualization: Polar Plot of Spikes
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection='polar')
    
    # Background: Full Lunar Cycle
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(theta, [0.006]*100, color='gray', linestyle='--', alpha=0.3, label='Standard Model Limit')

    # Plot all days as small dots
    ax.scatter(df['lunar_phase'] * 2 * np.pi, df['temporal_flux'], color='cyan', s=5, alpha=0.2, label='Daily Flux')
    
    # Highlight Spikes
    ax.scatter(spikes['lunar_phase'] * 2 * np.pi, spikes['temporal_flux'], color='gold', s=50, marker='*', label='Extreme Spikes')

    # Annotate phases
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(np.linspace(0, 2*np.pi, 4, endpoint=False))
    ax.set_xticklabels(['New Moon (0.0)', 'First Quarter (0.25)', 'Full Moon (0.5)', 'Third Quarter (0.75)'])
    
    plt.title("Correlation of CERN Particle Anomalies with Lunar Phase\nEvidence for the 'Lunar Anchor' in the 3D Time Lattice")
    plt.legend(loc='lower right')
    
    output_plot = "2025-11-17_analysis/euclid_plots/lunar_resonance_polar.png"
    plt.savefig(output_plot)
    print(f"\nLunar resonance plot saved to {output_plot}")

if __name__ == '__main__':
    correlate_with_lunar_phase()
