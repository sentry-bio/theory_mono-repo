# The rate-tail law: readable depth of a distance reader under a site-rate spectrum

Derivation written 2026-10-14, before PREREG22 was registered or run. This note fixes the model, the two
readers, the exact finite-L prediction curves and the asymptotic exponents. It supersedes the §5.3 sentence of
Paper II vG that quoted an unarchived Gamma(0.5) run (0.39).

## 1. Model

Jukes–Cantor on four letters. Site i has rate r_i (mean 1 across sites). Along a path of duration ℓ the letter
correlation is λ_i(ℓ) = exp(−4 r_i ℓ / 3), and two letters at path length ℓ agree with probability

    p(ℓ) = 1/4 + (3/4) λ_i(ℓ).

(`same_letter_prob_four` in Window.lean is this identity with λ^d in place of λ(ℓ).)

The reading task is a quartet AB|CD at depth t: tips A, B hang at duration t below an internal node X, tips
C, D at duration t below Y, and X–Y is the internal branch of duration τ. Path lengths: AB = CD = 2t,
AC = AD = BC = BD = 2t + τ. Readable depth t*(L) is the largest t at which a reader of L sites returns the true
split with probability at least P₀ (registered: 0.90).

Depth is measured in expected substitutions per site at the mean rate. The internal branch τ is fixed
(registered: τ = 1.0) so that at the depths of interest t ≫ τ and the deep signal is linear in τ.

## 2. Per-site signal and variance (exact)

Let λ₁ = λ_i(2t), λ₂ = λ_i(2t+τ), p₁ = 1/4 + 3λ₁/4, p₂ = 1/4 + 3λ₂/4. The per-site contrast between a
within-pair and a cross-pair agreement indicator is

    s_i(t) = p₁ − p₂ = (3/4) e^{−8 r_i t/3} (1 − e^{−4 r_i τ/3}).

In the Z₂×Z₂ coordinates of Jukes–Cantor, A⊕B and A⊕C are U⊕V and U⊕W with U, V, W independent noises on
paths of duration t, t, t+τ. Writing P₀(ℓ) = 1/4 + 3λ(ℓ)/4 and P₁(ℓ) = (1 − λ(ℓ))/4,

    q_i = P(A=B and A=C) = P₀(t)² P₀(t+τ) + 3 P₁(t)² P₁(t+τ),
    v_i(t) = Var[1(A=B) − 1(A=C)] = p₁(1−p₁) + p₂(1−p₂) − 2 (q_i − p₁ p₂).

Both are closed forms in r_i, t, τ. For the sites that carry the signal at depth t (r_i t = O(1)) v_i is
O(1) and bounded away from zero.

## 3. Two readers

**Unweighted mismatch reader.** T = Σ_i [1(A_i=B_i) − 1(A_i=C_i)] (and the analogous contrasts for the two
competing splits). E T = L·E_r[s], Var T = L·E_r[v], so

    SNR_u(L, t) = √L · E_r[s(t)] / √(E_r[v(t)]).

**Rate-weighted contrast reader.** T_w = Σ_i w_i [1(A_i=B_i) − 1(A_i=C_i)] with the optimal linear weights
w_i = s_i/v_i (the reader knows r_i and t; in simulation these are oracle values, on real data they are
estimates). Then

    SNR_w(L, t)² = L · E_r[s(t)² / v(t)].

Both expectations are over the site-rate distribution. Either SNR is a monotone decreasing function of t, and
t*(L) is the solution of SNR(L, t) = κ, where κ is a single reader-specific constant set by the success criterion
(κ ≈ Φ⁻¹(P₀) under the Gaussian approximation, corrected for the three-way decision). κ is the only nuisance
constant; the registration fits it once per reader on one cell and predicts every other cell with no free
parameter.

## 4. Site-rate spectrum and the exponents

Gamma(a) with mean 1 has density ∝ r^{a−1} e^{−a r} and Laplace transform

    E[e^{−s r}] = (1 + s/a)^{−a},   E[r e^{−s r}] = (1 + s/a)^{−(a+1)},   E[r² e^{−s r}] = ((a+1)/a)(1 + s/a)^{−(a+2)}.

For t ≫ τ the sites that matter have r τ ≪ 1, so s ≈ r τ e^{−8rt/3}, and v is a constant across them:

* unweighted:  SNR_u ∝ √L · E[r e^{−8rt/3}] = √L (1 + 8t/(3a))^{−(a+1)}, so
  **t*_u(L) ≍ L^{1/(2(a+1))}**;
* rate-weighted: SNR_w² ∝ L · E[r² e^{−16rt/3}] ∝ L (1 + 16t/(3a))^{−(a+2)}, so
  **t*_w(L) ≍ L^{1/(a+2)}**.

The two exponents differ because the weighted reader's information is a second moment in r (a sum of squared
per-site contrasts) while the unweighted reader's signal is a first moment; the density of slow sites near
r = 0, ∝ r^{a−1}, sets both. The weighted reader always reads deeper: 1/(a+2) > 1/(2(a+1)) for every finite a.

Uniform rates (a → ∞): (1 + s/a)^{−a} → e^{−s}, and both readers give

    t*(L) = (3/16) ln L + const,

the logarithmic horizon; the readers agree. This is the e^{−16rt/3} Fisher decay of Paper II §5.3 and is the
sequence-space form of the Erdős–Steel–Székely–Warnow logarithmic depth law for distance methods.

Numerical values of the asymptotic exponents:

| a | unweighted 1/(2(a+1)) | weighted 1/(a+2) |
|---|---|---|
| 0.5 | 0.333 | 0.400 |
| 1.0 | 0.250 | 0.333 |
| 2.0 | 0.167 | 0.250 |
| ∞ | log, slope 3/16 in ln L | log, slope 3/16 in ln L |

## 5. The exact finite-L curves (what the registration tests)

The asymptotic exponent is reached slowly: with the "−1" of (1 + 8t/(3a))^{a+1} = C√L the local log–log slope
over L = 256…32768 lies above the asymptote by 0.01–0.05 depending on κ and τ. So the registered test is of the
**exact curve**, not of a fitted slope: with κ fitted on one cell, t*(L) is predicted by solving SNR(L, t) = κ
using the exact s_i, v_i of §2 integrated over Gamma(a) by quadrature. The local slopes are reported as
readings beside the asymptotic exponents.

## 6. What this law is and is not

It is the law of a **distance (quartet) reader**: a fixed-size reader of pairwise contrasts. It is the
sequence-space statement of the one inequality of the program (deep cousins must stay farther apart than near
ones) measured against sampling noise over L sites. It is **not** the Kesten–Stigum threshold, which concerns a
census reader that pools exponentially many leaves and is governed by the second moment bλ² = 1; that
threshold is the ceiling over all readers and is kept separate (Paper II §5.4).

## 7. Which reader did the earlier run realise?

The earlier Gamma(0.5) run (exponent 0.39) has no archived script. 0.39 sits at the weighted asymptote (0.400)
and well above the unweighted one (0.333), but §5 shows a pre-asymptotic unweighted slope can also reach
0.36–0.38 at moderate L, so the run cannot be assigned to a reader after the fact. It is superseded by
PREREG22, which separates the readers by construction.
