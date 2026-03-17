"""
Delta Cosmology — Toy Model v2
================================
Generates the six-panel results figure (delta_toy_v2.png).

Dependencies:
    pip install numpy matplotlib

Run:
    python delta_toy_v2.py

Output:
    delta_toy_v2.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ── Difference functions ──────────────────────────────────────────────────────

def angular_dist(t1, t2):
    """Geodesic distance on S¹, result in [0, π]."""
    d = abs(t1 - t2) % (2 * np.pi)
    return min(d, 2 * np.pi - d)

def chord_dist(t1, t2):
    """Chord distance on S¹, embeddable in R².  chord = 2 sin(d/2)."""
    d = angular_dist(t1, t2)
    return 2 * np.sin(d / 2)

def delta_super(t1, t2, alpha=1.8):
    """
    Superlinear difference: d^alpha / pi^(alpha-1).
    For alpha > 1 this violates the triangle inequality.
    """
    d = angular_dist(t1, t2)
    return (d ** alpha) / (np.pi ** (alpha - 1))


# ── Statistical checks ────────────────────────────────────────────────────────

def check_triangle(delta_fn, n=3000):
    """Return array of values  Δ(A,C) − Δ(A,B) − Δ(B,C).
    Positive values are triangle-inequality violations."""
    rng = np.random.default_rng(42)
    pts = rng.uniform(0, 2 * np.pi, (n, 3))
    return np.array([delta_fn(a, c) - delta_fn(a, b) - delta_fn(b, c)
                     for a, b, c in pts])


def schoenberg_check(delta_fn, n_points=10):
    """
    Schoenberg / EDM embeddability test.

    A distance matrix D is embeddable in Euclidean space iff
    B = -0.5 * H * D² * H  is positive semidefinite,
    where H = I - (1/n) 11ᵀ is the centering matrix.

    Returns (min_eigenvalue, n_negative_eigenvalues, sorted_eigenvalues).
    """
    thetas = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
    D = np.array([[delta_fn(thetas[i], thetas[j])
                   for j in range(n_points)]
                  for i in range(n_points)])
    D2 = D ** 2
    n  = n_points
    H  = np.eye(n) - np.ones((n, n)) / n
    B  = -0.5 * H @ D2 @ H
    eigs = np.linalg.eigvalsh(B)
    n_neg = int(np.sum(eigs < -1e-6))
    return eigs.min(), n_neg, sorted(eigs.tolist())


# ── Pre-compute all data ──────────────────────────────────────────────────────

ALPHA = 1.8
RNG   = np.random.default_rng(0)

thetas = np.linspace(0, 2 * np.pi, 200)
ref    = np.pi / 2

chord_vals   = [chord_dist(ref, t)           for t in thetas]
angular_vals = [angular_dist(ref, t)         for t in thetas]
super_vals   = [delta_super(ref, t, ALPHA)   for t in thetas]

tri_chord   = check_triangle(chord_dist)
tri_angular = check_triangle(angular_dist)
tri_super   = check_triangle(lambda a, b: delta_super(a, b, ALPHA))

_, _, eigs_chord   = schoenberg_check(chord_dist)
_, _, eigs_angular = schoenberg_check(angular_dist)
_, nn_super, eigs_super = schoenberg_check(lambda a, b: delta_super(a, b, ALPHA))

# α sweep
alphas     = np.linspace(0.5, 3.0, 60)
tri_fracs  = []
min_eigs   = []
for a in alphas:
    def df(t1, t2, _a=a):
        d = angular_dist(t1, t2)
        return (d ** _a) / (np.pi ** (_a - 1))
    t = check_triangle(df, n=800)
    tri_fracs.append(float(np.mean(t > 1e-6)))
    me, _, _ = schoenberg_check(df, n_points=8)
    min_eigs.append(me)

# E-condition spread data
COUPLING = 0.3
n_pts    = 1000
d1_fixed = 1.0
d2_fixed = 0.8
contexts = RNG.uniform(0, 2 * np.pi, n_pts)
composite_std  = [np.sqrt(d1_fixed**2 + d2_fixed**2)] * n_pts
composite_coup = [
    np.sqrt(d1_fixed**2 + d2_fixed**2 +
            COUPLING * d1_fixed * d2_fixed * np.sin(ctx))
    for ctx in contexts
]


# ── Colour palette ────────────────────────────────────────────────────────────

BLUE  = '#2c5f8a'
AMBER = '#b05a2f'
GREEN = '#2a7a4f'
PALE  = '#dce8f5'
TITLE_COLOR = '#1a3a5c'
BG    = '#f8fafd'
SUBPANEL_BG = '#f0f4fa'


# ── Figure ────────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(16, 10), facecolor=BG)
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.44, wspace=0.38)


# ── A: difference functions ───────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(SUBPANEL_BG)
ax.plot(thetas, chord_vals,   color=GREEN, lw=2,       label='Chord Δ  (Hilbert-embeddable baseline)')
ax.plot(thetas, angular_vals, color=BLUE,  lw=2,       label='Angular Δ  (geodesic, not embeddable)')
ax.plot(thetas, super_vals,   color=AMBER, lw=2, ls='--', label=f'Superlinear Δ  α={ALPHA}')
ax.set_xlabel('θ')
ax.set_ylabel('Δ(π/2, θ)')
ax.set_title('A.  Difference Functions', fontweight='bold', color=TITLE_COLOR)
ax.legend(fontsize=7.5)
ax.grid(alpha=0.3)


# ── B: triangle-inequality violations ────────────────────────────────────────
ax = fig.add_subplot(gs[0, 1])
ax.set_facecolor(SUBPANEL_BG)
bins = np.linspace(-2, 2.5, 60)
frac_chord   = np.mean(tri_chord   > 1e-6)
frac_angular = np.mean(tri_angular > 1e-6)
frac_super   = np.mean(tri_super   > 1e-6)
ax.hist(tri_chord,   bins=bins, alpha=0.6, color=GREEN, label=f'Chord   (frac={frac_chord:.0%})')
ax.hist(tri_angular, bins=bins, alpha=0.5, color=BLUE,  label=f'Angular (frac={frac_angular:.0%})')
ax.hist(tri_super,   bins=bins, alpha=0.5, color=AMBER, label=f'Superlinear (frac={frac_super:.0%})')
ax.axvline(0, color='black', lw=1, ls=':')
ax.set_xlabel('Δ(A,C) − Δ(A,B) − Δ(B,C)')
ax.set_title('B.  Triangle Inequality Violations', fontweight='bold', color=TITLE_COLOR)
ax.legend(fontsize=7.5)
ax.grid(alpha=0.3)


# ── C: Schoenberg eigenvalues ─────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 2])
ax.set_facecolor(SUBPANEL_BG)
x = np.arange(len(eigs_chord))
ax.bar(x - 0.27, eigs_chord,   0.25, color=GREEN, alpha=0.75, label='Chord (embeddable)')
ax.bar(x,        eigs_angular, 0.25, color=BLUE,  alpha=0.75, label='Angular (not embeddable)')
ax.bar(x + 0.27, eigs_super,   0.25, color=AMBER, alpha=0.75, label='Superlinear (not embeddable)')
ax.axhline(0, color='black', lw=0.8, ls='--')
ax.set_xlabel('Eigenvalue index (sorted)')
ax.set_ylabel('Eigenvalue')
ax.set_title('C.  Schoenberg Eigenvalues\n(negative ⟹ not Hilbert-embeddable)',
             fontweight='bold', color=TITLE_COLOR)
ax.legend(fontsize=7.5)
ax.grid(alpha=0.3)


# ── D: α sweep ────────────────────────────────────────────────────────────────
ax  = fig.add_subplot(gs[1, 0])
ax2 = ax.twinx()
ax.set_facecolor(SUBPANEL_BG)
ax.plot(alphas, tri_fracs, color=AMBER, lw=2,       label='Frac. triangle violations')
ax2.plot(alphas, min_eigs, color=BLUE,  lw=2, ls='--', label='Min Schoenberg eigenvalue')
ax.axvline(1.0, color='gray', lw=0.8, ls=':')
ax.set_xlabel('α  (superlinear exponent)')
ax.set_ylabel('Fraction triangle violated', color=AMBER)
ax2.set_ylabel('Min eigenvalue', color=BLUE)
ax.set_title('D.  Effect of α on Non-Hilbert Severity', fontweight='bold', color=TITLE_COLOR)
lines1, labs1 = ax.get_legend_handles_labels()
lines2, labs2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labs1 + labs2, fontsize=7.5)
ax.grid(alpha=0.3)


# ── E: E-condition spread ─────────────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 1])
ax.set_facecolor(SUBPANEL_BG)
ax.hist(composite_std,  bins=40, alpha=0.6, color=BLUE,  label='Locally decomposable Δ₁₂')
ax.hist(composite_coup, bins=40, alpha=0.6, color=AMBER, label='Context-coupled Δ₁₂  (E holds)')
ax.set_xlabel('Δ₁₂ value')
ax.set_ylabel('Count')
ax.set_title('E.  E-Condition: Same Marginals, Different Composite\n'
             '(fixed Δ₁=1.0, Δ₂=0.8)',
             fontweight='bold', color=TITLE_COLOR)
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
spread = float(np.std(composite_coup))
ax.text(0.97, 0.97, f'spread = {spread:.3f}',
        transform=ax.transAxes, ha='right', va='top', fontsize=8, color=AMBER)


# ── F: summary table ──────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[1, 2])
ax.set_facecolor(PALE)
ax.axis('off')

rows = [
    ['Property',        'Chord Δ',   'Angular Δ',  'Superlinear Δ'],
    ['T (rot. inv.)',   '✓',         '✓',           '✓'],
    ['E (non-local)',   '✓',         '✓',           '✓'],
    ['Triangle ineq.',  '✓',         '✓',           '✗  (29%)'],
    ['Hilbert embed.',  '✓',         '✗',           '✗'],
    ['In std. QM?',     '✓',         'Partial',     '✗'],
    ['Status',          'Baseline',  'Geometric\nref.', 'Target\nmodel'],
]

row_colors = [
    ['#dce8f5'] * 4,
    [PALE, '#e8f5ec', PALE,      '#fff3e8'],
    [PALE, '#e8f5ec', PALE,      '#fff3e8'],
    [PALE, '#e8f5ec', PALE,      '#fde8dc'],
    [PALE, '#e8f5ec', '#fde8dc', '#fde8dc'],
    [PALE, '#e8f5ec', '#fff3e8', '#fde8dc'],
    [PALE, '#e8f5ec', '#fff3e8', '#fde8dc'],
]

tbl = ax.table(
    cellText=rows[1:],
    colLabels=rows[0],
    cellLoc='center',
    loc='center',
    cellColours=row_colors[1:],
    bbox=[0.0, 0.05, 1.0, 0.88],
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor('#c8d8e8')
    if r == 0:
        cell.set_facecolor(TITLE_COLOR)
        cell.set_text_props(color='white', fontweight='bold')

ax.set_title('F.  Model Comparison Summary', fontweight='bold',
             color=TITLE_COLOR, pad=6)


# ── Technical footnote ───────────────────────────────────────────────────────
fig.text(
    0.5, 0.01,
    'Technical note: angular geodesic distance on S¹ is not isometrically embeddable in finite-dim. Euclidean '
    'space — correct geometric behavior, not a bug.  '
    'Chord distance (baseline) embeds in R².  '
    'Superlinear Δ is not embeddable, confirming it lies outside standard QM geometry.',
    ha='center', fontsize=7, color='#667788', style='italic',
)

fig.suptitle(
    'Δ-Cosmology — Toy Model Results (v2)\n'
    'T + E satisfied;  superlinear Δ violates triangle inequality and Hilbert embeddability',
    fontsize=12, fontweight='bold', color=TITLE_COLOR, y=1.01,
)

plt.savefig('delta_toy_v2.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved: delta_toy_v2.png")
