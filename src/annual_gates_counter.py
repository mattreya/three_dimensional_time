import datetime
import numpy as np

def count_annual_fractures():
    t0_day_of_year = 40.0
    lattice_period = 29.33 
    moon_period = 29.53059
    
    start_year = 2026
    end_year = 2035
    
    print(f"{'Year':<6} | {'Total Gates':<15} | {'Irregular Gates (1 or 3 days)':<30}")
    print("-" * 65)
    
    for year in range(start_year, end_year + 1):
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        
        current_date = start_date
        raw_timeline = []
        
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
                
            raw_timeline.append(state)
            current_date += datetime.timedelta(days=1)
            
        blocks = []
        current_state = raw_timeline[0]
        count = 0
        
        for state in raw_timeline:
            if state == current_state:
                count += 1
            else:
                blocks.append((current_state, count))
                current_state = state
                count = 1
        blocks.append((current_state, count))
        
        total_gates = 0
        irregular_gates = 0
        
        for state, length in blocks:
            if state == "Gate":
                total_gates += 1
                if length not in [2, 5]:
                    irregular_gates += 1
                    
        print(f"{year:<6} | {total_gates:<15} | {irregular_gates:<30}")

if __name__ == "__main__":
    count_annual_fractures()
