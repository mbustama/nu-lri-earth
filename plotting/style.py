"""The style of the paper's figures.

use() loads plotting/matplotlibrc (text typeset by LaTeX in Palatino, inward ticks on all four
sides); call it before drawing.  The other functions are small drawing aids: tick labels for the
axis of the interaction range, the color of a light fill, and text written along a curve.
"""

import os

import matplotlib
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.path import Path
from matplotlib.ticker import FuncFormatter, LogFormatterSciNotation

RC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'matplotlibrc')

# One color per quantity across all figures (Okabe-Ito, colorblind-safe)
COLORS = {'up': '#0072B2', 'horizontal': '#009E73', 'down': '#D55E00',
          'numu': '#0072B2', 'nue': '#D55E00', 'numubar': '#56B4E9', 'nuebar': '#E69F00'}


def use():
    """Draw every later figure in the repository's style (the backend is left alone)."""
    backend = matplotlib.get_backend()
    matplotlib.rc_file(RC)
    matplotlib.rcParams['backend'] = backend
    matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amssymb}'


def km_formatter() -> FuncFormatter:
    """Log tick labels with 1 in place of 10^0 (for the axis of the range in km)."""
    base = LogFormatterSciNotation()
    return FuncFormatter(lambda v, pos: r'$1$' if abs(v - 1.0) < 1.e-9 else base(v, pos))


def shade_of(color, alpha: float) -> tuple:
    """The color of a fill of `color` with opacity `alpha` over white (for outlines of text
    that lies on that fill)."""
    return tuple(alpha * np.array(mcolors.to_rgb(color)) + (1.0 - alpha))


def _normals(ax, x, y) -> tuple:
    """The curve (x, y) in display units, its unit tangents, and its unit normals, pointing up."""
    p = ax.transData.transform(np.column_stack([x, y]))
    t = np.gradient(p, axis=0)
    t /= np.hypot(t[:, 0], t[:, 1])[:, None]
    n = np.column_stack([-t[:, 1], t[:, 0]])
    n[n[:, 1] < 0] *= -1.0
    return p, t, n


def closed_path(vertices: np.ndarray) -> Path:
    """A closed Path through the vertices (a closed Path ignores its last vertex, so the first
    is repeated there)."""
    return Path(np.vstack([vertices, vertices[:1]]), closed=True)


def side_strip(ax, x, y, width_pt: float) -> np.ndarray:
    """The polygon [data units] of a strip of width_pt points above the curve (x, y), offset
    along its normal in display space, so that it keeps its width where the curve rises (as in
    NuFlavorRatiosSteriles).  Call it after the axes limits are set."""
    p, _, n = _normals(ax, x, y)
    q = ax.transData.inverted().transform(p + width_pt * ax.figure.dpi / 72.0 * n)
    return np.vstack([np.column_stack([x, y]), q[::-1]])


def curved_text(ax, x, y, text: str, start_x: float, offset_pt: float=2.0, smooth: int=25,
                **kw) -> None:
    """Writes `text` along the curve (x, y), from start_x on, offset_pt points above it, each
    letter (or $...$ group) rotated with the curve, smoothed over `smooth` points so that the
    text does not follow kinks.  The letters are placed in data units, so that they stay put at
    any resolution of the output.  Call it after the axes limits are set."""
    fig = ax.figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    p = ax.transData.transform(np.column_stack([x, y]))
    if smooth > 1:
        pad = smooth // 2
        q = np.vstack([np.repeat(p[:1], pad, 0), p, np.repeat(p[-1:], pad, 0)])
        k = np.ones(smooth) / smooth
        p = np.column_stack([np.convolve(q[:, 0], k, 'valid'),
                             np.convolve(q[:, 1], k, 'valid')])[:len(x)]
    xs, ys = ax.transData.inverted().transform(p).T
    p, t, n = _normals(ax, xs, ys)
    p = p + offset_pt * fig.dpi / 72.0 * n
    s = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(p, axis=0).T))])
    s0 = np.interp(np.log(start_x), np.log(x), s)
    tokens, i = [], 0
    while i < len(text):
        j = text.index('$', i + 1) + 1 if text[i] == '$' else i + 1
        tokens.append(text[i:j])
        i = j
    space = 0.28 * kw.get('fontsize', 8) * fig.dpi / 72.0
    for tok in tokens:
        if tok == ' ':
            s0 += space
            continue
        probe = ax.text(0, 0, tok, transform=None, **kw)
        w = probe.get_window_extent(renderer).width
        probe.remove()
        sc = s0 + 0.5 * w
        xy = [np.interp(sc, s, p[:, 0]), np.interp(sc, s, p[:, 1])]
        angle = np.degrees(np.arctan2(np.interp(sc, s, t[:, 1]), np.interp(sc, s, t[:, 0])))
        ax.text(*ax.transData.inverted().transform(xy), tok, rotation=angle,
                rotation_mode='anchor', ha='center', va='bottom', **kw)
        s0 += w + 0.04 * space

