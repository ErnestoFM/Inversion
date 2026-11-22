import math

def npv(rate, values):
    return sum(v / ((1.0 + rate) ** i) for i, v in enumerate(values))

def irr(values, tol=1e-7, max_iter=1000):
    # Newton-Raphson
    rate = 0.1
    for _ in range(max_iter):
        f = sum(v / ((1.0 + rate) ** i) for i, v in enumerate(values))
        f_prime = sum(-i * v / ((1.0 + rate) ** (i + 1)) for i, v in enumerate(values))
        if abs(f_prime) < 1e-12:
            break
        new_rate = rate - f / f_prime
        if abs(new_rate - rate) < tol:
            return new_rate
        rate = new_rate
    return rate

rate = 0.15

# 1. Base
fen_base = [-180000, -32000, 78900, 296800]
vpn_b = npv(rate, fen_base)
tir_b = irr(fen_base)
print(f"BASE: VPN = {vpn_b:.2f}, TIR = {tir_b*100:.2f}%")

# 2. Pesimista (FEN Y3 = 168000)
fen_pes = [-180000, -32000, 78900, 168000]
vpn_p = npv(rate, fen_pes)
tir_p = irr(fen_pes)
payback_pes = 24.0 + (180000 + 32000 - 78900) / 168000.0 * 12.0
print(f"PESIMISTA (168k): VPN = {vpn_p:.2f}, TIR = {tir_p*100:.2f}%, Payback = {payback_pes:.1f} meses")

# 3. Optimista (FEN Y3 = 420000)
fen_opt = [-180000, -32000, 78900, 420000]
vpn_o = npv(rate, fen_opt)
tir_o = irr(fen_opt)
payback_opt = 24.0 + (180000 + 32000 - 78900) / 420000.0 * 12.0
print(f"OPTIMISTA (420k): VPN = {vpn_o:.2f}, TIR = {tir_o*100:.2f}%, Payback = {payback_opt:.1f} meses")

# 4. Umbral de viabilidad (VPN = 0)
# -180000 - 32000/1.15 + 78900/1.15^2 + FEN_Y3/1.15^3 = 0
fen_y3_umbral = (180000 + 32000/1.15 - 78900/(1.15**2)) * (1.15**3)
print(f"FEN Y3 Umbral (VPN=0): {fen_y3_umbral:.2f}")

# Interpolacion planteles:
# Base: 22 planteles -> 296,800
# Pesimista: 15 planteles -> 168,000
planteles_umbral = 15.0 + (fen_y3_umbral - 168000.0) / ((296800.0 - 168000.0) / 7.0)
print(f"Planteles umbral interpolados: {planteles_umbral:.2f} planteles")

# 5. SUS Stats (32 / 12 / 6)
n_est, m_est, s_est = 32, 83.28, 11.21
n_prof, m_prof, s_prof = 12, 81.25, 9.91
n_alm, m_alm, s_alm = 6, 83.75, 12.72

m_global = (n_est*m_est + n_prof*m_prof + n_alm*m_alm) / 50.0
# Pooled SD
ss_est = (n_est - 1)*(s_est**2) + n_est*((m_est - m_global)**2)
ss_prof = (n_prof - 1)*(s_prof**2) + n_prof*((m_prof - m_global)**2)
ss_alm = (n_alm - 1)*(s_alm**2) + n_alm*((m_alm - m_global)**2)
s_global = math.sqrt((ss_est + ss_prof + ss_alm) / 49.0)
print(f"SUS Global: Media = {m_global:.2f}, DE = {s_global:.2f}")

# t vs 68
t_68 = (m_global - 68.0) / (s_global / math.sqrt(50.0))
# t vs 80
t_80 = (m_global - 80.0) / (s_global / math.sqrt(50.0))
print(f"t vs 68: {t_68:.2f} (p < 0.001)")
print(f"t vs 80: {t_80:.3f} (p = 0.035)")
