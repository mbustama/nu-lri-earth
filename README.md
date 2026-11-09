# Earth-sized tests of long-range neutrino interactions

The limits of the paper, the numbers behind every one of its figures, and the code that draws them. By Dyer F. Cardenas (Pontificia Universidad Católica del Perú) and Mauricio Bustamante (Niels Bohr Institute, University of Copenhagen). The paper's arXiv link will be added here.

A new gauge boson $Z'$, very light, could mediate a force between neutrinos and the electrons and nucleons of ordinary matter. Atmospheric neutrinos that cross the Earth would then feel a potential, sourced by the Earth itself, that changes how they oscillate. The paper computes that potential at every point along the path of each neutrino, uses it to analyze 8 years of public IceCube DeepCore data, with a livetime of 2724 days (7.5 years), and sets upper limits on the coupling $g'$ of the $Z'$ for 14 flavor-dependent $U(1)'$ symmetries and mediator masses $m'$ from $10^{-15}$ to $10^{-9}$ eV (interaction ranges $1/m'$ from about $2 \times 10^5$ km down to 0.2 km).

## How to use it

* **To use the limits**: they are all in one file, [`data/limits.json`](data/limits.json): the upper limits on the coupling at 90% and 95% C.L., for every symmetry, on the data and expected, at 25 mediator masses. See [The limits](#the-limits) below.
* **To look at a figure**: open its PDF in [`figures/`](figures/), named after its number in the paper.
* **To redraw the figures**: install the packages of [`requirements.txt`](requirements.txt) and a LaTeX distribution (see [Redrawing the figures](#redrawing-the-figures)), then run `python make_figures.py`, or open [`notebooks/figures.ipynb`](notebooks/figures.ipynb) and run all its cells. The notebook explains each figure: what it shows, how to read it, and which data file holds its numbers. GitHub shows the notebook with its figures, so it can also be read without running it.

## The repository

```
README.md          this file
requirements.txt   the Python packages the notebook needs
make_figures.py    runs the notebook, redrawing every figure
notebooks/         figures.ipynb: every figure of the paper, each one explained
plotting/          data.py, which reads the data files; style.py and matplotlibrc, the figures' style
figures/           the figures of the paper (PDF)
data/              the limits, and the numbers behind every figure (JSON)
```

Every data file is a JSON file whose field `content` says what it holds.

## The limits

[`data/limits.json`](data/limits.json) has one entry per symmetry under `symmetries`, and the 25 mediator masses of the analysis under `mediator_mass_eV` (with the interaction ranges, $1/m' = \hbar c/m'$, under `interaction_range_km`). Its section `how_to_read` explains every field. For each symmetry:

* `upper_limit[CL][data]` is the list of upper limits on the coupling, one per mass: `CL` is `"90"` or `"95"` (the confidence level, in %), and `data` is `"observed"` (from the DeepCore data) or `"expected"` (from the Asimov data set, the expected events of the fit without a long-range interaction). `upper_limit` is `null` for the six symmetries whose potential acts on $\nu_e$ alone, which have no upper limit.
* `coupling` says which coupling is bounded: $g'$, the gauge coupling of the $U(1)'$, except for $L_\mu - L_\tau$, which ordinary matter does not carry: its potential comes from the mixing of the $Z'$ with the $Z$, and the limit is on the effective coupling $G'$ of that mixing (one entry for each sign of the potential).
* `charge_factor_k` is the charge factor $k$ of the paper's Table I: the potential is $g'^2 k$ times a potential per electron. Multiplying a limit by $\sqrt{|k|}$ gives the limit on the effective coupling $g'\sqrt{|k|}$ of the paper's Fig. 8, in which the eight limits fall into two groups.
* `excluded_intervals` (only for $L_e + 2L_\mu + 2L_\tau$ and $B_y + L_\mu + L_\tau$) lists, at each mass where there is one, a bounded interval of couplings, from `g_lower` to `g_upper`, excluded at 90% C.L. (none at 95% C.L.).

| Name in the file | Symmetry | Potential acts on | $k$ | Coupling | Upper limit |
|---|---|---|---|---|---|
| `B - 3L_mu` | $B - 3L_\mu$ | $\nu_\mu$ | −6.05 | $g'$ | yes |
| `L - 3L_mu` | $L - 3L_\mu$ | $\nu_\mu$ | −3 | $g'$ | yes |
| `B - 3L_tau` | $B - 3L_\tau$ | $\nu_\tau$ | −6.05 | $g'$ | yes |
| `L - 3L_tau` | $L - 3L_\tau$ | $\nu_\tau$ | −3 | $g'$ | yes |
| `L_mu - L_tau (k > 0)` | $L_\mu - L_\tau$ | $\nu_\mu - \nu_\tau$ | +0.731 | $G'$ | yes |
| `L_mu - L_tau (k < 0)` | $L_\mu - L_\tau$ | $\nu_\mu - \nu_\tau$ | −0.731 | $G'$ | yes |
| `B - L_e - 2L_tau` | $B - L_e - 2L_\tau$ | $\nu_\mu - \nu_\tau$ | +1.017 | $g'$ | yes |
| `L_e - L_mu` | $L_e - L_\mu$ | $\nu_e - \nu_\mu$ | +1 | $g'$ | yes |
| `L_e - L_tau` | $L_e - L_\tau$ | $\nu_e - \nu_\tau$ | +1 | $g'$ | yes |
| `B - 3L_e` | $B - 3L_e$ | $\nu_e$ | +2.95 | $g'$ | no |
| `L - 3L_e` | $L - 3L_e$ | $\nu_e$ | +6 | $g'$ | no |
| `B - 3/2(L_mu + L_tau)` | $B - \frac{3}{2}(L_\mu + L_\tau)$ | $\nu_e$ | +3.03 | $g'$ | no |
| `L_e - 1/2(L_mu + L_tau)` | $L_e - \frac{1}{2}(L_\mu + L_\tau)$ | $\nu_e$ | +1.5 | $g'$ | no |
| `L_e + 2L_mu + 2L_tau` | $L_e + 2L_\mu + 2L_\tau$ | $\nu_e$ | −1 | $g'$ | no; excluded intervals at 90% C.L. |
| `B_y + L_mu + L_tau` | $B_y + L_\mu + L_\tau$ | $\nu_e$ | −2.02 | $g'$ | no; excluded intervals at 90% C.L. |

The limits come from a $\Delta\chi^2$ profiled over the 18 nuisance parameters of the DeepCore analysis and the six oscillation parameters, with thresholds of 1.64 (90% C.L.) and 2.71 (95% C.L.) for a one-sided limit; the paper's Sec. III and Appendix E give the details and the coverage of these limits.

### Reading the limits in Python

With the standard library only:

```python
import json

with open('data/limits.json') as f:
    limits = json.load(f)

masses = limits['mediator_mass_eV']                                         # 25 masses [eV]
g90 = limits['symmetries']['L_e - L_mu']['upper_limit']['90']['observed']   # 25 upper limits on g'
for m, g in zip(masses, g90):
    print(f'{m:.2e} eV: g\' < {g:.2e}')
```

With the module of this repository, which also interpolates between the masses as the paper's figures do (a monotone cubic in log-log):

```python
import sys
import numpy as np
sys.path.insert(0, '.')                     # the root of this repository
from plotting import data

m = np.logspace(-15, -9, 200)               # mediator masses [eV]
g = data.limit_curve(m, 'L_e - L_mu', cl='90', data='observed')              # upper limit on g'
g_eff = data.limit_curve(m, 'B - 3L_mu', cl='95', effective=True)          # on g' sqrt|k|, as in Fig. 8
m_w, g_low, g_high = data.excluded_intervals('B_y + L_mu + L_tau', cl='90')  # excluded intervals
```

## Redrawing the figures

1. Install the Python packages: `pip install -r requirements.txt` (the figures of this repository were drawn with Python 3.12 and matplotlib 3.11.2).
2. Install a LaTeX distribution, such as TeX Live, with the psnfss fonts: the text of the figures is typeset by LaTeX, in Palatino, as in the paper.
3. Run `python make_figures.py`, or open `notebooks/figures.ipynb` in Jupyter and run all its cells. The figures go to `figures/`.

## Figures

| File | Figure in the paper |
|---|---|
| [`fig01_limits_Le_Lmu.pdf`](figures/fig01_limits_Le_Lmu.pdf) | **Fig. 1.** Limits on the coupling of an $L_e - L_\mu$ interaction versus the mediator mass, with the earlier DeepCore limit and the bounds from tests of the equivalence principle. |
| [`fig02_setup.pdf`](figures/fig02_setup.pdf) | **Fig. 2.** An atmospheric neutrino crossing the Earth, with a long-range interaction (a schematic). |
| [`fig03_potential.pdf`](figures/fig03_potential.pdf) | **Fig. 3.** The long-range potential inside the Earth, relative to its value at the detector, for three interaction ranges. |
| [`fig04_oscillograms.pdf`](figures/fig04_oscillograms.pdf) | **Fig. 4.** Muon-neutrino survival probability versus energy and direction, without and with a long-range interaction. |
| [`fig05_probabilities.pdf`](figures/fig05_probabilities.pdf) | **Fig. 5.** Muon-neutrino survival probability versus energy, along two paths. |
| [`fig06_data_and_fit.pdf`](figures/fig06_data_and_fit.pdf) | **Fig. 6.** Observed events of the IceCube DeepCore sample, and their pulls against the fit without a long-range interaction. |
| [`fig07_lri_in_bins.pdf`](figures/fig07_lri_in_bins.pdf) | **Fig. 7.** Change in the expected events caused by a long-range interaction. |
| [`fig08_all_symmetries.pdf`](figures/fig08_all_symmetries.pdf) | **Fig. 8.** Limits on the effective couplings of the eight symmetries that have an upper limit, at 90% C.L., with earlier limits and the bounds from tests of the equivalence principle. |
| [`figB1_flux.pdf`](figures/figB1_flux.pdf) | **Fig. B.1.** Atmospheric neutrino flux used in this work. |
| [`figD1_nuisance_parameters.pdf`](figures/figD1_nuisance_parameters.pdf) | **Fig. D.1.** Nuisance parameters at the fit without a long-range interaction, next to those of the DeepCore analysis. |
| [`figF1_all_symmetries_95CL.pdf`](figures/figF1_all_symmetries_95CL.pdf) | **Fig. F.1.** As Fig. 8, at 95% C.L. |
| [`figF2_excluded_intervals.pdf`](figures/figF2_excluded_intervals.pdf) | **Fig. F.2.** Bounded intervals of couplings excluded at 90% C.L. for the two symmetries whose potential acts on $\nu_e$ alone with $k < 0$. |

## Data

| File | What it holds | Figures |
|---|---|---|
| [`limits.json`](data/limits.json) | The upper limits on the coupling at 90% and 95% C.L., observed and expected, for every symmetry; the charge factors; the excluded intervals. | 1, 8, F.1, F.2 |
| [`previous_limits.json`](data/previous_limits.json) | Earlier 90% C.L. limits from the same DeepCore data, which hold the potential at its value at the detector: arXiv:2601.01220 ($L_e - L_\mu$) and arXiv:2606.03443 (eight symmetries), read off their Fig. 1. | 1, 8 |
| [`equivalence_principle_bounds.json`](data/equivalence_principle_bounds.json) | Bounds on $g'$ from tests of the equivalence principle (the stronger of Eöt-Wash and MICROSCOPE), translated to each symmetry, at 90% and 95% C.L. | 1, 8, F.1, F.2 |
| [`potential.json`](data/potential.json) | The potential of $L_e - L_\mu$ inside the Earth relative to its value at the detector, for three interaction ranges: versus radius, and along two paths with the electron density. | 3 |
| [`oscillograms.json`](data/oscillograms.json) | The $\nu_\mu$ survival probability versus energy and direction, without and with the benchmark interaction. | 4 |
| [`probabilities.json`](data/probabilities.json) | The same along two directions, on a finer grid of energies. | 5 |
| [`events.json`](data/events.json) | The DeepCore sample in its 200 analysis bins: observed events, expected events at our fit and their simulation variance, and the expected events of the benchmark without and with the interaction. | 6, 7 |
| [`flux.json`](data/flux.json) | The atmospheric neutrino flux (MCEq), averaged over up-going directions and over the year. | B.1 |
| [`nuisance_pulls.json`](data/nuisance_pulls.json) | The nuisance parameters at our fit and at the DeepCore analysis. | D.1 |
| [`earth.json`](data/earth.json) | The 12 layers of the Earth model, and land outlines for the schematic. | 2 |

## Sources

* The data: the public data release of the IceCube DeepCore oscillation analysis, [doi:10.7910/DVN/B4RITM](https://doi.org/10.7910/DVN/B4RITM); the analysis, IceCube Collaboration, Phys. Rev. D **108**, 012014 (2023), [arXiv:2304.12236](https://arxiv.org/abs/2304.12236).
* The Earth model: the Preliminary Reference Earth Model in the 12 layers of constant density used by the DeepCore analysis.
* The earlier limits: S. Garg et al., [arXiv:2601.01220](https://arxiv.org/abs/2601.01220) and [arXiv:2606.03443](https://arxiv.org/abs/2606.03443), digitized from their Fig. 1, so they are approximate.
* The equivalence-principle bounds: Eöt-Wash, [arXiv:1207.2442](https://arxiv.org/abs/1207.2442), and MICROSCOPE, [arXiv:2209.15487](https://arxiv.org/abs/2209.15487), translated to each symmetry as in the paper's Sec. IV C.
* The land outlines of Fig. 2: [Natural Earth](https://www.naturalearthdata.com/) (1:50m, public domain).

If you use these limits or this code, please cite the paper (reference to be added here).
