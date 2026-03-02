"""
BBO Utility Functions — Dibyajyoti Pradhan
Imperial College London Professional Certificate in ML/AI
Black-Box Optimisation Capstone (Modules 12–22)

Reusable functions for Gaussian Process surrogate fitting,
UCB acquisition, Latin Hypercube candidate generation,
and query logging across all eight unknown functions.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from scipy.stats import qmc


# ---------------------------------------------------------------------------
# Candidate generation
# ---------------------------------------------------------------------------

def lhs_candidates(n_dims: int, n_samples: int, seed: int = 42) -> np.ndarray:
    """
    Generate candidate points via Latin Hypercube Sampling.

    For low-dimensional functions (d <= 3) a full grid is feasible;
    for d >= 4 LHS provides better coverage than random sampling
    within the same budget.

    Parameters
    ----------
    n_dims   : input dimensionality
    n_samples: number of candidate points
    seed     : random seed for reproducibility

    Returns
    -------
    np.ndarray of shape (n_samples, n_dims), values in [0, 1)
    """
    sampler = qmc.LatinHypercube(d=n_dims, seed=seed)
    return sampler.random(n=n_samples)


def grid_candidates(n_dims: int, resolution: int = 101) -> np.ndarray:
    """
    Generate a full regular grid for low-dimensional functions (d <= 3).

    Parameters
    ----------
    n_dims    : input dimensionality (use only for d <= 3)
    resolution: points per dimension

    Returns
    -------
    np.ndarray of shape (resolution**n_dims, n_dims)
    """
    axes = [np.linspace(0, 1, resolution)] * n_dims
    grids = np.meshgrid(*axes, indexing='ij')
    return np.column_stack([g.ravel() for g in grids])


# ---------------------------------------------------------------------------
# Gaussian Process surrogate
# ---------------------------------------------------------------------------

def fit_gp(
    X_train: np.ndarray,
    y_train: np.ndarray,
    length_scale: float = 0.1,
    noise_level: float = 1e-6,
    fit_noise: bool = True,
) -> GaussianProcessRegressor:
    """
    Fit a Gaussian Process with RBF (+optional WhiteKernel noise) kernel.

    Parameters
    ----------
    X_train     : training inputs  (n, d)
    y_train     : training outputs (n,)
    length_scale: initial RBF length-scale per dimension
    noise_level : initial WhiteKernel noise level
    fit_noise   : if True, include WhiteKernel for noise-aware fitting

    Returns
    -------
    Fitted GaussianProcessRegressor
    """
    n_dims = X_train.shape[1]
    ls = [length_scale] * n_dims
    kernel = RBF(length_scale=ls, length_scale_bounds='fixed')
    if fit_noise:
        kernel = kernel + WhiteKernel(noise_level=noise_level)

    model = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    model.fit(X_train, y_train.reshape(-1, 1))
    return model


def gp_posterior(
    model: GaussianProcessRegressor,
    X_candidates: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return posterior mean and standard deviation over candidate points.

    Parameters
    ----------
    model       : fitted GaussianProcessRegressor
    X_candidates: candidate inputs (m, d)

    Returns
    -------
    mean (m,), std (m,)
    """
    mean, std = model.predict(X_candidates, return_std=True)
    return mean.ravel(), std.ravel()


# ---------------------------------------------------------------------------
# Acquisition functions
# ---------------------------------------------------------------------------

def ucb_acquisition(mean: np.ndarray, std: np.ndarray, beta: float = 0.02) -> np.ndarray:
    """
    Upper Confidence Bound acquisition: UCB(x) = μ(x) + β·σ(x)

    Low β  → exploitation-heavy (converging functions: F4, F5, F8)
    High β → exploration-heavy (stagnant functions: F1, F7)

    Parameters
    ----------
    mean : posterior mean  (m,)
    std  : posterior std   (m,)
    beta : exploration weight

    Returns
    -------
    acquisition values (m,)
    """
    return mean + beta * std


def suggest_next_query(
    X_train: np.ndarray,
    y_train: np.ndarray,
    n_candidates: int = 500_000,
    beta: float = 0.02,
    length_scale: float = 0.1,
    noise_level: float = 1e-6,
    fit_noise: bool = True,
    trust_region_radius: float | None = None,
    seed: int = 42,
) -> np.ndarray:
    """
    Fit a GP surrogate and select the next query via UCB acquisition.

    Optionally applies a trust region: candidates are restricted to
    a hypercube of radius `trust_region_radius` around the current best
    observed point.  Trust regions prevent over-exploitation of the
    surrogate in regions far from training data.

    Parameters
    ----------
    X_train              : training inputs  (n, d)
    y_train              : training outputs (n,)
    n_candidates         : LHS candidate budget
    beta                 : UCB exploration weight
    length_scale         : GP RBF length-scale
    noise_level          : GP WhiteKernel noise level
    fit_noise            : whether to include WhiteKernel
    trust_region_radius  : if not None, restrict search to this radius
                           around best-observed point (per dimension)
    seed                 : random seed

    Returns
    -------
    next_query: np.ndarray of shape (d,)
    """
    n_dims = X_train.shape[1]
    candidates = lhs_candidates(n_dims, n_candidates, seed=seed)

    # Apply trust region if requested
    if trust_region_radius is not None:
        best_idx = np.argmax(y_train)
        best_x = X_train[best_idx]
        lo = np.clip(best_x - trust_region_radius, 0.0, 1.0)
        hi = np.clip(best_x + trust_region_radius, 0.0, 1.0)
        mask = np.all((candidates >= lo) & (candidates <= hi), axis=1)
        candidates = candidates[mask]
        if len(candidates) == 0:
            # Fallback: remove trust region if no candidates survive
            candidates = lhs_candidates(n_dims, n_candidates, seed=seed + 1)

    model = fit_gp(X_train, y_train, length_scale, noise_level, fit_noise)
    mean, std = gp_posterior(model, candidates)
    acq = ucb_acquisition(mean, std, beta)
    next_query = candidates[np.argmax(acq)]
    return next_query, model


