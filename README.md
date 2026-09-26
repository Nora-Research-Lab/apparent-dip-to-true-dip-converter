![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Apparent Dip to True Dip Converter
 
*For structural geologists and field mappers: enter the apparent dip angle and direction plus the strike of the bedding to instantly compute true dip angle and direction.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Geology
 
A dedicated Gradio tool that converts an apparent dip measurement into the true dip of a planar geological structure (e.g., bedding, fault, joint). The user provides three numeric inputs: (1) apparent dip angle (in degrees, 0-90), (2) apparent dip direction (azimuth in degrees, 0-360, the compass direction in which the apparent dip is observed), and (3) strike of the planar structure (azimuth in degrees, 0-360, using the right-hand rule convention, i.e., the strike direction such that the dip direction is 90° clockwise from it). The core calculation proceeds as follows: compute the acute angle θ between the apparent dip direction and the strike direction (absolute difference modulo 180, taking the acute angle between 0° and 90°). Then compute true dip using the formula: true_dip = arctan( tan(apparent_dip) / sin(θ) ). The true dip direction is then derived as (strike + 90°) modulo 360. If θ = 0° or 180°, the apparent dip is parallel to strike, which is invalid (the formula returns division by zero) — the tool catches this and displays a clear error message. If θ = 90°, the apparent dip equals the true dip. Outputs: (a) true dip angle in degrees to 1 decimal, (b) true dip direction as an azimuth in degrees to 1 decimal, and (c) a simple matplotlib diagram showing a labelled 3D perspective sketch of the geometry (a dipping plane, an apparent dip line on a vertical cross-section, and annotated angles). The Gradio UI consists of three number input boxes with appropriate labels and units, a 'Compute' button, and output components: a text box for the true dip angle, a text box for the true dip direction, and a plot area for the diagram. No AI/ML component — pure trigonometric calculation with geometric validation.
 
## Run it
 
```bash
docker build -t apparent-dip-to-true-dip-converter .
docker run -p 7860:7860 apparent-dip-to-true-dip-converter
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-26.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
