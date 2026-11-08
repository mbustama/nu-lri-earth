"""Redraw every figure: run notebooks/figures.ipynb from top to bottom, in place (the figures go to figures/).

Usage: python make_figures.py
Needs Jupyter (nbconvert) and a LaTeX distribution; see README.md.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

if __name__ == '__main__':
    for nb in sorted((ROOT / 'notebooks').glob('*.ipynb')):
        print(f'running {nb.name} ...', flush=True)
        subprocess.run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace',
                        '--ExecutePreprocessor.timeout=1800', str(nb)], check=True, cwd=ROOT / 'notebooks')
    print('done: the figures are in figures/')
