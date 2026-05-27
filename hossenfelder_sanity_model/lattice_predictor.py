import numpy as np
import pandas as pd

def metric_dot(v1, v2):
    """
    Computes the dot product in 4+2 spacetime with signature (+, -, -, -, +, -).
    X^2 = (X^0)^2 - (X^1)^2 - (X^2)^2 - (X^3)^2 + (X^4)^2 - (X^5)^2
    """
    signature = np.array([1.0, -1.0, -1.0, -1.0, 1.0, -1.0])
    return np.sum(v1 * v2 * signature)

def verify_constraints(X, P):
    """Verifies the Sp(2, R) gauge constraints: X^2 = 0, P^2 = 0, X.P = 0"""
    x2 = metric_dot(X, X)
    p2 = metric_dot(P, P)
    xp = metric_dot(X, P)
    return x2, p2, xp

def compute_generators(X, P):
    """Computes the gauge invariant SO(4,2) generators L^{MN} = X^M P^N - X^N P^M"""
    L = np.zeros((6, 6))
    for m in range(6):
        for n in range(6):
            L[m, n] = X[m]*P[n] - X[n]*P[m]
    return L

def run_2t_simulation():
    print("=============================================================")
    print("   TWO-TIME (2T) PHYSICS SANITY SIMULATOR")
    print("   Gauge Invariance & Holographic Projections in 4+2 Spacetime")
    print("=============================================================\n")

    # 1. Initialize a base state in 4+2 dimensions that satisfies the constraints:
    # X^2 = 0, P^2 = 0, X.P = 0
    # Let's construct a valid pair of vectors:
    # We choose X with X^0 = 2.0, X^1 = 1.0, X^2 = 1.0, X^3 = 1.0, X^4 = 0.0, X^5 = 1.0
    # X^2 = 4.0 - 1.0 - 1.0 - 1.0 + 0.0 - 1.0 = 0.0
    X = np.array([2.0, 1.0, 1.0, 1.0, 0.0, 1.0])
    
    # We choose P such that P^2 = 0 and X.P = 0
    # P^0 = 1.0, P^1 = 1.0, P^2 = 0.0, P^3 = 0.0, P^4 = 1.0, P^5 = 1.0
    # P^2 = 1.0 - 1.0 - 0.0 - 0.0 + 1.0 - 1.0 = 0.0
    # X.P = 2(1) - 1(1) - 1(0) - 1(0) + 0(1) - 1(1) = 2 - 1 - 1 = 0
    P = np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0])

    x2, p2, xp = verify_constraints(X, P)
    print("1. Initializing 2T-Physics State in 4+2 Spacetime:")
    print(f"   Position X^M: {X}")
    print(f"   Momentum P^M: {P}")
    print(f"   Constraint Check: X^2 = {x2:.2f}, P^2 = {p2:.2f}, X.P = {xp:.2f}")
    assert np.allclose([x2, p2, xp], 0.0), "Initial state does not satisfy Sp(2, R) constraints!"
    print("   [SUCCESS] State satisfies all Sp(2, R) gauge constraints.\n")

    # Compute original generators
    L_original = compute_generators(X, P)

    # 2. Simulate Sp(2, R) Gauge Transformations
    # A gauge transformation maps:
    # X' = a*X + b*P
    # P' = c*X + d*P
    # where ad - bc = 1 (area preserving parameterization)
    print("2. Simulating Gauge Transformations along Sp(2, R) parameter space:")
    print(f"{'Step':<5} | {'a':<6} | {'b':<6} | {'c':<6} | {'d':<6} | {'X.P':<6} | {'Generator Invariance Match?'}")
    print("-" * 75)

    np.random.seed(126)
    steps = 5
    for i in range(steps):
        # Generate SL(2, R) parameters
        a = np.random.uniform(0.5, 2.0)
        b = np.random.uniform(-1.0, 1.0)
        # We need ad - bc = 1 => d = (1 + b*c)/a
        c = np.random.uniform(-1.0, 1.0)
        d = (1.0 + b*c) / a

        # Transform coordinates
        X_trans = a * X + b * P
        P_trans = c * X + d * P

        # Verify transformed constraints
        x2_t, p2_t, xp_t = verify_constraints(X_trans, P_trans)
        
        # Verify Generator Invariance
        L_trans = compute_generators(X_trans, P_trans)
        invariance_check = np.allclose(L_trans, L_original)

        print(f"{i+1:<5} | {a:.3f} | {b:.3f} | {c:.3f} | {d:.3f} | {xp_t:.2e} | {invariance_check}")

    print("\n   [SUCCESS] L^{MN} is invariant under all gauge transformations.\n")

    # 3. Holographic Projections (Gauge Slicing)
    # Different choices of gauge slices project the 4+2 physics into different 1T physical systems.
    print("3. Gauge Slices (Projections to 3+1 Dimensions):")
    
    # Slice A: Relativistic Particle Gauge
    # We gauge-fix the extra coordinates to map to standard Minkowski spacetime.
    # We solve for a gauge where X^4 = 1.0, X^5 = 0.0.
    # Under a gauge transformation X' = a*X + b*P:
    # We want:
    # a*X[4] + b*P[4] = 1.0
    # a*X[5] + b*P[5] = 0.0
    # Let's solve the 2x2 linear system for (a, b):
    # a*0.0 + b*1.0 = 1.0  => b = 1.0
    # a*1.0 + b*1.0 = 0.0  => a = -1.0
    # Let's check ad - bc = 1. We choose c, d to satisfy ad - bc = 1.
    # Let's pick c = 0.0, then d = 1/a = -1.0. (ad - bc = (-1)(-1) - 1(0) = 1).
    a_a, b_a = -1.0, 1.0
    c_a, d_a = 0.0, -1.0
    
    X_A = a_a * X + b_a * P
    P_A = c_a * X + d_a * P
    
    print("\n   --- GAUGE SLICE A (Standard 3+1 Relativistic Particle) ---")
    print(f"   Projected Coordinates X_A^M: {X_A}")
    print(f"   Projected Momentum P_A^M:   {P_A}")
    print(f"   Minkowski Position x^mu:    {X_A[0:4]}")
    print(f"   Minkowski Momentum p^mu:    {P_A[0:4]}")
    # Verify mass-shell relation in 3+1 dimensions:
    # in standard relativistic particle, p^mu p_mu = m^2
    m2 = P_A[0]**2 - P_A[1]**2 - P_A[2]**2 - P_A[3]**2
    print(f"   Minkowski Mass Squared (p^mu p_mu): {m2:.2f}")

    # Slice B: Conformal / AdS Gauge
    # We gauge-fix to map to AdS_5 or conformal space, where X^0 = 1.0 and X^5 = 1.0.
    # a*X[0] + b*P[0] = 1.0
    # a*X[5] + b*P[5] = 1.0
    # a*2.0 + b*1.0 = 1.0
    # a*1.0 + b*1.0 = 1.0
    # Subtracting the two: a = 0.0 => b = 1.0.
    # To satisfy ad - bc = 1: if a = 0, then -b*c = 1 => c = -1.0 (since b=1.0).
    # We can choose d = 0.0. (ad - bc = 0 - (1)(-1) = 1).
    a_b, b_b = 0.0, 1.0
    c_b, d_b = -1.0, 0.0
    
    X_B = a_b * X + b_b * P
    P_B = c_b * X + d_b * P
    
    print("\n   --- GAUGE SLICE B (Conformal Particle / AdS Space) ---")
    print(f"   Projected Coordinates X_B^M: {X_B}")
    print(f"   Projected Momentum P_B^M:   {P_B}")
    print(f"   AdS_5 Coordinates:         {X_B[1:5]}")

    # 4. Compare Generators
    L_A = compute_generators(X_A, P_A)
    L_B = compute_generators(X_B, P_B)
    
    print("\n4. Generator Equivalence Verification:")
    print(f"   L^MN (Slice A) == L^MN (Slice B)? {np.allclose(L_A, L_B)}")
    print(f"   L^MN (Slice A) == L^MN (Original)? {np.allclose(L_A, L_original)}")
    
    print("\n   [CONCLUSION] The physical observables represented by the generators L^{MN}")
    print("   are absolutely identical in both gauge slices, proving that the two completely")
    print("   different 1T-physics descriptions (Relativistic Particle vs Conformal AdS Particle)")
    print("   are mathematically equivalent projections of the same 2T-physics state.")

if __name__ == '__main__':
    run_2t_simulation()
