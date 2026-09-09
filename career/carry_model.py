"""
Carry model for a $5.5bn fund. European (whole-fund) waterfall: preferred return (hurdle) + full GP catch-up.
Simplifications: 90% of commitments invested evenly over 4 years; each deal held 5 years; fees on invested cost.
"""
FUND = 5_500.0            # $mn commitments
INVESTED = FUND * 0.90    # $mn actually invested

def irr(cf):
    def npv(r): return sum(c / (1 + r) ** t for t, c in enumerate(cf))
    lo, hi = -0.99, 1.0
    if npv(lo) * npv(hi) > 0: return float('nan')
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(mid) > 0: lo = mid
        else: hi = mid
    return mid

def fund(gross_irr, fee_rate=0.015, hurdle=0.08, carry_rate=0.20, invest_years=4, hold=5):
    T = invest_years + hold + 2
    contrib = [0.0]*T; fees = [0.0]*T; gross = [0.0]*T
    per = INVESTED / invest_years
    for y in range(1, invest_years+1):
        contrib[y] = per
        gross[y+hold] += per * (1+gross_irr)**hold
    for y in range(1, T):
        invested_so_far = per * min(y, invest_years)
        realized = per * max(0, min(y-hold, invest_years))
        fees[y] = fee_rate * (invested_so_far - realized)
    lp_out = [c+f for c, f in zip(contrib, fees)]
    paid_in = sum(lp_out); total_gross = sum(gross)
    profit = total_gross - paid_in
    def lp_irr_with_carry(c):
        dist = [g - c*g/total_gross for g in gross]
        return irr([-o+d for o, d in zip(lp_out, dist)])
    if profit <= 0:
        carry = 0.0
    else:
        full = carry_rate * profit
        if lp_irr_with_carry(full) >= hurdle: carry = full
        elif lp_irr_with_carry(0.0) < hurdle: carry = 0.0
        else:
            lo, hi = 0.0, full
            for _ in range(60):
                mid = (lo+hi)/2
                if lp_irr_with_carry(mid) >= hurdle: lo = mid
                else: hi = mid
            carry = lo
    dist = [g - carry*g/total_gross for g in gross] if total_gross else gross
    return dict(carry=carry, gross_moic=total_gross/INVESTED, lp_net_irr=lp_irr_with_carry(carry),
                lp_net_moic=sum(dist)/paid_in, profit=profit)

print("=== Fund-level carry pool, $5.5bn fund, 90% invested, 1.5% fee on invested cost, 4-yr deployment, 5-yr holds ===")
print(f"{'gross IRR':>9} {'carry':>6} {'hurdle':>6} {'grossMOIC':>9} {'LP net IRR':>10} {'LP net MOIC':>11} {'carry pool $mn':>14}")
for cr in (0.20, 0.10):
    for h in (0.08, 0.06):
        for g in (0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25):
            r = fund(g, hurdle=h, carry_rate=cr)
            print(f"{g:>9.0%} {cr:>6.0%} {h:>6.0%} {r['gross_moic']:>9.2f} {r['lp_net_irr']:>10.1%} {r['lp_net_moic']:>11.2f} {r['carry']:>14,.0f}")
        print()

print("=== Individual: nominal value of a slice of the carry pool, RMB mn (USD/CNY 7.1), 20% carry / 8% hurdle ===")
shares = [0.001, 0.002, 0.003, 0.005, 0.010, 0.020, 0.030]
print(f"{'gross IRR':>9} " + " ".join(f"{s:>8.1%}" for s in shares))
for g in (0.10, 0.12, 0.15, 0.20, 0.25):
    r = fund(g, hurdle=0.08, carry_rate=0.20)
    print(f"{g:>9.0%} " + " ".join(f"{r['carry']*s*7.1:>8,.1f}" for s in shares))
print()
print("=== Same, 10% carry / 8% hurdle ===")
print(f"{'gross IRR':>9} " + " ".join(f"{s:>8.1%}" for s in shares))
for g in (0.10, 0.12, 0.15, 0.20, 0.25):
    r = fund(g, hurdle=0.08, carry_rate=0.10)
    print(f"{g:>9.0%} " + " ".join(f"{r['carry']*s*7.1:>8,.1f}" for s in shares))

print()
print("=== Haircuts to turn nominal carry into today's expected value ===")
for yrs in (6, 7.5, 9):
    for rate in (0.08, 0.10, 0.12):
        print(f"paid in {yrs} yrs, discount {rate:.0%}: PV factor {1/(1+rate)**yrs:.2f}")
print("P(stay through vesting & realisation) 50-70%; P(fund clears hurdle | 10% target) maybe 50-60%")
for p_stay in (0.5, 0.6, 0.7):
    for p_perf in (0.5, 0.6, 0.8):
        print(f"  p_stay {p_stay:.0%} x p_perf {p_perf:.0%} x PV 0.49 = expected-PV multiplier {p_stay*p_perf*0.49:.2f}")
