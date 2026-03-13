
import datetime
import numpy as np

def analyze_true_lattice():
    # Corrected Constants
    t0_day_of_year = 40.0 # Feb 9
    lattice_period = 16.0 # The actual injected frequency
    
    # Standard Astronomical Constant
    moon_period = 29.53059
    
    start_date = datetime.date(2026, 1, 1)
    end_date = datetime.date(2026, 12, 31)
    
    current_date = start_date
    timeline = []
    
    while current_date <= end_date:
        day_of_year = current_date.timetuple().tm_yday
        
        # Stability Function
        phase = 2 * np.pi * (day_of_year - t0_day_of_year) / lattice_period
        psi = np.cos(phase)
        
        # Lunar Phase (for Anchor points)
        # Using a fixed reference for Full Moon - March 14, 2026 is Day 73
        lunar_days_since_ref = day_of_year - 73
        lunar_phase = (lunar_days_since_ref % moon_period) / moon_period
        
        is_boundary = abs(psi) < 0.2
        is_peak = abs(psi) > 0.8
        
        is_full_moon = abs(lunar_phase - 0.0) < 0.05 or abs(lunar_phase - 1.0) < 0.05
        is_new_moon = abs(lunar_phase - 0.5) < 0.05
        
        # Synergetic Anomaly: Boundary Crossing + Lunar Anchor
        is_synergetic = is_boundary and (is_full_moon or is_new_moon)
        
        state = "Gate" # Default state is the "gap"
        if is_synergetic:
            state = "SYNERGETIC"
        elif is_boundary:
            state = "Boundary"
        elif is_peak:
            state = "Peak"
        elif is_full_moon or is_new_moon:
            state = "Anchor"
            
        timeline.append((current_date, state))
        current_date += datetime.timedelta(days=1)

    # Group into blocks
    blocks = []
    if not timeline: return
    
    curr_state = timeline[0][1]
    curr_start = timeline[0][0]
    count = 0
    
    for date, state in timeline:
        if state == curr_state:
            count += 1
        else:
            blocks.append((curr_state, count, curr_start, date - datetime.timedelta(days=1)))
            curr_state = state
            curr_start = date
            count = 1
    blocks.append((curr_state, count, curr_start, timeline[-1][0]))

    print(f"{'State':<12} | {'Span':<5} | {'Range'}")
    print("-" * 40)
    for b in blocks:
        marker = " <--" if b[0] == "SYNERGETIC" else ""
        print(f"{b[0]:<12} | {b[1]:<5} | {b[2].strftime('%m-%d')} to {b[3].strftime('%m-%d')}{marker}")

    # Check for March 17
    mar17 = datetime.date(2026, 3, 17)
    for b in blocks:
        if b[2] <= mar17 <= b[3]:
            print(f"\n[ANALYSIS] March 17 status: {b[0]} ({b[1]} day span)")

if __name__ == "__main__":
    analyze_true_lattice()
