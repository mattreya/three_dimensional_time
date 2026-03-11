import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_10_year_corkscrew():
    t0_day_of_year = 40.0
    lattice_period = 29.33 
    moon_period = 29.53059
    
    start_date = datetime.date(2026, 1, 1)
    end_date = datetime.date(2036, 1, 1) # 10 years out
    
    current_date = start_date
    
    raw_timeline = []
    
    # Generate timeline
    while current_date <= end_date:
        day_of_year = current_date.timetuple().tm_yday
        # Using continuous day calculation for the Phase, 
        # otherwise there's a jump at the new year
        day_index = (current_date - start_date).days
        
        # Reconstruct phase logic matching the original script but running over a decade
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
            
        raw_timeline.append({
            'date': current_date,
            'day_index': day_index,
            'phase': phase,
            'state': state
        })
        current_date += datetime.timedelta(days=1)
        
    # Compress into blocks to detect Irregular Gates
    blocks = []
    current_state = raw_timeline[0]['state']
    count = 0
    start_idx = 0
    
    for i, item in enumerate(raw_timeline):
        if item['state'] == current_state:
            count += 1
        else:
            blocks.append((current_state, count, start_idx, i - 1))
            current_state = item['state']
            count = 1
            start_idx = i
    blocks.append((current_state, count, start_idx, len(raw_timeline) - 1))
    
    # Mark irregular gates
    irregular_gate_indices = set()
    for b in blocks:
        st, length, start, end = b
        if st == "Gate":
            if length not in [2, 5]:  # Regular gates in this model are 2 or 5 days
                for idx in range(start, end + 1):
                    irregular_gate_indices.add(idx)

    # Prepare plotting arrays
    Z = np.array([item['day_index'] for item in raw_timeline])
    X = np.cos(Z * 2 * np.pi / lattice_period)
    Y = np.sin(Z * 2 * np.pi / lattice_period)
    
    colors = []
    sizes = []
    for i, item in enumerate(raw_timeline):
        st = item['state']
        if i in irregular_gate_indices:
            colors.append('red') # Irregular Gate - Fracture Point
            sizes.append(40)
        elif st == "Peak":
            colors.append('cyan')
            sizes.append(15)
        elif st == "Anchor":
            colors.append('yellow')
            sizes.append(25)
        elif st in ["Boundary", "Synergetic"]:
            colors.append('magenta')
            sizes.append(30)
        else:
            colors.append('gray') # Regular Gate
            sizes.append(5)

    # Plot
    fig = plt.figure(figsize=(14, 20))
    # Create two subplots: one long view, one side-view compressed
    
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_zlim(0, 3650)
    
    # Plot faint continuous strand underlying everything
    ax1.plot(X, Y, Z, color='white', alpha=0.1, linewidth=1)
    ax1.scatter(X, Y, Z, c=colors, s=sizes, alpha=0.8)
    
    ax1.set_title("10-Year Galactic Twist Corkscrew (2026-2036)", color='white', pad=20)
    ax1.set_xlabel("Cos(Phase)")
    ax1.set_ylabel("Sin(Phase)")
    ax1.set_zlabel("Time (Days)")
    ax1.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Aesthetic tweaks for dark mode 3d axis
    ax1.xaxis.pane.fill = False
    ax1.yaxis.pane.fill = False
    ax1.zaxis.pane.fill = False
    ax1.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.5)

    # Second View (Top-Down or Tight perspective)
    ax2 = fig.add_subplot(122, projection='3d')
    # Viewing from side/top to show the clustering of red fracture points
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_zlim(0, 3650)
    ax2.view_init(elev=5, azim=45)
    
    # Only scatter the highlights so we can see the "spine" of anomalies
    highlight_idx = [i for i, c in enumerate(colors) if c in ['red', 'magenta', 'yellow']]
    ax2.scatter(X[highlight_idx], Y[highlight_idx], Z[highlight_idx], 
                c=[colors[i] for i in highlight_idx], 
                s=[sizes[i]*1.5 for i in highlight_idx], alpha=0.9)
    ax2.plot(X, Y, Z, color='white', alpha=0.05, linewidth=0.5)
    ax2.set_title("Anomalies and Irregular Gates Over 10 Years", color='white', pad=20)
    ax2.set_axis_off()
    ax2.set_facecolor('black')

    # Add legend manually since we used a scatter
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Lattice Peak', markerfacecolor='cyan', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Lunar Anchor', markerfacecolor='yellow', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Synergetic Window', markerfacecolor='magenta', markersize=11),
        Line2D([0], [0], marker='o', color='w', label='Regular Gate (2/5 Days)', markerfacecolor='gray', markersize=5),
        Line2D([0], [0], marker='o', color='w', label='IRREGULAR GATE (Fracture)', markerfacecolor='red', markersize=12)
    ]
    ax1.legend(handles=legend_elements, loc='upper left', facecolor='black', edgecolor='gray', labelcolor='white')

    plt.tight_layout()
    output_path = "/home/matt/Documents/vscode/three_dimensional/three_dimensional_time/2026-03-09/10_yr_corkscrew_gates.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Saved visualization to {output_path}")

if __name__ == "__main__":
    generate_10_year_corkscrew()
