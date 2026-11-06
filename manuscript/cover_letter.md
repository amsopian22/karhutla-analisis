# COVER LETTER FOR SUBMISSION

**Date:** 6 November 2026

**To:**  
The Editor-in-Chief  
*Land Use Policy*  
Elsevier Science

**Subject:** Submission of Original Research Article titled *"The Governance Void at Concession Frontiers: A Spatial Boundary Discontinuity Analysis of Peatland Wildfires in Central Kalimantan"*

Dear Editor-in-Chief and Editorial Board Members,

We are pleased to submit our original research manuscript entitled **"The Governance Void at Concession Frontiers: A Spatial Boundary Discontinuity Analysis of Peatland Wildfires in Central Kalimantan"** for consideration for publication as a regular research article in *Land Use Policy*.

### Journal Fit and Core Land Use Policy Contribution
Tropical peatland wildfires across equatorial Southeast Asia present one of the world's most acute environmental governance dilemmas. While public discourse and statutory enforcement in Indonesia center heavily on corporate strict liability under environmental law (Law No. 32/2009, Article 88), recurrent mega-fires continue to devastate degraded peat domes during drought episodes. *Land Use Policy* provides the ideal venue for this study because our research directly addresses the territorial political economy, statutory boundaries, and institutional voids that govern tropical rural land use.

Rather than treating wildfire purely as a biophysical hazard or a generic classification problem, this manuscript deploys a **Spatial Boundary Discontinuity Design (Spatial BDD)** to evaluate how cadastral boundaries shape environmental outcomes. By computing signed Euclidean distances in metric UTM Zone 49S projection from 43,937 verified satellite thermal anomalies (NASA FIRMS) across 812 audited concessions (627 oil palm HGU and 185 commercial forestry PBPH), we provide the first spatially explicit econometric and geographic appraisal of the concession frontier governance void.

### Key Empirical and Policy Findings:
1. **The APL Institutional Governance Void:** Cadastral point-in-polygon overlays reveal that **75.42% (33,138 hotspots)** ignited outside corporate concession perimeters on unallocated state land (*Area Penggunaan Lain*, APL). These areas represent degraded state peatlands excised from the forest estate during the historical Mega Rice Project (ex-PLG) but left without designated institutional custodians, tenure security, or dedicated wildfire suppression mandates.
2. **Spatial Boundary Discontinuity Design (Spatial BDD):** We uncover an acute discontinuity at corporate perimeter boundaries. Inside certified concessions (-3 km to 0 km), where strict legal liability deters burning and incentivizes private surveillance, active fire density is suppressed at 0.183 hotspots/km². In contrast, directly across the boundary (0 km to +3 km) on unallocated APL state land, active fire density escalates by **+56.5% to 0.286 hotspots/km²**, peaking at **0.370 hotspots/km²** at the 3-km frontier (over 3.1-fold higher than the deep concession interior). This confirms that artificial drainage networks constructed within corporate concessions desorb adjacent unmanaged state peat domes, while legal liability stops abruptly at the cadastral border.
3. **Tobler's First Law and Spatial Autocorrelation Mitigation:** We demonstrate that tree-based machine learning algorithms ingesting geodetic coordinates suffer from spatial memorization and data leakage. Under 5-fold Spatial Block Cross-Validation (`GroupKFold` by administrative regency), a coordinate-dependent Random Forest collapses (ROC-AUC drops from 0.7956 to 0.5399). Conversely, our Pure Biophysical Model (excluding coordinates) maintains transferable predictive skill across all spatial blocks (Holdout ROC-AUC: 0.7527; Extreme Fire Recall: 65.82%; Spatial CV mean $F_1 = 0.1399$, representing a 2.4-fold retention over coordinate models). TreeSHAP reveals non-linear tipping points: severe fire risk escalates within 3,000 meters of artificial drainage canals and after 14 consecutive drought days.
4. **Actionable Land Governance Reforms:** Our findings demonstrate that strict liability jurisprudence within concession borders is necessary but insufficient. We formulate concrete spatial policy mechanisms: (i) mandating a statutory 3-km perimeter buffer co-management responsibility for concessionaires operating contiguous peat drainage networks, (ii) formalizing community land tenure through Social Forestry (*Perhutanan Sosial*) and Peatland Management Units (*Kesatuan Pengelolaan Gambut* / KPG), and (iii) prioritizing canal blocking within 3,000 meters of concession frontiers.

### Editorial and Ethical Declarations:
- **Originality:** This manuscript is an original work that has not been published previously and is not under consideration for publication elsewhere.
- **Authorship and Affiliation:** The manuscript is co-authored by Ahmad Sopian (Independent Researcher, Samarinda, Kalimantan Timur, Indonesia; Corresponding Author) and Rahmi Susanti (Faculty of Public Health, Universitas Mulawarman, Samarinda, Kalimantan Timur, Indonesia).
- **Open Access Model:** We confirm submission under the Subscription ($0 APC) publishing route.
- **Funding Statement:** This research received no external funding or institutional grant and was conducted as an independent collaborative research project.
- **Conflict of Interest:** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
- **Data Availability:** The master processed dataset of 43,937 active fire hotspots, official administrative boundaries (geoBoundaries ADM2), primary canal vectors in UTM Zone 49S projection, and complete analysis scripts are openly deposited and accessible in the research repository at https://github.com/amsopian22/karhutla-analisis.

Because this study speaks directly to the intersection of statutory land regulation, cadastral boundaries, and tropical peatland stewardship, we believe it will be of high interest to the readers of *Land Use Policy*.

Thank you very much for your time, consideration, and editorial handling of our manuscript.

Sincerely yours,

**Ahmad Sopian** (Corresponding Author)  
*Independent Researcher*  
Samarinda, Kalimantan Timur, Indonesia  
E-mail: ahmadsopian22@gmail.com  

**Rahmi Susanti**  
*Faculty of Public Health, Universitas Mulawarman*  
Samarinda, Kalimantan Timur, Indonesia  
E-mail: rahmi.susanti@fkm.unmul.ac.id