# ---------------------------------------------------------------------------
# Dimension importance (gradient-based)
# ---------------------------------------------------------------------------

def dimension_sensitivity(
    model: GaussianProcessRegressor,
    x_best: np.ndarray,
    delta: float = 0.01,
) -> np.ndarray:
    """
    Estimate per-dimension sensitivity via finite differences on GP mean.

    Positive value → increasing that dimension increases predicted output.
    Useful for pseudo-dimensionality reduction in high-d functions (F7, F8).

    Parameters
    ----------
    model : fitted GaussianProcessRegressor
    x_best: current best input point (d,)
    delta : finite-difference step

    Returns
    -------
    gradient approximation (d,)
    """
    d = len(x_best)
    grad = np.zeros(d)
    base_mean = model.predict(x_best.reshape(1, -1)).ravel()[0]
    for i in range(d):
        x_plus = x_best.copy()
        x_plus[i] = np.clip(x_best[i] + delta, 0.0, 1.0)
        x_minus = x_best.copy()
        x_minus[i] = np.clip(x_best[i] - delta, 0.0, 1.0)
        mean_plus = model.predict(x_plus.reshape(1, -1)).ravel()[0]
        mean_minus = model.predict(x_minus.reshape(1, -1)).ravel()[0]
        grad[i] = (mean_plus - mean_minus) / (2 * delta)
    return grad


# ---------------------------------------------------------------------------
# Visualisation (2D functions only)
# ---------------------------------------------------------------------------

def plot_gp_surface_2d(
    model: GaussianProcessRegressor,
    X_train: np.ndarray,
    y_train: np.ndarray,
    next_query: np.ndarray | None = None,
    resolution: int = 80,
    title: str = "GP Posterior Mean",
) -> None:
    """
    Plot the GP posterior mean surface for 2D functions (F1, F2).

    Parameters
    ----------
    model      : fitted GaussianProcessRegressor
    X_train    : training inputs  (n, 2)
    y_train    : training outputs (n,)
    next_query : suggested next query point (2,) — plotted as red star
    resolution : grid resolution
    title      : plot title
    """
    assert X_train.shape[1] == 2, "plot_gp_surface_2d requires 2D functions"

    x1 = np.linspace(0, 1, resolution)
    x2 = np.linspace(0, 1, resolution)
    xx1, xx2 = np.meshgrid(x1, x2)
    X_grid = np.column_stack([xx1.ravel(), xx2.ravel()])

    mean, std = gp_posterior(model, X_grid)
    mean_grid = mean.reshape(resolution, resolution)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Posterior mean
    im = axes[0].contourf(xx1, xx2, mean_grid, levels=30, cmap='viridis')
    plt.colorbar(im, ax=axes[0])
    axes[0].scatter(X_train[:, 0], X_train[:, 1], c=y_train,
                    cmap='plasma', edgecolors='white', s=60, zorder=5, label='Observed')
    if next_query is not None:
        axes[0].scatter(*next_query, marker='*', s=200, c='red', zorder=6, label='Next query')
    axes[0].set_title(f"{title} — Posterior Mean")
    axes[0].set_xlabel("X₁"); axes[0].set_ylabel("X₂")
    axes[0].legend()

    # Posterior std (uncertainty)
    std_grid = std.reshape(resolution, resolution)
    im2 = axes[1].contourf(xx1, xx2, std_grid, levels=30, cmap='magma')
    plt.colorbar(im2, ax=axes[1])
    axes[1].scatter(X_train[:, 0], X_train[:, 1], c='white',
                    edgecolors='black', s=60, zorder=5, label='Observed')
    if next_query is not None:
        axes[1].scatter(*next_query, marker='*', s=200, c='red', zorder=6, label='Next query')
    axes[1].set_title(f"{title} — Posterior Uncertainty")
    axes[1].set_xlabel("X₁"); axes[1].set_ylabel("X₂")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_running_best(y_values: np.ndarray, title: str = "Running Best") -> None:
    """
    Plot the running maximum across all observations.

    Parameters
    ----------
    y_values: observed outputs in order of collection
    title   : plot title
    """
    running_best = np.maximum.accumulate(y_values)
    plt.figure(figsize=(8, 4))
    plt.plot(y_values, 'o--', alpha=0.5, label='Observed output')
    plt.plot(running_best, 'r-', linewidth=2, label='Running best')
    plt.xlabel("Query index"); plt.ylabel("Output value")
    plt.title(title); plt.legend(); plt.grid(True)
    plt.tight_layout(); plt.show()
