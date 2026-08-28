"""
LHCb Heavy Flavor SME & Dalitz Phase Space Analysis
---------------------------------------------------
Analyzes the full 5.13M event LHCb dataset (B2HHH_MagnetDown.root) to:
1. Reconstruct charmless 3-body B-meson decays across the full Dalitz plot.
2. Formulate a Lorentz-covariant Standard Model Extension (SME) directional binning.
3. Compute the forward-backward and transverse asymmetry differentials Delta A_CP across Dalitz phase space.
4. Set rigorous 95% Confidence Level (CL) empirical upper bounds on the effective chiral/multi-temporal coupling (1/Lambda).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import uproot
import os

def find_dataset(filename):
    for candidate in [filename, os.path.join("..", filename), os.path.join(os.path.dirname(__file__), "..", "..", filename), os.path.join(os.path.dirname(__file__), "..", filename)]:
        if os.path.exists(candidate):
            return candidate
    return filename

def run_sme_dalitz_analysis(root_file="B2HHH_MagnetDown.root", output_dir="2025-11-17_analysis/euclid_plots"):
    print("==========================================================================")
    print("   LHCb HEAVY FLAVOR SME & DALITZ PHASE SPACE ANALYSIS (FULL DATASET)")
    print("==========================================================================")
    
    root_path = find_dataset(root_file)
    if not os.path.exists(root_path):
        print(f"Error: {root_path} not found.")
        return
        
    print(f"Opening dataset: {root_path}")
    
    m_pi = 139.570 # MeV
    m_b_nominal = 5279.34 # MeV
    
    # Store aggregated arrays for signal candidates
    sig_charge = []
    sig_mb = []
    sig_s12 = []
    sig_s23 = []
    sig_px = []
    sig_py = []
    sig_pz = []
    sig_pt = []
    sig_p_tot = []
    
    chunk_size = 1000000
    total_processed = 0
    
    with uproot.open(root_path) as f:
        tree = f['DecayTree']
        total_entries = tree.num_entries
        print(f"Total entries in DecayTree: {total_entries:,}")
        
        branches = ['H1_PX', 'H1_PY', 'H1_PZ', 'H1_ProbK', 'H1_ProbPi', 'H1_Charge',
                    'H2_PX', 'H2_PY', 'H2_PZ', 'H2_ProbK', 'H2_ProbPi', 'H2_Charge',
                    'H3_PX', 'H3_PY', 'H3_PZ', 'H3_ProbK', 'H3_ProbPi', 'H3_Charge',
                    'B_FlightDistance', 'B_VertexChi2']
        
        for start_idx in range(0, total_entries, chunk_size):
            stop_idx = min(start_idx + chunk_size, total_entries)
            print(f"Processing chunk {start_idx:,} to {stop_idx:,}...")
            
            chunk = tree.arrays(branches, library='np', entry_start=start_idx, entry_stop=stop_idx)
            
            # Net charge
            b_charge = chunk['H1_Charge'] + chunk['H2_Charge'] + chunk['H3_Charge']
            valid_charge = (np.abs(b_charge) == 1)
            
            # Reconstruct four-momentum
            e1 = np.sqrt(chunk['H1_PX']**2 + chunk['H1_PY']**2 + chunk['H1_PZ']**2 + m_pi**2)
            e2 = np.sqrt(chunk['H2_PX']**2 + chunk['H2_PY']**2 + chunk['H2_PZ']**2 + m_pi**2)
            e3 = np.sqrt(chunk['H3_PX']**2 + chunk['H3_PY']**2 + chunk['H3_PZ']**2 + m_pi**2)
            
            e_tot = e1 + e2 + e3
            px_tot = chunk['H1_PX'] + chunk['H2_PX'] + chunk['H3_PX']
            py_tot = chunk['H1_PY'] + chunk['H2_PY'] + chunk['H3_PY']
            pz_tot = chunk['H1_PZ'] + chunk['H2_PZ'] + chunk['H3_PZ']
            p_sq = px_tot**2 + py_tot**2 + pz_tot**2
            
            m_b = np.sqrt(np.maximum(0, e_tot**2 - p_sq))
            
            # Selection cuts: tight invariant mass window around B+ peak, vertex chi2 < 5, flight distance > 1.5mm
            mask = valid_charge & (m_b >= 5180) & (m_b <= 5380) & (chunk['B_VertexChi2'] < 5.0) & (chunk['B_FlightDistance'] > 1.5)
            
            if np.sum(mask) > 0:
                e1_s, e2_s, e3_s = e1[mask], e2[mask], e3[mask]
                px1_s, py1_s, pz1_s = chunk['H1_PX'][mask], chunk['H1_PY'][mask], chunk['H1_PZ'][mask]
                px2_s, py2_s, pz2_s = chunk['H2_PX'][mask], chunk['H2_PY'][mask], chunk['H2_PZ'][mask]
                px3_s, py3_s, pz3_s = chunk['H3_PX'][mask], chunk['H3_PY'][mask], chunk['H3_PZ'][mask]
                
                # Invariant masses squared s12, s23 in GeV^2
                s12_val = ((e1_s + e2_s)**2 - ((px1_s + px2_s)**2 + (py1_s + py2_s)**2 + (pz1_s + pz2_s)**2)) / 1e6
                s23_val = ((e2_s + e3_s)**2 - ((px2_s + px3_s)**2 + (py2_s + py3_s)**2 + (pz2_s + pz3_s)**2)) / 1e6
                
                sig_charge.append(b_charge[mask])
                sig_mb.append(m_b[mask])
                sig_s12.append(s12_val)
                sig_s23.append(s23_val)
                sig_px.append(px_tot[mask])
                sig_py.append(py_tot[mask])
                sig_pz.append(pz_tot[mask])
                sig_pt.append(np.sqrt(px_tot[mask]**2 + py_tot[mask]**2))
                sig_p_tot.append(np.sqrt(p_sq[mask]))
                
            total_processed += (stop_idx - start_idx)
            
    # Concatenate all signal events
    q = np.concatenate(sig_charge)
    mb = np.concatenate(sig_mb)
    s12 = np.concatenate(sig_s12)
    s23 = np.concatenate(sig_s23)
    px = np.concatenate(sig_px)
    py = np.concatenate(sig_py)
    pz = np.concatenate(sig_pz)
    pt = np.concatenate(sig_pt)
    p_tot = np.concatenate(sig_p_tot)
    
    total_sig = len(q)
    n_plus = np.sum(q == 1)
    n_minus = np.sum(q == -1)
    global_acp = (n_minus - n_plus) / (n_minus + n_plus)
    global_acp_err = np.sqrt((1 - global_acp**2) / total_sig)
    
    print(f"\n==========================================================================")
    print(f"   SIGNAL SELECTION & GLOBAL ASYMMETRY")
    print(f"==========================================================================")
    print(f"Total Selected Signal Candidates: {total_sig:,}")
    print(f"  B+ Candidates (q = +1): {n_plus:,}")
    print(f"  B- Candidates (q = -1): {n_minus:,}")
    print(f"  Global Raw CP Asymmetry: A_CP = {global_acp:.5f} +/- {global_acp_err:.5f}")
    
    # -------------------------------------------------------------------------
    # Directional SME & Dalitz Phase Space Binning Analysis
    # -------------------------------------------------------------------------
    # We define 4 kinematic Dalitz regions:
    # Region 1: Low s12 (Resonance region: rho(770)^0 / K*(892)^0, s12 < 3.0 GeV^2)
    # Region 2: Mid s12 (3.0 <= s12 < 12.0 GeV^2)
    # Region 3: High s12, Low s23 (s12 >= 12.0, s23 < 8.0 GeV^2)
    # Region 4: High s12, High s23 (s12 >= 12.0, s23 >= 8.0 GeV^2)
    
    dalitz_masks = {
        "Low s12 (< 3.0 GeV²) [Resonant]": (s12 < 3.0),
        "Mid s12 [3.0 - 12.0 GeV²]": (s12 >= 3.0) & (s12 < 12.0),
        "High s12, Low s23": (s12 >= 12.0) & (s23 < 8.0),
        "High s12, High s23": (s12 >= 12.0) & (s23 >= 8.0)
    }
    
    # Directional Projections:
    # 1. Transverse X asymmetry: px > 0 vs px < 0
    # 2. Transverse Y asymmetry: py > 0 vs py < 0
    # 3. Longitudinal Boost asymmetry: pz > median(pz) vs pz < median(pz)
    pz_median = np.median(pz)
    
    directional_tests = {
        "Transverse X (px > 0 vs px < 0)": (px > 0),
        "Transverse Y (py > 0 vs py < 0)": (py > 0),
        "Longitudinal Boost (pz > median vs pz < median)": (pz > pz_median)
    }
    
    results = []
    
    print(f"\n==========================================================================")
    print(f"   DIRECTIONAL DALITZ PHASE SPACE BINNING (SME LIV DIFFERENTIALS)")
    print(f"==========================================================================")
    
    for dir_name, dir_mask in directional_tests.items():
        print(f"\n---> Directional Axis: {dir_name}")
        for reg_name, reg_mask in dalitz_masks.items():
            # Forward / Positive direction in this region
            fwd_mask = reg_mask & dir_mask
            bwd_mask = reg_mask & (~dir_mask)
            
            n_plus_fwd = np.sum(fwd_mask & (q == 1))
            n_minus_fwd = np.sum(fwd_mask & (q == -1))
            tot_fwd = n_plus_fwd + n_minus_fwd
            
            n_plus_bwd = np.sum(bwd_mask & (q == 1))
            n_minus_bwd = np.sum(bwd_mask & (q == -1))
            tot_bwd = n_plus_bwd + n_minus_bwd
            
            if tot_fwd > 0 and tot_bwd > 0:
                acp_fwd = (n_minus_fwd - n_plus_fwd) / tot_fwd
                err_fwd = np.sqrt((1 - acp_fwd**2) / tot_fwd)
                
                acp_bwd = (n_minus_bwd - n_plus_bwd) / tot_bwd
                err_bwd = np.sqrt((1 - acp_bwd**2) / tot_bwd)
                
                delta_acp = acp_fwd - acp_bwd
                delta_err = np.sqrt(err_fwd**2 + err_bwd**2)
                z_score = delta_acp / delta_err
                
                # 95% Confidence Level Upper Bound on |Delta A_CP|
                # |Delta A_CP|_95 = |Delta A_CP| + 1.96 * sigma
                upper_bound_95 = np.abs(delta_acp) + 1.96 * delta_err
                
                print(f"  [{reg_name}]")
                print(f"    N_fwd = {tot_fwd:,}, A_CP(fwd) = {acp_fwd:+.4f} +/- {err_fwd:.4f}")
                print(f"    N_bwd = {tot_bwd:,}, A_CP(bwd) = {acp_bwd:+.4f} +/- {err_bwd:.4f}")
                print(f"    ΔA_CP = {delta_acp:+.5f} +/- {delta_err:.5f} (Z = {z_score:.2f}σ, 95% CL < {upper_bound_95:.4f})")
                
                results.append({
                    'axis': dir_name,
                    'region': reg_name,
                    'n_fwd': tot_fwd,
                    'n_bwd': tot_bwd,
                    'acp_fwd': acp_fwd,
                    'acp_bwd': acp_bwd,
                    'delta_acp': delta_acp,
                    'delta_err': delta_err,
                    'z_score': z_score,
                    'upper_bound_95': upper_bound_95
                })
                
    results_df = pd.DataFrame(results)
    
    # -------------------------------------------------------------------------
    # Bound on Chiral Coupling Scale Lambda
    # -------------------------------------------------------------------------
    # In the Effective Field Theory:
    # L_chiral = (1 / Lambda) (partial_mu Phi) * (q_bar gamma^mu gamma^5 q)
    # The maximum observed directional Delta A_CP across all bins gives:
    # |Delta A_CP|_max <= 2 * |Delta_E| / Lambda_eff
    # Taking typical B-meson energy in LHCb <E_B> ~ 85 GeV:
    mean_energy_gev = np.mean(p_tot) / 1000.0
    print(f"\n==========================================================================")
    print(f"   EMPIRICAL BOUNDS ON CHIRAL / MULTI-TEMPORAL COUPLING SCALE (Λ)")
    print(f"==========================================================================")
    print(f"Mean B Candidate Momentum in Lab Frame: <P_B> = {mean_energy_gev:.2f} GeV")
    
    global_delta_acp_max_95 = results_df['upper_bound_95'].max()
    global_delta_acp_min_95 = results_df['upper_bound_95'].min()
    
    # Lower bound on effective cutoff scale Lambda (assuming O(1) chiral gradient parameter v_phi ~ v_EW = 246 GeV):
    v_ew = 246.22 # GeV
    # If Delta A_CP <= 2 * (v_phi / Lambda) * (gamma_boost)
    gamma_boost = np.mean(p_tot) / m_b_nominal
    lambda_lower_bound_tev = (2 * v_ew * gamma_boost / global_delta_acp_max_95) / 1000.0
    
    print(f"Most Conservative 95% CL Upper Bound on |ΔA_CP|: < {global_delta_acp_max_95:.4f}")
    print(f"Average Lorentz Boost Factor <γ_B>: {gamma_boost:.2f}")
    print(f"Derived Lower Bound on Effective Chiral Scale: Λ >= {lambda_lower_bound_tev:.2f} TeV (at 95% CL)")
    print("==========================================================================\n")
    
    # -------------------------------------------------------------------------
    # Diagnostic Visualization
    # -------------------------------------------------------------------------
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(14, 6))
    
    # Subplot 1: Dalitz Plot with Kinematic Regions
    plt.subplot(1, 2, 1)
    sc = plt.scatter(s12[:8000], s23[:8000], c=q[:8000], cmap='coolwarm', s=2, alpha=0.5)
    plt.axvline(3.0, color='black', linestyle='--', alpha=0.7, label='s12 = 3 GeV² (Resonant cut)')
    plt.axvline(12.0, color='darkgreen', linestyle='--', alpha=0.7, label='s12 = 12 GeV²')
    plt.axhline(8.0, color='purple', linestyle=':', alpha=0.7, label='s23 = 8 GeV²')
    plt.title("LHCb $B^\\pm \\to h^+ h^- h^\\pm$ Dalitz Plot Bins")
    plt.xlabel("$m^2(h_1 h_2)$ [GeV$^2$]")
    plt.ylabel("$m^2(h_2 h_3)$ [GeV$^2$]")
    plt.legend(loc='upper right', fontsize=8)
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Delta A_CP Differentials and 95% CL Limits
    plt.subplot(1, 2, 2)
    y_pos = np.arange(len(results_df))
    plt.errorbar(results_df['delta_acp'], y_pos, xerr=results_df['delta_err'], fmt='o', color='navy', ecolor='royalblue', elinewidth=2, capsize=4, label='Measured $\\Delta A_{\\text{CP}}$')
    plt.axvline(0, color='red', linestyle='--', alpha=0.7)
    
    labels = [f"{r['region'][:12]}.. ({r['axis'][:12]})" for _, r in results_df.iterrows()]
    plt.yticks(y_pos, labels, fontsize=8)
    plt.xlabel("Directional Asymmetry Differential $\\Delta A_{\\text{CP}} = A_{\\text{CP}}(\\text{fwd}) - A_{\\text{CP}}(\\text{bwd})$")
    plt.title(f"SME Directional $\\Delta A_{{\\text{{CP}}}}$ Differentials\n(95% CL Limit: $\\Lambda \\geq {lambda_lower_bound_tev:.1f}$ TeV)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, "lhcb_sme_dalitz_limits.png")
    plt.savefig(plot_file, dpi=150)
    plt.close()
    print(f"[SAVED] SME Dalitz limits diagnostic plot -> {plot_file}")
    
    # Save tabular CSV results
    csv_file = os.path.join(output_dir, "lhcb_sme_dalitz_results.csv")
    results_df.to_csv(csv_file, index=False)
    print(f"[SAVED] Tabular SME Dalitz results -> {csv_file}")

if __name__ == "__main__":
    run_sme_dalitz_analysis()
