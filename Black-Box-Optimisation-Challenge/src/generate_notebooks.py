"""
generate_notebooks.py — Dibyajyoti Pradhan
Generates one Jupyter notebook per BBO function (F1–F8).
Run from the Black-Box-Optimisation-Challenge/ root:
    python src/generate_notebooks.py
"""

import json
import os

# ─── Function metadata ─────────────────────────────────────────────────────────
FUNCTIONS = {
    1: {"dims": 2,  "n_init": 10, "beta": 2.0,  "trust_r": None,   "lhs_n": 500_000,
        "note": "Near-zero outputs throughout all rounds. Exploring new region."},
    2: {"dims": 2,  "n_init": 10, "beta": 0.5,  "trust_r": 0.08,   "lhs_n": 500_000,
        "note": "Moderate, gradually improving. Continue directional drift."},
    3: {"dims": 3,  "n_init": 15, "beta": 0.5,  "trust_r": 0.06,   "lhs_n": 1_000_000,
        "note": "Gradual improvement along consistent trajectory."},
    4: {"dims": 4,  "n_init": 30, "beta": 0.2,  "trust_r": 0.05,   "lhs_n": 2_000_000,
        "note": "Converging cluster with consistent gains. Tight local refinement."},
    5: {"dims": 4,  "n_init": 20, "beta": 0.02, "trust_r": 0.04,   "lhs_n": 2_000_000,
        "note": "Strong ridge near boundary (1600+). Heavy exploitation."},
    6: {"dims": 5,  "n_init": 20, "beta": 0.3,  "trust_r": 0.06,   "lhs_n": 3_000_000,
        "note": "Noisy, moderate. Conservative GP-guided refinement."},
    7: {"dims": 6,  "n_init": 30, "beta": 3.0,  "trust_r": None,   "lhs_n": 5_000_000,
        "note": "Plateau, uncertain. Probing undersampled region."},
    8: {"dims": 8,  "n_init": 40, "beta": 0.02, "trust_r": 0.04,   "lhs_n": 9_500_000,
        "note": "High output. X1, X3 dominant. Gradient ascent in pseudo-2D."},
}

# ─── Known queries from Round 10 (capstone_component_21_1) ────────────────────
R10_QUERIES = {
    1: [0.483291, 0.716842],
    2: [0.621478, 0.304591],
    3: [0.712046, 0.483712, 0.591834],
    4: [0.568923, 0.731045, 0.412867, 0.350000],   # corrected to 4D
    5: [0.952841, 0.073621, 0.837492, 0.961074],
    6: [0.683741, 0.512894, 0.749213, 0.384521, 0.621843],
    7: [0.412847, 0.718934, 0.519283, 0.384712, 0.623891, 0.571234],
    8: [0.847213, 0.492381, 0.913847, 0.381274, 0.512847, 0.673821, 0.428137, 0.591284],
}

# ─── Known queries from Round 11 (capstone_component_22_1) ────────────────────
R11_QUERIES = {
    1: [0.152834, 0.341729],
    2: [0.648213, 0.283047],
    3: [0.728491, 0.467038, 0.608217],
    4: [0.574812, 0.748391, 0.427963, 0.365000],   # corrected to 4D
    5: [0.961283, 0.058174, 0.851293, 0.972418],
    6: [0.697234, 0.528471, 0.762841, 0.371893, 0.637524],
    7: [0.213847, 0.492183, 0.678341, 0.147293, 0.831472, 0.392841],
    8: [0.871492, 0.496738, 0.934821, 0.378413, 0.507829, 0.671384, 0.432817, 0.586941],
}


