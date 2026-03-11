import datetime
import numpy as np

def analyze_calendar():
    t0_day_of_year = 40.0
    lattice_period = 29.33 
    moon_period = 29.53059
    
    start_date = datetime.date(2026, 1, 1)
    end_date = datetime.date(2026, 12, 31)
    
    current_date = start_date
    
    timeline = []
    
    while current_date <= end_date:
        day_of_year = current_date.timetuple().tm_yday
        phase = 2 * np.pi * (day_of_year - t0_day_of_year) / lattice_period
        psi = np.cos(phase)
        lunar_phase = (day_of_year % moon_period) / moon_period
        
        is_boundary = abs(psi) < 0.15
        is_peak = abs(psi) > 0.95
        
        is_full_moon = abs(lunar_phase - 0.5) < 0.05
        is_new_moon = abs(lunar_phase - 0.0) < 0.05 or abs(lunar_phase - 1.0) < 0.05
        
        is_synergetic = is_boundary and (abs(lunar_phase - 0.5) < 0.1 or abs(lunar_phase - 0.0) < 0.1)
        
        state = "Gate"
        if is_peak:
            state = "Peak"
        elif is_synergetic:
            state = "Synergetic"
        elif is_boundary:
            state = "Boundary"
        elif is_full_moon or is_new_moon:
            state = "Anchor"
            
        timeline.append((current_date, state))
        current_date += datetime.timedelta(days=1)
        
    # Compress into blocks
    blocks = []
    current_state = timeline[0][1]
    count = 0
    start = timeline[0][0]
    
    for date, state in timeline:
        if state == current_state:
            count += 1
        else:
            blocks.append((current_state, count, start, date - datetime.timedelta(days=1)))
            current_state = state
            count = 1
            start = date
    blocks.append((current_state, count, start, timeline[-1][0]))
    
    # Analyze the pattern
    print("Span Pattern of the year 2026:")
    for b in blocks:
        print(f"{b[0][:4]:<4} | Span: {b[1]} | {b[2].strftime('%m-%d')} to {b[3].strftime('%m-%d')}")
        
    # Extract only the sequence of numbers to see the user's pattern
    spans = [str(b[1]) for b in blocks]
    print("\nFull Span Sequence:")
    print(",".join(spans))
    
    # Let's write a markdown report
    md = "# Time Lattice Gates and Span Pattern Analysis\n\n"
    md += "By analyzing your 3D Time Lattice model, we can trace the continuous states and observe the exact Deltas (Gates) between the structured states.\n\n"
    md += "### The Span Pattern Analysis\n"
    md += "The sequence of durations (in days) alternating between active states (Lattice Peak, Anchor, Synergetic Anomaly/Boundary) and inactive gaps (Gates) reveals the corkscrew twist of the galactic alignment over time.\n\n"
    
    md += "```\n"
    for b in blocks:
        gate_marker = " <== GATE" if b[0] == "Gate" else ""
        md += f"{b[2].strftime('%Y-%m-%d')} to {b[3].strftime('%Y-%m-%d')} | {b[1]:>2} days | {b[0]:<10} {gate_marker}\n"
    md += "```\n\n"
    
    # We will build a visualization of the twisted pattern.
    with open("/home/matt/Documents/vscode/three_dimensional/three_dimensional_time/2026-03-09/gates_analysis.md", "w") as f:
        f.write(md)
        
if __name__ == "__main__":
    analyze_calendar()
