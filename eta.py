import numpy as np

def calculate_eta_from_W(W, u_W, d, u_d, l, u_l):
    """
    Calculate dynamic viscosity eta using Poiseuille's law:
        eta = (W * pi * d^4) / (128 * l)
    and propagate uncertainties from W, d, and l.
    
    Parameters:
        W (float): Flow resistance in Pa·s/m³
        u_W (float): Uncertainty of W
        d (float): Capillary inner diameter in meters
        u_d (float): Uncertainty of d
        l (float): Capillary length in meters
        u_l (float): Uncertainty of l
        
    Returns:
        eta_rounded (float): Rounded viscosity value
        u_eta_rounded (float): Rounded uncertainty
    """
    print("Viscosity Calculation (Poiseuille's Law)")
    print("----------------------------------------")

    # Input parameters
    print("\nInput parameters:")
    print(f"  Flow resistance W      = {W:.6e} ± {u_W:.3e}  Pa·s/m³")
    print(f"  Capillary diameter d   = {d:.6e} ± {u_d:.3e}  m")
    print(f"  Capillary length l     = {l:.6e} ± {u_l:.3e}  m")

    # Intermediate calculations
    d4 = d**4
    numerator = W * np.pi * d4
    denominator = 128 * l
    eta = numerator / denominator

    print("\nIntermediate steps:")
    print(f"  d^4 = ({d:.3e})^4 = {d4:.6e}  m^4")
    print(f"  Numerator = W * pi * d^4 = {numerator:.6e}  Pa·s")
    print(f"  Denominator = 128 * l = {denominator:.6e}  m")
    print(f"  eta = Numerator / Denominator = {eta:.6e}  Pa·s")

    # Relative uncertainties
    rel_u_W = u_W / W if W != 0 else 0.0
    rel_u_d = u_d / d if d != 0 else 0.0
    rel_u_l = u_l / l if l != 0 else 0.0

    rel_u_eta = np.sqrt(rel_u_W**2 + (4 * rel_u_d)**2 + rel_u_l**2)
    u_eta = eta * rel_u_eta

    print("\nUncertainty propagation:")
    print(f"  Relative uncertainty contributions:")
    print(f"    - W:       {rel_u_W * 100:.2f}%")
    print(f"    - d (×4):  {4 * rel_u_d * 100:.2f}%")
    print(f"    - l:       {rel_u_l * 100:.2f}%")
    print(f"  Total relative uncertainty = sqrt[({rel_u_W:.4f})^2 + ({4*rel_u_d:.4f})^2 + ({rel_u_l:.4f})^2] = {rel_u_eta * 100:.2f}%")
    print(f"  Absolute uncertainty u(eta) = {eta:.6e} × {rel_u_eta:.4f} = {u_eta:.6e}  Pa·s")

    # Rounding function
    def round_to_uncertainty(value, uncertainty):
        if uncertainty == 0:
            return value, 0
        from math import floor, log10
        exponent = floor(log10(abs(uncertainty)))
        mantissa = uncertainty / (10**exponent)
        digits = -exponent + (1 if mantissa < 3.55 else 0)
        u_rounded = round(uncertainty, digits)
        v_rounded = round(value, digits)
        return v_rounded, u_rounded

    eta_r, u_eta_r = round_to_uncertainty(eta, u_eta)
    print(f"\nFinal result (rounded):")
    print(f"  eta = ({eta_r:.3e} ± {u_eta_r:.1e})  Pa·s")

    return eta_r, u_eta_r


# ============================================================
# USER INPUT SECTION — Replace values with your experimental data
# ============================================================

if __name__ == "__main__":
    # Thin capillary data
    W_thin = 2.448e11        # Pa·s/m³
    u_W_thin = 0.009e11      # = 9e8
    d_thin = 0.32e-3         # m (0.32 mm)
    u_d_thin = 0.02e-3       # m (0.02 mm)
    l_thin = 28.05e-3        # m (28.05 mm)
    u_l_thin = 0.05e-3       # m (0.05 mm)

    print("Thin Capillary:")
    eta1, u_eta1 = calculate_eta_from_W(W_thin, u_W_thin, d_thin, u_d_thin, l_thin, u_l_thin)

    print("\n" + "-"*50 + "\n")

    # Thick capillary data
    W_thick = 1.24e11        # Pa·s/m³
    u_W_thick = 0.03e11      # = 3e9
    d_thick = 0.36e-3        # m
    u_d_thick = 0.02e-3      # m
    l_thick = 31.15e-3       # m
    u_l_thick = 0.05e-3      # m

    print("Thick Capillary:")
    eta2, u_eta2 = calculate_eta_from_W(W_thick, u_W_thick, d_thick, u_d_thick, l_thick, u_l_thick)

    # Comparison with literature
    eta_lit = 0.958e-3  # at 22°C
    print("\n" + "="*60)
    print("Comparison with literature value (water at 22°C):")
    print(f"  Literature eta = {eta_lit:.3e} Pa·s")
    print(f"  Thin:  ({eta1:.3e} ± {u_eta1:.1e}) → deviation = {(eta1/eta_lit - 1)*100:.1f}%")
    print(f"  Thick: ({eta2:.3e} ± {u_eta2:.1e}) → deviation = {(eta2/eta_lit - 1)*100:.1f}%")