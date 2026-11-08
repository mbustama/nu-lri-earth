"""Reading the data files in data/, and the few calculations the figures need on top of them.

Every number that a figure shows is in a JSON file in data/; the functions here read those files
and return numpy arrays.  The only calculations are simple ones: interpolation of the limits
between the 25 masses of the analysis, geometry of the Earth's cross-section, and the stylized
detector of Fig. 2.
"""

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

DATA = Path(__file__).resolve().parent.parent / 'data'

HBARC_EV_KM = 1.97327e-10        # hbar c [eV km]: the interaction range 1/m' [km] is HBARC_EV_KM / m' [eV]
R_EARTH = 6371.0                 # radius of the Earth [km]
DETECTOR_DEPTH = 2.0             # depth of the detector in the Earth model [km]


def range_km(m: np.ndarray) -> np.ndarray:
    """The interaction range 1/m' [km] of a mediator of mass m' [eV]; the same function turns a
    range [km] back into a mass [eV] (the top axis of the limit figures)."""
    with np.errstate(divide='ignore'):
        return HBARC_EV_KM / np.asarray(m, dtype=float)


@lru_cache(maxsize=None)
def load(name: str) -> dict:
    """The contents of data/<name>.json."""
    with open(DATA / f'{name}.json') as f:
        return json.load(f)


def _array(values) -> np.ndarray:
    """A list from a JSON file as a float array, with null (no value) as nan."""
    return np.array([np.nan if v is None else v for v in values], dtype=float)


# ---------------------------------------------------------------------------- the limits
def masses() -> np.ndarray:
    """The 25 mediator masses of the analysis [eV]."""
    return np.array(load('limits')['mediator_mass_eV'])


def symmetries() -> list:
    """The names of the 15 entries of limits.json, in the order of the paper's Table I."""
    return list(load('limits')['symmetries'])


def charge_factor(symmetry: str) -> float:
    """The charge factor k of a symmetry (the paper's Table I)."""
    return load('limits')['symmetries'][symmetry]['charge_factor_k']


def upper_limit(symmetry: str, cl: str = '90', data: str = 'observed') -> np.ndarray:
    """The upper limit on g' (on G' for L_mu - L_tau) at the 25 masses: cl is '90' or '95',
    data is 'observed' or 'expected'.  All nan for a symmetry without an upper limit."""
    entry = load('limits')['symmetries'][symmetry]['upper_limit']
    if entry is None:
        return np.full(masses().size, np.nan)
    return _array(entry[cl][data])


def interpolate(m: np.ndarray, m_nodes: np.ndarray, g_nodes: np.ndarray) -> np.ndarray:
    """A curve through (m_nodes, g_nodes), a monotone cubic in log-log, at the masses m (how the
    paper draws its limits between the 25 masses)."""
    if not np.isfinite(g_nodes).all():
        return np.full(np.shape(m), np.nan)
    return 10**PchipInterpolator(np.log10(m_nodes), np.log10(g_nodes))(np.log10(m))


def limit_curve(m: np.ndarray, symmetry: str, cl: str = '90', data: str = 'observed',
                effective: bool = False) -> np.ndarray:
    """upper_limit, interpolated to the masses m; with effective=True, the limit on the effective
    coupling g' sqrt|k| of the paper's Fig. 8."""
    g = upper_limit(symmetry, cl, data)
    if effective:
        g = g * np.sqrt(abs(charge_factor(symmetry)))
    return interpolate(m, masses(), g)


def excluded_intervals(symmetry: str, cl: str = '90', data: str = 'observed',
                       effective: bool = False) -> tuple:
    """The bounded intervals of excluded couplings: (masses [eV], lower edges, upper edges), in g',
    or in g' sqrt|k| with effective=True."""
    rows = load('limits')['symmetries'][symmetry]['excluded_intervals'][cl][data]
    m = np.array([r['mass_eV'] for r in rows])
    lo, hi = np.array([r['g_lower'] for r in rows]), np.array([r['g_upper'] for r in rows])
    f = np.sqrt(abs(charge_factor(symmetry))) if effective else 1.0
    return m, f * lo, f * hi


# ---------------------------------------------------------------------------- other bounds
def previous_le_lmu() -> tuple:
    """The earlier DeepCore limit on L_e - L_mu (arXiv:2601.01220): masses [eV], g'."""
    c = load('previous_limits')['garg_2026_le_lmu']
    return np.array(c['mass_eV']), np.array(c['g'])


def previous_symmetries() -> dict:
    """The earlier DeepCore limits on eight symmetries (arXiv:2606.03443): {symmetry: (masses, g')}."""
    curves = load('previous_limits')['garg_2026_symmetries']['curves']
    return {s: (np.array(c['mass_eV']), np.array(c['g'])) for s, c in curves.items()}


def ep_bounds(cl: str = '90') -> tuple:
    """Bounds on g' from tests of the equivalence principle: masses [eV], {symmetry: g'}
    (inf where there is none)."""
    d = load('equivalence_principle_bounds')[cl]
    return np.array(d['mass_eV']), {s: np.nan_to_num(_array(g), nan=np.inf) for s, g in d['g'].items()}


# The symmetries whose matter charge is baryon number alone: B and no L_e (the upper EP band)
BARYON_ONLY = ('B - 3L_mu', 'B - 3L_tau', 'B - 3/2(L_mu + L_tau)', 'B_y + L_mu + L_tau')


