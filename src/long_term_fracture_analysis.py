import numpy as np
import matplotlib.pyplot as plt

def analyze_long_term_fractures(years):
    # Constants from the established model
    t0_day = 40.0
    lattice_period = 29.33
    moon_period = 29.53059
    
    total_days = int(years * 365.25)
    days = np.arange(total_days)
    
    # Cumulative phase calculation (no resets)
    lattice_phase = 2 * np.pi * (days - t0_day) / lattice_period
    psi = np.cos(lattice_phase)
    
    # Cumulative lunar phase
    lunar_phase = (days % moon_period) / moon_period
    
    # State classification
    is_boundary = np.abs(psi) < 0.15
    is_peak = np.abs(psi) > 0.95
    is_full_moon = np.abs(lunar_phase - 0.5) < 0.05
    is_new_moon = (np.abs(lunar_phase - 0.0) < 0.05) | (np.abs(lunar_phase - 1.0) < 0.05)
    is_anchor = is_full_moon | is_new_moon
    is_synergetic = is_boundary & ((np.abs(lunar_phase - 0.5) < 0.1) | (np.abs(lunar_phase - 0.0) < 0.1) | (np.abs(lunar_phase - 1.0) < 0.1))
    
    states = np.full(total_days, "Gate", dtype='U10')
    states[is_peak] = "Peak"
    states[is_synergetic] = "Synergetic"
    states[is_boundary & ~is_synergetic] = "Boundary"
    states[is_anchor & ~(is_peak | is_synergetic | is_boundary)] = "Anchor"
    
    # Block compression to find Gate lengths
    gate_lengths = []
    current_state = states[0]
    count = 0
    
    fracture_days = []
    
    for i, state in enumerate(states):
        if state == current_state:
            count += 1
        else:
            if current_state == "Gate":
                if count not in [2, 5]:
                    fracture_days.append(i - count // 2) # Mark roughly the middle of the gate
            current_state = state
            count = 1
    
    return days, fracture_days

def plot_fracture_density(years_list):
    plt.figure(figsize=(15, 10))
    plt.style.use('dark_background')
    
    for i, years in enumerate(years_list):
        days, fractures = analyze_long_term_fractures(years)
        
        # Calculate density (fractures per year) over time
        window = int(365.25 * 5) # 5-year moving window
        bins = np.arange(0, days[-1], 365.25) # 1-year bins
        hist, bin_edges = np.histogram(fractures, bins=bins)
        
        years_axis = bin_edges[:-1] / 365.25
        
        plt.subplot(len(years_list), 1, i+1)
        plt.plot(years_axis, hist, color='red', alpha=0.7, label=f'Fractures/Year ({years} yr span)')
        plt.fill_between(years_axis, hist, color='red', alpha=0.2)
        plt.ylabel("Irregular Gates / Year")
        plt.title(f"Temporal Fracture Density Over {years} Years")
        plt.grid(alpha=0.2)
        
    plt.xlabel("Years from T0 (2026)")
    plt.tight_layout()
    plt.savefig("long_term_fracture_analysis.png")
    print("Saved long_term_fracture_analysis.png")

def analyze_periodicity(fractures, total_days):
    # Create a time series of fracture occurrences
    time_series = np.zeros(total_days)
    time_series[np.array(fractures, dtype=int)] = 1
    
    # Calculate FFT
    fft_vals = np.abs(np.fft.fft(time_series))
    fft_freqs = np.fft.fftfreq(total_days, d=1) # frequency in cycles/day
    
    # Only keep positive frequencies
    pos_mask = fft_freqs > 0
    freqs = fft_freqs[pos_mask]
    power = fft_vals[pos_mask]
    
    # Find top peaks
    top_indices = np.argsort(power)[-100:][::-1]
    print("\nTop Periodicity Peaks (Days > 30):")
    found = 0
    for idx in top_indices:
        period = 1 / freqs[idx]
        if period > 30:
            print(f"Period: {period:.2f} days (~{period/365.25:.4f} years)")
            found += 1
        if found >= 10:
            break

if __name__ == "__main__":
    days_70, fractures_70 = analyze_long_term_fractures(70)
    days_1000, fractures_1000 = analyze_long_term_fractures(1000)
    
    analyze_periodicity(fractures_1000, len(days_1000))
    plot_fracture_density([70, 1000])
