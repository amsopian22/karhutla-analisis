# COVER LETTER FOR SUBMISSION

**Date:** 4 November 2026

**To:**  
The Editor-in-Chief  
*Ecological Modelling* / *Remote Sensing of Environment* / *Land Use Policy*  
Elsevier Science

**Subject:** Submission of Original Research Article titled *"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"*

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit our original research manuscript entitled **"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"** for consideration for publication as a regular research article in your esteemed journal.

### Context and Core Scientific Contribution
Tropical peat swamp forests in Southeast Asia constitute globally vital carbon repositories that are experiencing chronic destabilization due to artificial drainage networks and recurrent wildfire crises. In Central Kalimantan, Indonesia, the legacy of the former Mega Rice Project (ex-PLG) excavated over 4,000 km of drainage canals across ombrotrophic peat domes. Despite extensive study, operational fire hazard prediction has remained constrained by two unresolved issues: (1) widespread methodological vulnerability to **spatial autocorrelation (Tobler’s First Law)** in machine learning models, causing optimistic validation bias and spatial memorization failure across unseen regions; and (2) polarized public debates surrounding **land tenure culpability** (corporate concessions vs. smallholders).

In this study, we present a calibrated spatiotemporal investigation integrating **43,937 verified active fire thermal anomalies** from the NASA FIRMS constellation (VIIRS 375m and MODIS Aqua) during the acute October 2026 crisis, official peat depth inventories (BBLSDLP/KHG 2019), metric primary canal vectors in UTM Zone 49S projection, daily ECMWF ERA5-Land atmospheric reanalysis, and comprehensive cadastral boundary overlays covering 627 oil palm concessions (HGU) and 185 commercial forestry concessions (PBPH).

### Key Empirical Findings:
1. **Resolution of the Spatial Memorization Trap ($H_1$ vs. $H_2$):** We demonstrate that a coordinate-dependent Random Forest baseline (Model A) collapses under 5-fold Spatial Block Cross-Validation (`GroupKFold` grouped by regency), with its mean ROC-AUC dropping from 0.7956 to 0.5399 and its $F_1$-score collapsing to 0.0000 across four of five spatial folds. In contrast, our Pure Biophysical Model (Model B, trained strictly without spatial coordinates) maintains stable predictive capacity across all spatial blocks (Holdout ROC-AUC: 0.7527; Extreme Fire Recall: 65.82%; Spatial CV mean $F_1 = 0.1399$, representing a 2.4-fold retention over Model A).
2. **Empirical Land Tenure Resolution:** Automated cadastral spatial overlay reveals that **75.42% (33,138 hotspots)** occurred on unallocated Non-Concession land (*Area Penggunaan Lain* / APL), representing an acute institutional and regulatory vacuum on abandoned state peatlands. Meanwhile, corporate oil palm (HGU) and commercial forestry (PBPH) concessions accounted for 16.56% (7,276 hotspots) and 8.02% (3,523 hotspots), respectively, providing an objective basis for targeted legal accountability under Indonesian strict liability jurisprudence (Law No. 32/2009).
3. **Quantified Biophysical Tipping Points:** Explainable AI via genuine TreeSHAP (`shap.TreeExplainer`) uncovered key non-linear intervention thresholds: a 7-day cumulative precipitation deficit $< 5.0$ mm, canal drainage proximity within a critical 3,000-meter corridor, and consecutive dry spells exceeding 14 days.

### Editorial and Ethical Declarations:
- **Originality:** This manuscript is an original work that has not been published previously and is not under consideration for publication elsewhere.
- **Authorship and Affiliation:** The manuscript is authored solely by Ahmad Sopian as an **Independent Researcher** based in Samarinda, Kalimantan Timur, Indonesia.
- **Funding Statement:** This research received no external funding or institutional grant and was conducted as an independent research project.
- **Conflict of Interest:** The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
- **Data Availability:** The satellite thermal anomaly observations and national peatland hydrological unit layers used in this study are derived from publicly accessible databases provided by NASA FIRMS (MODIS/VIIRS) and the Indonesian Ministry of Environment and Forestry (KLHK/BBLSDLP). Atmospheric reanalysis variables were obtained from the ECMWF ERA5-Land service. The processed analytical datasets and machine learning modeling code supporting the findings of this study are available from the corresponding author upon reasonable request.

Given the strong emphasis on spatial machine learning methodology, ecological modeling, and land governance, we believe this manuscript will be of broad interest to the readership of your journal.

Thank you very much for your time, consideration, and handling of our submission.

Sincerely yours,

**Ahmad Sopian**  
*Independent Researcher*  
Samarinda, Kalimantan Timur, Indonesia  
E-mail: ahmadsopian22@gmail.com  
