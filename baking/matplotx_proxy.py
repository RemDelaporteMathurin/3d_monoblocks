from __future__ import annotations

import math

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

import numpy as np
from numpy.typing import ArrayLike

import numpy


def nnls(A, b, eps: float = 1.0e-10, max_steps: int = 100):
    # non-negative least-squares after
    # <https://en.wikipedia.org/wiki/Non-negative_least_squares>
    A = numpy.asarray(A)
    b = numpy.asarray(b)

    AtA = A.T @ A
    Atb = A.T @ b

    m, n = A.shape
    assert m == b.shape[0]
    mask = numpy.zeros(n, dtype=bool)
    x = numpy.zeros(n)
    w = Atb
    s = numpy.zeros(n)
    k = 0
    while sum(mask) != n and max(w) > eps:
        if k >= max_steps:
            break
        mask[numpy.argmax(w)] = True

        s[mask] = numpy.linalg.lstsq(AtA[mask][:, mask], Atb[mask], rcond=None)[0]
        s[~mask] = 0.0

        while numpy.min(s[mask]) <= 0:
            alpha = numpy.min(x[mask] / (x[mask] - s[mask]))
            x += alpha * (s - x)
            mask[numpy.abs(x) < eps] = False

            s[mask] = numpy.linalg.lstsq(AtA[mask][:, mask], Atb[mask], rcond=None)[0]
            s[~mask] = 0.0

        x = s.copy()
        w = Atb - AtA @ x

        k += 1

    return x


def move_min_distance(targets: ArrayLike, min_distance: float) -> np.ndarray:
    """Move the targets such that they are close to their original positions, but keep
    min_distance apart.

    https://math.stackexchange.com/a/3705240/36678
    """
    # sort targets
    idx = np.argsort(targets)
    targets = np.sort(targets)

    n = len(targets)
    x0_min = targets[0] - n * min_distance
    A = np.tril(np.ones([n, n]))
    b = targets - (x0_min + np.arange(n) * min_distance)

    # import scipy.optimize
    # out, _ = scipy.optimize.nnls(A, b)

    out = nnls(A, b)

    sol = np.cumsum(out) + x0_min + np.arange(n) * min_distance

    # reorder
    idx2 = np.argsort(idx)
    return sol[idx2]


def get_mid_y(c: PolyCollection):
    points = c.get_paths()[0].vertices
    # x = points[1:, 0].reshape(2, int(points[:, 1].size / 2))
    # x_high = x[0]
    # x_low = x[1]

    y = points[1:, 1].reshape(2, int(points[:, 1].size / 2))
    y_high = y[0]
    y_low = y[1]

    return (y_high[-2] + y_low[0]) / 2


def label_fillbetween(
    min_label_distance: float or str = "auto",
    alpha_optimize: float = 1.0,
    **text_kwargs,
):
    ax = plt.gca()

    logy = ax.get_yscale() == "log"

    if min_label_distance == "auto":
        # Make sure that the distance is alpha * fontsize. This needs to be translated
        # into axes units.
        fig = plt.gcf()
        fig_height_inches = fig.get_size_inches()[1]
        ax = plt.gca()
        ax_pos = ax.get_position()
        ax_height = ax_pos.y1 - ax_pos.y0
        ax_height_inches = ax_height * fig_height_inches
        ylim = ax.get_ylim()
        if logy:
            ax_height_ylim = math.log10(ylim[1]) - math.log10(ylim[0])
        else:
            ax_height_ylim = ylim[1] - ylim[0]
        # 1 pt = 1/72 in
        fontsize = mpl.rcParams["font.size"]
        assert fontsize is not None
        min_label_distance_inches = fontsize / 72 * alpha_optimize
        min_label_distance = (
            min_label_distance_inches / ax_height_inches * ax_height_ylim
        )

    # Add "legend" entries.
    # Get last non-nan y-value.
    targets = []
    for c in plt.gca().collections:
        if not isinstance(c, PolyCollection):
            continue

        targets.append(get_mid_y(c))

    if logy:
        targets = [math.log10(t) for t in targets]

    # Sometimes, the max value if beyond ymax. It'd be cool if in this case we could put
    # the label above the graph (instead of the to the right), but for now let's just
    # cap the target y.
    ymax = ax.get_ylim()[1]
    targets = [min(target, ymax) for target in targets]

    targets = move_min_distance(targets, min_label_distance)
    if logy:
        targets = [10**t for t in targets]

    labels = [
        c.get_label() for c in plt.gca().collections if isinstance(c, PolyCollection)
    ]
    alphas = [
        c.get_alpha() for c in plt.gca().collections if isinstance(c, PolyCollection)
    ]
    colors = [
        c.get_facecolor()
        for c in plt.gca().collections
        if isinstance(c, PolyCollection)
    ]

    axis_to_data = ax.transAxes + ax.transData.inverted()
    xpos = axis_to_data.transform([1.03, 1.0])[0]

    for label, ypos, color, alpha in zip(labels, targets, colors, alphas):
        plt.text(
            xpos,
            ypos,
            label,
            verticalalignment="center",
            alpha=alpha,
            color=color[0],
            **text_kwargs,
        )
