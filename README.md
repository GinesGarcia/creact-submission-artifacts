CCS 2026 Anonymous Submission Artifacts
======================================

This repository contains the data and analysis artifacts for an anonymous CCS 2026 submission.
It includes two plotting notebooks, the datasets, and derived outputs used for the figures and
tables referenced in the submission.

Manuscript title: C-RE-ACT: Causal RE-ACTing Agent for O-RAN Forensic Triage

Repository Contents
-------------------

- [plot_sam_tool1.ipynb](plot_sam_tool1.ipynb): Loads SAM causal graphs from [data/sam_outputs](data/sam_outputs) and
	visualizes ranked root-cause nodes and subgraphs.
- [plot_tool2_pipeline.ipynb](plot_tool2_pipeline.ipynb): Loads evaluation results from
	[data/pipeline_outputs](data/pipeline_outputs) and generates aggregate plots (accuracy, F1, and
	text-metric summaries).
- [data/](data/): Inputs and outputs used by the notebooks.
	- [data/o-ran-performance-degradation-dataset/](data/o-ran-performance-degradation-dataset/):
		O-RAN testbed dataset: Packet delay and packet loss experiments (low/medium/high) across A1, E2, F1-c, and F1-u interfaces, organized by iteration.
	- [data/o-ciqa/](data/o-ciqa/): O-CIQA <Graph, Question, Answer> dataset with a dataset loading utility class. This dataset is derived from the causal graphs generated with the O-RAN testbed metrics, and it is used for training the graph soft-prompting architecture.
	- [data/pipeline_outputs/](data/pipeline_outputs/): Pipeline evaluation CSVs and intermediate results.
	- [data/sam_outputs/](data/sam_outputs/): SAM causal graphs generated from the O-RAN performance degradation dataset.
	- [data/plot_outputs/](data/plot_outputs/): Figure exports produced by the notebooks.

How To Use
----------

1. Open the notebooks in Jupyter or VS Code:
	 - [plot_sam_tool1.ipynb](plot_sam_tool1.ipynb)
	 - [plot_tool2_pipeline.ipynb](plot_tool2_pipeline.ipynb)
2. Run cells top to bottom. Paths are relative and assume you run from the repository root.
3. Figures are displayed inline and can be exported to [plot_outputs/](plot_outputs/)
	 by the notebook cells that save plots.

Dependencies
Notebooks executed with Python 3.10.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -f requirements.txt
```
Notes
-----

- This repository is anonymized for double-blind review.