def ep_bands(cl: str = '90') -> tuple:
    """The EP bounds in units of g' sqrt|k|, as two bands: masses [eV] and {'B': (low, high),
    'other': (low, high)}, the range of the bounds over the symmetries of BARYON_ONLY and over
    the others (as in the paper's Fig. 8)."""
    m, best = ep_bounds(cl)
    k = {s.replace(' (k > 0)', ''): load('limits')['symmetries'][s]['charge_factor_k'] for s in symmetries()}
    out = {}
    for key, group in (('B', True), ('other', False)):
        g = np.array([best[s] * np.sqrt(abs(k[s])) for s in best if (s in BARYON_ONLY) == group])
        out[key] = (g.min(axis=0), g.max(axis=0))
    return m, out


# ---------------------------------------------------------------------------- the Earth
def path_length(cos_zenith: float) -> float:
    """Length [km] of the path from where a neutrino enters the Earth to the detector."""
    r_d = R_EARTH - DETECTOR_DEPTH
    return np.sqrt(R_EARTH**2 - r_d**2 * (1.0 - cos_zenith**2)) - r_d * cos_zenith


def path_chord(cos_zenith: float) -> tuple:
    """Where a path enters the Earth and where the detector is, in a cross-section with the
    detector at the right: two (x, y) points in units of the Earth's radius."""
    r_d = R_EARTH - DETECTOR_DEPTH
    s_hat = np.array([cos_zenith, np.sqrt(1.0 - cos_zenith**2)])
    det = np.array([r_d, 0.0])
    return (det + path_length(cos_zenith) * s_hat) / R_EARTH, det / R_EARTH


def cos_zenith_grazing(radius_km: float) -> float:
    """cos(theta_z) of the path that grazes the sphere of radius_km; steeper paths cross it."""
    return -float(np.sqrt(1.0 - (radius_km / (R_EARTH - DETECTOR_DEPTH))**2))


def potential_map(range_index: int, n: int = 801) -> np.ndarray:
    """The potential in a cross-section of the Earth relative to its value at the detector, on an
    n x n grid of (x, y) from -1 to 1 (units of the Earth's radius); nan outside the Earth."""
    entry = load('potential')['ranges'][range_index]
    r1, v1 = np.array(entry['radius_km']), np.array(entry['ratio'])
    x = np.linspace(-1.0, 1.0, n)
    rr = np.hypot(*np.meshgrid(x, x)) * R_EARTH
    return np.where(rr <= R_EARTH, np.interp(rr, r1, v1), np.nan)


def earth_layers() -> list:
    """The 12 layers of the Earth model: (inner radius [km], outer radius [km], density [g/cm^3])."""
    return [(l['inner_km'], l['outer_km'], l['density_g_cm3']) for l in load('earth')['layers']]


def land_rings() -> list:
    """Land outlines seen from above the equator at longitude -40 deg, South Pole at the right:
    one (n, 2) array of (x, y) per landmass, in units of the Earth's radius."""
    return [np.array(r) for r in load('earth')['land_rings_lon_minus40']]


# ---------------------------------------------------------------------------- the stylized detector of Fig. 2
def detector_doms() -> np.ndarray:
    """A stylized IceCube in the plane of the schematic: (depth [km], transverse position [km],
    DeepCore flag) of each optical module.  Nine strings of modules every 0.1 km between 1.45 and
    2.45 km deep, and four denser DeepCore strings (every 0.05 km between 2.1 and 2.45 km)."""
    doms = [(d, v, False) for v in np.linspace(-0.5, 0.5, 9) for d in np.linspace(1.45, 2.45, 11)]
    doms += [(d, v, True) for v in (-0.09, -0.03, 0.03, 0.09) for d in np.linspace(2.1, 2.45, 8)]
    return np.array(doms, dtype=float)


def event_hits(kind: str) -> dict:
    """Stylized hits of a 'track' (a muon from a nu_mu charged-current interaction near DeepCore,
    going up, with a small shower at its vertex) or a 'shower' (light spreading from the vertex).
    Charge falls exponentially with the distance from the light, and time grows with it.  Returns
    the modules hit: depth, transverse position [km], charge and time (both relative)."""
    doms = detector_doms()
    d, v = doms[:, 0], doms[:, 1]
    vertex = np.array([2.36, -0.06])
    if kind == 'track':
        direction = np.array([-np.cos(np.deg2rad(12)), np.sin(np.deg2rad(12))])
        rel = np.column_stack([d, v]) - vertex
        along = rel @ direction
        perp = np.abs(rel @ np.array([-direction[1], direction[0]]))
        on = (along > -0.05) & (along < 1.0) & (perp < 0.08)
        dist = np.where(along > 0, perp, np.hypot(perp, along))
        charge, time = np.exp(-dist / 0.03), np.clip(along, 0, None) + dist
        shower = np.hypot(d - vertex[0], v - vertex[1]) < 0.09
        on = on | shower
        charge = np.where(shower, np.maximum(charge, np.exp(-np.hypot(d - vertex[0], v - vertex[1]) / 0.04)),
                          charge)
    elif kind == 'shower':
        r = np.hypot(d - vertex[0], v - vertex[1])
        on = r < 0.22
        charge, time = np.exp(-r / 0.06), r
    else:
        raise ValueError(f"event_hits: kind must be 'track' or 'shower', not {kind!r}")
    return {'depth': d[on], 'transverse': v[on], 'charge': charge[on] / charge[on].max(),
            'time': time[on] / max(time[on].max(), 1e-12)}