# ─── Cell builders ─────────────────────────────────────────────────────────────
def md_cell(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def build_notebook(fn: int, meta: dict) -> dict:
    dims = meta["dims"]
    beta = meta["beta"]
    trust_r = meta["trust_r"]
    lhs_n = meta["lhs_n"]
    note = meta["note"]
    r10 = R10_QUERIES[fn]
    r11 = R11_QUERIES[fn]

    trust_kwarg = f"trust_region_radius={trust_r}" if trust_r else "trust_region_radius=None"
    dim_labels = ", ".join([f"X{i+1}" for i in range(dims)])

    cells = []

    # ── Title ────────────────────────────────────────────────────────────────
    cells.append(md_cell(
        f"# Bayesian Optimisation — Function {fn} ({dims}D)\n\n"
        f"**Author:** Dibyajyoti Pradhan  \n"
        f"**Programme:** Imperial College London Professional Certificate in ML/AI  \n"
        f"**Module:** BBO Capstone (Modules 12–22)  \n\n"
        f"**Strategy note:** {note}"
    ))

    # ── Imports ───────────────────────────────────────────────────────────────
    cells.append(md_cell("## 1. Imports"))
    cells.append(code_cell(
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import sys\n"
        "import os\n\n"
        "# Add src/ to path for reusable utilities\n"
        "sys.path.append(os.path.join(os.getcwd(), '..', 'src'))\n"
        "from bbo_utils import (\n"
        "    lhs_candidates, fit_gp, gp_posterior,\n"
        "    ucb_acquisition, suggest_next_query,\n"
        "    dimension_sensitivity, plot_running_best,\n"
        + ("    plot_gp_surface_2d,\n" if dims == 2 else "") +
        ")\n\n"
        "np.random.seed(42)"
    ))

    # ── Load initial data ─────────────────────────────────────────────────────
    cells.append(md_cell("## 2. Load Initial Data\n\nInitial observations provided at the start of the BBO challenge."))
    cells.append(code_cell(
        f"data_dir = os.path.join('..', 'data', 'initial_data', 'function_{fn}')\n\n"
        f"X_init = np.load(os.path.join(data_dir, 'initial_inputs.npy'))\n"
        f"y_init = np.load(os.path.join(data_dir, 'initial_outputs.npy'))\n\n"
        f"print(f'Initial inputs shape:  {{X_init.shape}}')\n"
        f"print(f'Initial outputs shape: {{y_init.shape}}')\n"
        f"print(f'Output range: [{{y_init.min():.6f}}, {{y_init.max():.6f}}]')\n"
        f"print(f'Best initial output:   {{y_init.max():.6f}}')\n"
        f"print(f'Best initial input:    {{X_init[np.argmax(y_init)]}}')"
    ))

    # ── Add subsequent queries ────────────────────────────────────────────────
    cells.append(md_cell(
        "## 3. Add Subsequent Query Data\n\n"
        "Queries accumulated across Rounds 1–11.  \n"
        "Round 10 coordinates from `capstone_component_21_1_bbo_round_10.md`  \n"
        "Round 11 coordinates from `capstone_component_22_1_bbo_round_11.md`\n\n"
        "> **Note:** Rounds 1–9 are documented in the weekly strategy markdown files. "
        "Their specific coordinates should be appended here once retrieved from the BBO portal."
    ))
    cells.append(code_cell(
        f"# Round 10 query\n"
        f"x_r10 = np.array([{', '.join(str(v) for v in r10)}])\n\n"
        f"# Round 11 query\n"
        f"x_r11 = np.array([{', '.join(str(v) for v in r11)}])\n\n"
        f"# Placeholder outputs — replace with actual portal results\n"
        f"# When you have the actual values, update these:\n"
        f"y_r10 = np.float64(0.0)   # TODO: replace with actual R10 output\n"
        f"y_r11 = np.float64(0.0)   # TODO: replace with actual R11 output\n\n"
        f"X_train = np.vstack([X_init,\n"
        f"                     x_r10.reshape(1, -1),\n"
        f"                     x_r11.reshape(1, -1)])\n"
        f"y_train = np.append(y_init, [y_r10, y_r11])\n\n"
        f"print(f'Total observations: {{len(y_train)}}')\n"
        f"print(f'Best observed output: {{y_train.max():.6f}}')\n"
        f"print(f'Best observed input:  {{X_train[np.argmax(y_train)]}}')"
    ))

    # ── Data exploration ──────────────────────────────────────────────────────
    cells.append(md_cell("## 4. Data Exploration"))
    cells.append(code_cell(
        "print('Output statistics:')\n"
        "print(f'  Min:  {y_train.min():.6f}')\n"
        "print(f'  Max:  {y_train.max():.6f}')\n"
        "print(f'  Mean: {y_train.mean():.6f}')\n"
        "print(f'  Std:  {y_train.std():.6f}')\n\n"
        "# Running best across all observations\n"
        f"plot_running_best(y_train, title='Function {fn} — Running Best Output')"
    ))

    if dims == 2:
        cells.append(code_cell(
            "# 2D scatter of observed points\n"
            "plt.figure(figsize=(7, 6))\n"
            "sc = plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train,\n"
            "                 cmap='viridis', s=80, edgecolors='k')\n"
            "plt.colorbar(sc, label='Output value')\n"
            f"plt.xlabel('X₁'); plt.ylabel('X₂')\n"
            f"plt.title('Function {fn} — Observed Query Points')\n"
            "plt.grid(True); plt.tight_layout(); plt.show()"
        ))

    # ── Correlation / dimension analysis for high-D ───────────────────────────
    if dims >= 4:
        cells.append(md_cell(
            "### Dimension–Output Correlation\n\n"
            "For high-dimensional functions, identifying influential dimensions "
            "allows pseudo-dimensionality reduction (fixing low-influence inputs)."
        ))
        cells.append(code_cell(
            "correlations = np.array([\n"
            "    np.corrcoef(X_train[:, i], y_train)[0, 1]\n"
            "    for i in range(X_train.shape[1])\n"
            "])\n\n"
            "plt.figure(figsize=(8, 4))\n"
            f"plt.bar([f'X{{i+1}}' for i in range({dims})], correlations, color='steelblue')\n"
            "plt.axhline(0, color='k', linewidth=0.8)\n"
            "plt.ylabel('Pearson r with output')\n"
            f"plt.title('Function {fn} — Dimension-Output Correlation')\n"
            "plt.grid(axis='y'); plt.tight_layout(); plt.show()\n\n"
            f"print('Correlations ({dim_labels}):')\n"
            "for i, r in enumerate(correlations):\n"
            f"    print(f'  X{{i+1}}: {{r:.4f}}')"
        ))

    # ── Bayesian Optimisation ─────────────────────────────────────────────────
    cells.append(md_cell(
        f"## 5. Bayesian Optimisation (UCB, β={beta})\n\n"
        f"Strategy: {'exploitation-heavy (trust region ±' + str(trust_r) + ')' if trust_r else 'exploration-heavy (no trust region)'}"
    ))
    cells.append(code_cell(
        "next_query, fitted_model = suggest_next_query(\n"
        "    X_train=X_train,\n"
        "    y_train=y_train,\n"
        f"    n_candidates={lhs_n:_},\n"
        f"    beta={beta},\n"
        "    length_scale=0.1,\n"
        "    noise_level=1e-6,\n"
        "    fit_noise=True,\n"
        f"    {trust_kwarg},\n"
        "    seed=42,\n"
        ")\n\n"
        "# Format to 6 decimal places (BBO portal requirement)\n"
        "coords = ', '.join(f'{v:.6f}' for v in next_query)\n"
        f"print(f'Round 12 suggested query for Function {fn}:')\n"
        "print(f'  ({coords})')"
    ))

    if dims == 2:
        cells.append(code_cell(
            f"# Visualise GP posterior\n"
            f"plot_gp_surface_2d(\n"
            f"    model=fitted_model,\n"
            f"    X_train=X_train,\n"
            f"    y_train=y_train,\n"
            f"    next_query=next_query,\n"
            f"    title='Function {fn}',\n"
            f")"
        ))

    # ── Dimension sensitivity for high-D ──────────────────────────────────────
    if dims >= 4:
        cells.append(md_cell(
            "### Dimension Sensitivity (Finite-Difference Gradients)\n\n"
            "Identifies which input dimensions most strongly influence "
            "the GP predicted mean at the current best point."
        ))
        cells.append(code_cell(
            "best_x = X_train[np.argmax(y_train)]\n"
            "sensitivity = dimension_sensitivity(fitted_model, best_x, delta=0.01)\n\n"
            "plt.figure(figsize=(8, 4))\n"
            f"plt.bar([f'X{{i+1}}' for i in range({dims})], sensitivity, color='tomato')\n"
            "plt.axhline(0, color='k', linewidth=0.8)\n"
            "plt.ylabel('∂μ/∂xᵢ  (GP mean gradient)')\n"
            f"plt.title('Function {fn} — Dimension Sensitivity at Best Point')\n"
            "plt.grid(axis='y'); plt.tight_layout(); plt.show()\n\n"
            "print('Sensitivity at best point:')\n"
            "for i, g in enumerate(sensitivity):\n"
            f"    print(f'  X{{i+1}}: {{g:+.4f}}')"
        ))

    # ── Summary ───────────────────────────────────────────────────────────────
    cells.append(md_cell(
        f"## 6. Round 12 Strategy Summary\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| Function | F{fn} ({dims}D) |\n"
        f"| Total observations | n/a (computed above) |\n"
        f"| Acquisition | UCB, β={beta} |\n"
        f"| Trust region | {'±' + str(trust_r) + ' per dim' if trust_r else 'None (exploration)'} |\n"
        f"| Strategy | {note} |\n\n"
        f"> Submit the coordinates printed above via the BBO portal. "
        f"All inputs must be in `[0, 1)` to 6 decimal places."
    ))

    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0",
            },
        },
        "cells": cells,
    }
    return nb


# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "notebooks")
    os.makedirs(out_dir, exist_ok=True)

    for fn, meta in FUNCTIONS.items():
        nb = build_notebook(fn, meta)
        path = os.path.join(out_dir, f"bbo_function_{fn}.ipynb")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"Created: {path}")

    print("\nAll 8 notebooks generated successfully.")
