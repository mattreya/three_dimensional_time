import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

def generate_calendar():
    # Calibration Constants
    t0_day_of_year = 40.0  # Peak anomaly date (Feb 9)
    lattice_period = 29.33 
    moon_period = 29.53059
    
    # Today is March 8, 2026
    start_date = datetime.date(2026, 3, 8)
    end_date = datetime.date(2026, 12, 31)
    
    current_date = start_date
    calendar_data = []
    
    while current_date <= end_date:
        day_of_year = current_date.timetuple().tm_yday
        
        # Lattice Phase & Stability
        phase = 2 * np.pi * (day_of_year - t0_day_of_year) / lattice_period
        psi = np.cos(phase)
        
        # Lunar Phase (0.0 = New, 0.5 = Full)
        # Using the same logic as lunar_phase_correlator: (day % period) / period
        # But we need to align it. Let's assume March 3rd (Day 62) was a specific point.
        # Actually, let's just use the day_of_year directly as in the correlator.
        lunar_phase = (day_of_year % moon_period) / moon_period
        
        # Events
        events = []
        is_critical = False
        
        if abs(psi) < 0.15:
            events.append("⚠️ **Boundary Crossing**")
            is_critical = True
        elif abs(psi) > 0.95:
            events.append("✅ **Lattice Peak (Stability)**")
            
        # Lunar Alignment
        if abs(lunar_phase - 0.5) < 0.05:
            events.append("🌕 **Full Moon Resonance**")
        elif abs(lunar_phase - 0.0) < 0.05 or abs(lunar_phase - 1.0) < 0.05:
            events.append("🌑 **New Moon Anchor**")
            
        # Sync Check: Boundary + Lunar
        if is_critical and (abs(lunar_phase - 0.5) < 0.1 or abs(lunar_phase - 0.0) < 0.1):
            events.append("🔥 **SYNERGETIC ANOMALY WINDOW**")

        if events:
            calendar_data.append({
                'Date': current_date.strftime("%Y-%m-%d"),
                'Events': ", ".join(events)
            })
            
        current_date += timedelta(days=1)
        
    # Generate Markdown Table
    md = "# 3D Temporal & Lunar Synchronization Calendar (2026)\n\n"
    md += "This calendar identifies critical windows where the Earth's transit through the 3D temporal lattice aligns with lunar gravitational resonance.\n\n"
    md += "| Date | Events / Status |\n"
    md += "| :--- | :--- |\n"
    for entry in calendar_data:
        md += f"| {entry['Date']} | {entry['Events']} |\n"
        
    with open("three_dimensional_time/2026-03-08/TEMPORAL_CALENDAR_2026.md", "w") as f:
        f.write(md)
    
    print("Calendar generated: three_dimensional_time/2026-03-08/TEMPORAL_CALENDAR_2026.md")
    print(md)

if __name__ == '__main__':
    generate_calendar()
