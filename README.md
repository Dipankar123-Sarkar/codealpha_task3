# Data Visualization demo

This small project demonstrates creating several data visualizations from a sample dataset.

What is included

- `src/visualize.py` — generator function `generate_visuals(output_dir)` that creates multiple charts and saves them as PNGs.
- `tests/test_visualize.py` — a minimal test that runs the generator and checks files are created.
- `requirements.txt` — libraries used.

Quick start (PowerShell)

1. Create a virtual environment and activate it (optional but recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the generator to produce images in `outputs_test`:

```powershell
python -c "from src.visualize import generate_visuals; print(generate_visuals('outputs_test'))"
```

4. Open the `outputs_test` folder to view the generated PNGs.

Notes

- The script will try to use Seaborn's `tips` dataset if Seaborn is installed; otherwise it falls back to a synthetic dataset so the generator remains runnable even without Seaborn.
- For portfolio/demo work, consider adding a Jupyter notebook (`notebooks/`) with narrative, interactive widgets, and higher-resolution images.
