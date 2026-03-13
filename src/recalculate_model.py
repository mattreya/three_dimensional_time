
import numpy as np
import datetime

def recalculate():
    # Constants
    t0 = 40 # Feb 9, 2026
    
    # Old Model (Fudged)
    p_old = 29.33
    angle_old = 57.56
    
    # New Model (Empirical/Corrected)
    p_new = 16.0
    angle_new = 51.52
    
    target_date = 76 # March 17
    
    print(f"--- Model Comparison for March 17 (Day {target_date}) ---")
    
    # Stability Check
    phase_old = (target_date - t0) / p_old
    psi_old = np.cos(2 * np.pi * phase_old)
    
    phase_new = (target_date - t0) / p_new
    psi_new = np.cos(2 * np.pi * phase_new)
    
    print(f"Old Model Phase: {phase_old:.2f} cycles | Psi: {psi_old:.4f}")
    print(f"New Model Phase: {phase_new:.2f} cycles | Psi: {psi_new:.4f}")
    
    # Rotation Check
    rot_old = 360 / angle_old
    rot_new = 360 / angle_new
    
    print(f"\nOld Rotation Period: {rot_old * p_old:.2f} days")
    print(f"New Rotation Period: {rot_new * p_new:.2f} days")
    
    # Sar Resonance (3600 years = 1,314,871.9 days)
    sar_days = 1314871.9
    
    print(f"\n--- 1 Sar (3,600 Year) Resonance ---")
    print(f"Old Model Rotations: {sar_days / (rot_old * p_old):.4f}")
    print(f"New Model Rotations: {sar_days / (rot_new * p_new):.4f}")
    
    # Check for 7-fold symmetry (360/7 = 51.428)
    angle_hept = 360 / 7
    print(f"\nHeptagonal Symmetry (51.43°):")
    print(f"Heptagonal Rotation Period: {7 * p_new:.2f} days")
    print(f"Heptagonal Sar Rotations: {sar_days / (7 * p_new):.4f}")

if __name__ == '__main__':
    recalculate()
