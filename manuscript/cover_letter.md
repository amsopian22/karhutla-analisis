# COVER LETTER FOR SUBMISSION

**Date:** 4 November 2026

**To:**  
The Editor-in-Chief  
*Applied Geography*  
Elsevier Science

**Subject:** Submission of Original Research Article titled *"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"*

Dear Editor-in-Chief and Editorial Board Members,

We are pleased to submit our original research manuscript entitled **"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"** for consideration for publication as a regular research article in *Applied Geography*.

### Context, Journal Fit, and Spatial Geographic Contribution
Given *Applied Geography*’s core commitment to utilizing geospatial analysis, GIScience, and spatial modeling to resolve pressing human-environment resource and hazard dilemmas ("putting problems in a geographical perspective"), this manuscript directly addresses the spatial methodological traps and land governance challenges underpinning Southeast Asia's recurrent peatland wildfire crises.

For full editorial transparency, an earlier iteration of this manuscript received an out-of-scope desk rejection from *Ecological Modelling*. That decision was based on that journal's exclusive mandate for mechanistic biological simulations, population dynamics, and ecosystem metabolic equations. In contrast, our investigation is fundamentally grounded in **Applied Spatial Geography**, **Geographic Information Science (GIScience)**, **Spatial Autocorrelation Mitigation**, and **Land Tenure Political Economy**. It does not model cellular or physiological plant mechanics, but rather addresses spatial policy, territorial land administration, and regional transboundary environmental hazard management.

### Key Empirical and Methodological Contributions:
1. **Resolution of the Spatial Memorization Trap via Tobler’s First Law ($H_1$ vs. $H_2$):** Governed by Tobler’s First Law of Geography ("near things are more related than distant things"), environmental data inherently exhibit spatial autocorrelation. We prove empirically that incorporating geodetic coordinates into tree-based wildfire models induces severe spatial data leakage and spatial memorization. A coordinate-dependent Random Forest baseline (Model A) collapses under 5-fold Spatial Block Cross-Validation (`GroupKFold` grouped by administrative regency), with its ROC-AUC plunging from 0.7956 to 0.5399 and its $F_1$-score falling to 0.0000 across four of five spatial blocks. Conversely, our Pure Biophysical Model (Model B, trained strictly without spatial coordinates) maintains transferable predictive skill across all spatial blocks (Holdout ROC-AUC: 0.7527; Extreme Fire Recall: 65.82%; Spatial CV mean $F_1 = 0.1399$, representing a 2.4-fold retention over Model A).
2. **Empirical Land Tenure Resolution and the APL Governance Vacuum:** Integrating 43,937 verified satellite thermal anomalies (NASA FIRMS) with 812 audited cadastral concessions (627 oil palm HGU and 185 forestry PBPH) resolves the polarized public debate over fire culpability. Crucially, **75.42% (33,138 hotspots)** occurred on unallocated Non-Concession public land (*Area Penggunaan Lain* / APL), exposing an acute institutional and territorial vacuum across abandoned state peatlands. Meanwhile, corporate oil palm (16.56%) and commercial forestry (8.02%) concessions accounted for 24.58%, providing an objective spatial basis for targeted corporate enforcement under Indonesian strict liability jurisprudence (Law No. 32/2009, Article 88).
3. **Metric Hydrological Canal Proximity Forensics:** By vectorizing 13 primary canal axes in metric UTM Zone 49S projection across the ex-Mega Rice Project, we quantify a pronounced spatial distance decay effect: severe fire radiative risk escalates sharply within a 3,000-meter canal corridor (TreeSHAP rank 2, mean $|\text{SHAP}| = 0.0322$), establishing a concrete spatial zoning threshold for canal-blocking investments by restoration agencies.
4. **Regional Transboundary Smoke Haze Dispersion:** We link localized peat smoldering in Central Kalimantan to regional transboundary aerosol exposure. Under the prevailing Southwest Monsoon, smoke plumes advect north-northwestward toward Kuching ($197.3\,\mu\text{g}/\text{m}^3$), Singapore ($165.3\,\mu\text{g}/\text{m}^3$), and Kuala Lumpur ($191.7\,\mu\text{g}/\text{m}^3$), providing an analytical foundation for regional environmental early warning under the ASEAN Agreement on Transboundary Haze Pollution.

### Editorial and Ethical Declarations:
- **Originality:** This manuscript is an original work that has not been published previously and is not under consideration for publication elsewhere.
- **Authorship and Affiliation:** The manuscript is co-authored by Ahmad Sopian (Independent Researcher, Samarinda, Kalimantan Timur, Indonesia; Corresponding Author) and Rahmi Susanti (Faculty of Public Health, Universitas Mulawarman, Samarinda, Kalimantan Timur, Indonesia).
- **Funding Statement:** This research received no external funding or institutional grant and was conducted as an independent collaborative research project.
- **Conflict of Interest:** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
- **Data Availability:** All processed master active fire data, administrative boundaries, primary canal vectors in UTM Zone 49S projection, and trained machine learning models are openly deposited and accessible in the research repository at https://github.com/amsopian22/karhutla-analisis. Raw active fire thermal anomalies are accessible from NASA FIRMS (https://firms.modaps.eosdis.nasa.gov/). Atmospheric reanalysis variables were obtained from the ECMWF ERA5-Land service.

Because this study directly exemplifies the application of spatial geographical methods and spatial tenure governance to solve high-impact environmental hazard and public policy challenges, we firmly believe it will resonate strongly with the readership of *Applied Geography*.

Thank you very much for your time, consideration, and editorial handling of our submission.

Sincerely yours,

**Ahmad Sopian** (Corresponding Author)  
*Independent Researcher*  
Samarinda, Kalimantan Timur, Indonesia  
E-mail: ahmadsopian22@gmail.com  

**Rahmi Susanti**  
*Faculty of Public Health, Universitas Mulawarman*  
Samarinda, Kalimantan Timur, Indonesia  
E-mail: rahmi.susanti@fkm.unmul.ac.id
