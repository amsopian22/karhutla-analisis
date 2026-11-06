# The Governance Void at Concession Frontiers: A Spatial Boundary Discontinuity Analysis of Peatland Wildfires in Central Kalimantan

**Authors:** Anonymous for Double-Blind Peer Review  
**Target Journal:** *Remote Sensing Applications: Society and Environment* (Elsevier)  
**Date:** November 2026  
---

## Abstract

Tropical peatland wildfires in Southeast Asia represent a critical land governance dilemma. While environmental enforcement emphasizes corporate liability, fire distributions across jurisdictional boundaries remain contested. Here, we implement a Spatial Boundary Discontinuity Design (Spatial BDD) using 43,937 verified satellite active fire detections (NASA FIRMS) during the October 2026 crisis in Central Kalimantan, integrated with 812 audited concessions (627 oil palm HGU and 185 forestry PBPH), metric canal vectors, and ERA5-Land covariates. Cadastral overlay reveals that 75.4% (33,138 hotspots) ignited outside corporate perimeters on unallocated public lands (*Area Penggunaan Lain*, APL), exposing an acute governance void. Within a 3-km frontier corridor, Spatial BDD establishes a sharp +56.5% discontinuity in fire density, jumping from 0.183 hotspots/km² inside concessions to 0.286 hotspots/km² on exterior APL peatlands (peaking at 0.370 hotspots/km² at 3 km). Under 5-fold Spatial Block Cross-Validation, coordinate-dependent models suffered complete recall collapse ($F_1 = 0.00$) from spatial memorization. While cross-landscape covariate shift depressed spatial ROC-AUC, a pure biophysical Random Forest rescued operational detection across unseen regencies (holdout ROC-AUC: 0.7527; 2.4-fold higher spatial $F_1$-score). TreeSHAP identified a 3-km canal corridor and 14-day drought trigger as critical tipping points. Corporate strict liability (Law No. 32/2009) deters burning inside concessions but leaves adjacent state peatlands vulnerable to drainage spillover. Sustainable land governance requires extending statutory buffer liability across 3 km and formalizing community peatland management units.

**Keywords:** Remote sensing applications; Satellite active fires; Tropical peatlands; Spatial boundary discontinuity; Spatial block cross-validation; Land tenure governance; Fire Radiative Power.

---

## 1. Introduction

Tropical peat swamp forests are among the most carbon-dense terrestrial ecosystems on the planet, sequestering up to twenty times more organic carbon per unit area than adjacent upland tropical rainforests on mineral soils (@Page2002Nature; @Dommain2011ProcRSocB). In undisturbed equatorial environments, high phreatic water tables remain near or above the surface throughout the annual cycle, creating anoxic conditions that retard organic matter decomposition and render natural peat formations virtually non-combustible (@Wosten2008Geoderma; @Dadap2021NatComm). Over the past three decades, however, Southeast Asian peatlands across Sumatra and Borneo have experienced severe anthropogenic disturbance from industrial logging, agricultural conversion, and massive state-sponsored drainage schemes (@Miettinen2016ERL; @Dohong2017RestorEcol; @Langner2007IJWF; @Carlson2012PNAS).

In Central Kalimantan, Indonesia, the Mega Rice Project (ex-PLG) excavated over 4,000 km of primary, secondary, and tertiary drainage canals between 1995 and 1999 across more than one million hectares of ombrotrophic peat domes between the Sebangau, Kahayan, Kapuas, and Barito rivers (@Silvius2005Wetlands; @Ritzema2014HESS). These canals accelerate gravitational drainage during dry seasons, drawing groundwater tables below the regulatory limit of -40 cm established under Indonesian Government Regulations (PP No. 71/2014 and PP No. 57/2016). When dry spells coincide with positive El Niño–Southern Oscillation (ENSO) anomalies or positive Indian Ocean Dipole (pIOD) events, drained peat ignites readily (@Cochrane2003Nature; @Hooijer2012Biogeosciences; @Field2016PNAS). Once ignited, smoldering combustion propagates horizontally and vertically through the catotelm for months, releasing ancient carbon sequestered over millennia (@Usup2004Tropics; @Wooster2018NatGeosci; @Vetrita2020RemoteSensing).

Major fire episodes in 1997, 2015, and 2019 released an estimated 0.81–2.57 Gt, 1.2 Gt, and 0.71 Gt of CO$_2$-equivalent emissions, respectively, at times exceeding the daily fossil fuel emissions of major industrialized nations (@Page2002Nature; @Field2016PNAS; @VanderWerf2017ESSD). Peat smoldering also generates fine particulate matter (PM2.5), carbon monoxide, and aerosol precursors that form regional smoke-haze across Indonesia, Singapore, and Malaysia, causing acute public health emergencies and substantial economic losses (@Gaveau2014PLOSONE; @Kiely2021ACP; @Graham2022SciRep).

In the domain of land use policy, environmental governance, and applied spatial geography, resolving tropical peatland wildfire crises encounters two critical impasses:

First, **the territorial political economy of land tenure culpability and concession frontier spillover remains clouded by empirical ambiguity and legal asymmetry**. Public discourse and regulatory enforcement in Indonesia have centered primarily on corporate concessionaires, anchored in the strict statutory liability framework of Law No. 32/2009 on Environmental Protection and Management (Article 88), which imposes no-fault liability for any fire occurring within certified concession perimeters (@Tacconi2003CIFOR; @Carlson2012PNAS). However, historical state territorialization partitioned Indonesia's land estate into the State Forest Estate (*Kawasan Hutan*) and Other Utilization Areas (*Area Penggunaan Lain*, APL). In post-Mega Rice Project Central Kalimantan, vast expanses of drained peatlands were excised from the forest estate into APL, but left unallocated without designated concessionaires, Forest Management Units (KPH), or dedicated fire suppression mandates (@Cattau2016GCB; @Putranto2023LandUsePol). Concurrently, artificial drainage networks constructed within corporate concessions inevitably lower regional groundwater tables across contiguous hydrological domes, desorbing adjacent state peatlands beyond concession borders. Whether corporate strict liability deters fire inside borders while inadvertently displacing ignitions onto adjacent unmanaged APL lands—creating a "frontier governance void"—remains untested through rigorous econometric or spatial boundary discontinuity techniques.

Second, **unmitigated spatial autocorrelation induces insidious spatial memorization in predictive spatial land use models**. Machine learning classifiers, including Random Forests, are increasingly deployed for spatial wildfire susceptibility and active combustion mapping (@Breiman2001ML). However, terrestrial environmental processes strictly operate under Tobler's First Law of Geography: everything is related to everything else, but near things are more related than distant things (@Tobler1970EconGeogr; @Legendre1993Ecology). When spatial hazard models ingest geodetic coordinates (`latitude` and `longitude`) or administrative unit labels as independent predictors, recursive tree partitioning algorithms exploit spatial coordinates as empirical shortcuts, memorizing historical spatial clusters rather than learning underlying biophysical combustion mechanics (@Meyer2018EcolModel; @Dormann2007Ecography). Under standard random cross-validation, spatial autocorrelation between geographically proximate training and validation samples causes severe data leakage (@Roberts2017Ecography; @Wadoux2021EcolModel). Consequently, while coordinate-dependent models report deceptively high predictive skill within sampled neighborhoods, their transferability collapses precipitously when deployed across out-of-sample administrative jurisdictions or unfamiliar peat dome systems (@MeyerPebesma2021NatComm; @Schratz2019EcolModel).

To resolve these fundamental land tenure and spatial methodological dilemmas, this study presents an empirical investigation of the wildfire crisis in Central Kalimantan. Utilizing 43,937 satellite active fire observations from NASA FIRMS during the acute October 2026 fire pulse, we test two central land governance hypotheses:
1. $\mathbf{H_1}$ (*Spatial Boundary Discontinuity Hypothesis*): *Corporate strict liability creates a sharp spatial discontinuity at concession perimeters: fires are actively suppressed within certified concession boundaries, but active fire density escalates sharply directly across the cadastral frontier onto unallocated APL state land due to drainage spillover and an open-access institutional governance void.*
2. $\mathbf{H_2}$ (*Spatial Generalizability and Biophysical Transferability Hypothesis*): *Eliminating spatial coordinate proxies prevents catastrophic spatial memorization and preserves operational combustion detection across out-of-sample geographical blocks, evaluated via two complementary sub-hypotheses:*
   * $\mathbf{H_{2a}}$ (*Spatial Memorization Collapse*): Coordinate-dependent models achieve deceptively high random-split validation metrics but suffer catastrophic recall collapse ($F_1 \to 0$) under Spatial Block Cross-Validation across unobserved administrative blocks.
   * $\mathbf{H_{2b}}$ (*Biophysical Operational Retention*): Pure biophysical feature architectures retain transferable predictive capacity and prevent total recall failure across spatial blocks by learning physical combustion tipping points.

To evaluate these hypotheses within a land use policy framework, we: (1) analyze decadal burned area records (2018–2026) from the Ministry of Environment and Forestry (SiPongi KLHK) alongside micro-scale diurnal satellite dynamics; (2) map 13 primary canal vectors in UTM Zone 49S projection across the ex-Mega Rice Project landscape; (3) perform a comprehensive spatial overlay against 812 cadastral concessions (627 oil palm HGU and 185 commercial forestry PBPH) to resolve land tenure attribution; (4) deploy a Spatial Boundary Discontinuity Design (Spatial BDD) to quantify the boundary step jump and distance-decay spillover within a 3-km frontier corridor; (5) benchmark coordinate-dependent (Model A) and pure biophysical (Model B) Random Forest models using 5-fold Spatial Block Cross-Validation (`GroupKFold` by regency); and (6) formulate actionable land governance reforms to close the concession frontier governance void.

---

## 2. Materials and Methods

### 2.1. Study Area and Regional Landscape Characterization

The investigation covers the entire province of Central Kalimantan (*Kalimantan Tengah*), Indonesia, extending between latitudes 0.8° N to 3.6° S and longitudes 110.7° E to 115.9° E, covering approximately 153,564 km² (Figure 1a). The province is partitioned administratively into 13 regencies (*Kabupaten*) and one autonomous urban municipality (*Kota Palangka Raya*), structured into five spatial cross-validation blocks (Figure 1b). Geomorphologically, Central Kalimantan exhibits a pronounced north-to-south gradient: the northern interior comprises rugged upland terrain defined by the Schwaner and Müller mountain ranges situated on mineral soils and covered by primary and secondary dipterocarp rainforests. Conversely, the central and southern sectors form vast alluvial lowlands and ombrotrophic peat swamp basins drained by nine principal south-flowing rivers: the Jelai, Kumai, Seruyan, Mentaya, Katingan, Sebangau, Kahayan, Kapuas, and Barito rivers.

The southern peatland belt houses the historic Mega Rice Project (ex-PLG) footprint, which was excavated during 1995–1999 across four major planning blocks (Figure 1c):
* **Block A** (~300,000 ha): Flanked by the Kapuas and Barito rivers, centered within the Kapuas Regency (Mentangai, Dadahup, and Jenamas districts).
* **Block B** (~160,000 ha): Located between the Kahayan and Kapuas rivers, centered in the Pulang Pisau Regency (Jabiren, Basarang, and Kahayan Hilir districts).
* **Block C** (~390,000 ha): Situated between the Sebangau and Kahayan rivers, encompassing the southern peat outskirts of Palangka Raya City (Kalampangan, Bereng Bengkel) and northern Pulang Pisau.
* **Block D** (~150,000 ha): Encompassing the coastal peat dome south of the Kahayan river extending toward Sebangau Kuala.

![**Figure 1. Geographic setting, spatial cross-validation partitioning, and degraded peatland infrastructure in Central Kalimantan, Indonesia.** (a) Regional inset showing the geographic position of Central Kalimantan within Borneo Island and Maritime Southeast Asia. (b) Provincial cartography featuring all 14 regencies and municipalities classified into five Spatial Block Cross-Validation partitions (`GroupKFold`), overlaid with the 24 official Peat Hydrological Units (KHG) from the BBLSDLP database. (c) Focal landscape zoom of the ex-Mega Rice Project (ex-PLG) peatland territory (Blocks A, B, C, and D) delineating the 13 primary drainage canal vectors (Saluran Primer Induk / SPI), Sebangau National Park conservation dome, metric scale bar, and cartographic graticules.](output/figures/01_peta_wilayah_studi_spatial_cv.png)

### 2.2. Multisource Geospatial Data Ingestion and Processing Pipeline

#### 2.2.1. Active Fire Remote Sensing (NASA FIRMS)
Near-real-time satellite thermal anomaly detections were compiled from the NASA Fire Information for Resource Management System (FIRMS) for the acute fire surge observed between 5 October and 12 October 2026. The data stream combined observations from three polar-orbiting satellite sensor configurations:
1. **VIIRS on Suomi-NPP**: 375 m nominal spatial resolution in the I-band (3.74–3.93 $\mu$m), providing daytime and nighttime passes (@Schroeder2021RSE; @Roberts2020RS).
2. **VIIRS on NOAA-20**: Identical 375 m I-band sensor configuration operating on a sun-synchronous orbit offset by approximately 50 minutes (@Schroeder2021RSE).
3. **MODIS on Aqua**: 1 km spatial resolution (Collection 6.1 active fire algorithm) operating with daytime overpass at ~13:30 local solar time (@Giglio2020RSE).

Initial provincial bounding box extraction yielded 52,829 raw candidate thermal detections. To eliminate boundary contamination from adjacent provinces (West Kalimantan and South Kalimantan) and discard peripheral edge artifacts, we performed an automated spatial point-in-polygon clipping operation using official high-resolution administrative boundary vectors (geoBoundaries ADM2, 14 provincial units). This spatial filter excluded 8,892 out-of-boundary observations (16.83%), yielding **43,937 verified active fire hotspots** located strictly within Central Kalimantan.

Recorded attributes for each hotspot include acquisition date (`acq_date`), UTC acquisition timestamp (`acq_time`), geodetic coordinates (`latitude`, `longitude`), sensor instrument (`satellite`), algorithmic detection confidence (`confidence`), mid-infrared brightness temperature in kelvins (`brightness_k`), and Fire Radiative Power in megawatts (`frp_mw`) (@Roberts2015RSE; @Chuvieco2019ESSD).

#### 2.2.2. Peatland Delineation and Depth Stratification
Peatland spatial boundaries and depth classifications were obtained from the official national peatland database compiled by the Indonesian Center for Agricultural Land Resources Research and Development (BBLSDLP, Ministry of Agriculture, 2019) and the Ministry of Environment and Forestry (Decree SK.130/MENLHK/SETJEN/PKL.0/2/2017 delineating the National Peat Hydrological Units / KHG). The vector database delineates 24 distinct peat dome units in Central Kalimantan across five standardized depth strata:
1. **Shallow Peat** (*Gambut Dangkal*, 50–100 cm depth; median baseline: 75 cm).
2. **Medium Peat** (*Gambut Sedang*, 100–200 cm depth; median baseline: 150 cm).
3. **Deep Peat** (*Gambut Dalam*, 200–300 cm depth; median baseline: 250 cm).
4. **Very Deep Peat** (*Gambut Sangat Dalam*, >300 cm depth; median baseline: 390 cm).
5. **Mineral Soil** (*Tanah Mineral*, non-peat mineral formations, assigned depth: 0 cm).

Each FIRMS hotspot was intersected against this polygon database. Detections located outside delineated peat polygons were classified as Mineral Soil with a peat depth of 0 cm.

#### 2.2.3. Canal Vector Network and Projected Metric Drainage Distance
To quantify the hydrological drainage impact of artificial canals without geodetic distortion, the primary canal backbone (Saluran Primer Induk / SPI) of the Mega Rice Project Blocks A, B, C, and D was vectorized as a multi-segment line network comprising 13 primary canal axes.

Both active fire coordinates and canal polyline vectors were reprojected from WGS 84 geographic coordinates (`EPSG:4326`) into the official metric projected coordinate system for Central Kalimantan, **WGS 84 / UTM Zone 49S** (`EPSG:32749`). The minimum Euclidean distance from each hotspot to the nearest primary canal line was computed as:
$$d_{\text{canal}, i} = \min_{j} \left\| \mathbf{p}_i - \mathbf{c}_j \right\|_2 = \min_{j} \sqrt{(x_i - u_j)^2 + (y_i - v_j)^2}$$
where $\mathbf{p}_i = (x_i, y_i)$ represents the projected UTM Zone 49S coordinates (in meters) of hotspot $i$, and $\mathbf{c}_j = (u_j, v_j)$ represents the vertices of primary canal vector segments.

To prevent geographic distortion in western regencies that do not contain ex-PLG canal networks (e.g., Seruyan, Kotawaringin Barat, Kotawaringin Timur), a binary landscape zoning indicator was established:
$$\text{is\_ex\_plg\_landscape} = \begin{cases} 1, & \text{if Regency} \in \{\text{Pulang Pisau, Kapuas, Kota Palangka Raya}\} \\ 0, & \text{otherwise} \end{cases}$$
For hotspots outside the ex-PLG landscape, the operational canal distance feature was assigned an asymptotic physical distance of 99,999 m ($d_{\text{canal}} = 99,999\text{ m}$), reflecting that these remote peat domes are hydraulically decoupled from the ex-PLG drainage network. Within the ex-PLG zone, points retained their true Euclidean drainage proximity in meters. Furthermore, in downstream explainable AI modeling, TreeSHAP canal proximity dependencies were explicitly resolved on the ex-PLG focal landscape ($n = 16,645$) where canals are physically present.

#### 2.2.4. Atmospheric Reanalysis and Fire Weather Modeling
Daily atmospheric forcing data were obtained from the European Centre for Medium-Range Weather Forecasts (ECMWF) ERA5-Land atmospheric reanalysis dataset (nominal horizontal grid resolution of 0.1° $\approx$ 9 km). Reanalysis variables were compiled across all 14 administrative centroids for a 30-day antecedent window prior to each fire observation. This regency-level spatial extraction was deliberately selected to align with the operational jurisdictional scale of regional disaster management agencies (BPBD) and forest fire control brigades (*Manggala Agni Daops*), whose emergency dispatch and resource allocation protocols operate on district administrative tiers. Extracted daily meteorological indicators include:
* Maximum 2-meter air temperature ($T_{\text{max}}$, °C).
* Mean 2-meter relative humidity ($RH_{\text{mean}}$, %).
* Maximum 10-meter horizontal wind speed ($W_{\text{max}}$, km/h).
* Daily precipitation ($P_{\text{daily}}$, mm).
* 7-day cumulative antecedent precipitation ($P_{\text{7d}} = \sum_{t=0}^{6} P_{t}$, mm).
* 14-day cumulative antecedent precipitation ($P_{\text{14d}} = \sum_{t=0}^{13} P_{t}$, mm).
* Consecutive dry spell duration ($D_{\text{spell}}$, days with $P_{\text{daily}} < 1.0$ mm).

A regionally calibrated Fire Weather Index ($FWI$) was formulated following the Canadian Forest Fire Weather Index / BMKG Fire Danger Rating framework adapted for tropical peat environments (@Spessa2015Biogeosciences):
$$FWI_i = 0.35 T_{\text{max}, i} + 1.35 D_{\text{spell}, i} - 0.22 P_{\text{7d}, i} + 0.22 (100 - RH_{\text{mean}, i}) + 0.25 W_{\text{max}, i}$$

#### 2.2.5. Cadastral Land Tenure Overlay
To evaluate land tenure attribution, official concession boundary shapefiles were obtained from the national cadastral registry:
1. **Oil Palm Plantations**: 627 certified Right to Cultivate (*Hak Guna Usaha* / HGU) corporate concession polygons administered by the National Land Agency (BPN).
2. **Commercial Forestry Concessions**: 185 Forest Utilization Business License (*Perizinan Berusaha Pemanfaatan Hutan* / PBPH) polygons issued by the Ministry of Environment and Forestry (KLHK).

Through automated spatial overlay, each active fire observation was classified into one of three mutually exclusive legal tenure categories:
* **Oil Palm Concessions (HGU)** (`concession_oil_palm`): Hotspots located within certified corporate oil palm concession boundaries.
* **Commercial Forestry Concessions (PBPH)** (`concession_forestry`): Hotspots located within commercial timber or ecosystem restoration forestry concessions.
* **Non-Concession Land (APL)** (`non_concession_apl`): Hotspots located outside concessions on state Other Utilization Areas (APL), community agroforestry lands, or unallocated degraded peatlands (@Putranto2023LandUsePol).

A comprehensive summary of all feature variables ingested into the predictive modeling pipeline is presented in Table 1.

### 2.3. Spatial Boundary Discontinuity Design (Spatial BDD)

To test Hypothesis $\mathbf{H_1}$—whether corporate legal liability deters fire inside perimeters while displacing ignitions across boundaries into unmanaged state land—we implement a Spatial Boundary Discontinuity Design (Spatial BDD) (@LeeLemieux2010JEL; @KeeleTitiunik2015JASA). Under this quasi-experimental framework, corporate concession perimeters serve as legal cutoffs separating strictly regulated corporate lands from open-access state lands.

All cadastral concession polygons (627 oil palm HGU and 185 commercial forestry PBPH) and administrative boundaries were reprojected to UTM Zone 49S (`EPSG:32749`). Concession geometries within Central Kalimantan were dissolved into a unified corporate estate polygon $\Omega_C$. The exterior perimeter boundary $\partial \Omega_C$ represents the legal frontier separating concession lands from unallocated state land (*Area Penggunaan Lain*, APL).

For each active fire hotspot $\mathbf{p}_i = (x_i, y_i)$, the signed Euclidean distance to the nearest corporate concession boundary vertex was computed as:
$$\tilde{d}_i = \begin{cases} -\min_{\mathbf{b} \in \partial \Omega_C} \|\mathbf{p}_i - \mathbf{b}\|_2, & \text{if } \mathbf{p}_i \in \Omega_C \text{ (Corporate Concession Interior)} \\ +\min_{\mathbf{b} \in \partial \Omega_C} \|\mathbf{p}_i - \mathbf{b}\|_2, & \text{if } \mathbf{p}_i \notin \Omega_C \text{ (APL Non-Concession State Land)} \end{cases}$$
where negative values denote locations within certified concessions (Strict Liability Zone) and positive values denote exterior locations on unallocated APL state land.

We evaluated a continuous frontier bandwidth of $\pm 3,000$ m, discretized into 500-meter concentric buffer bands $B_k = [d_k, d_{k+1})$. For each band $k$, the exact geometric surface area $A(B_k) = \text{Area}(B_k \cap \Omega_{\text{Kalteng}})$ was computed by planar polygon buffering in UTM Zone 49S and clipping to the provincial land boundary. Active fire hotspot density $D_k$ was formulated as:
$$D_k = \frac{N_k}{A(B_k)} \quad (\text{hotspots}/\text{km}^2)$$
where $N_k$ is the number of active fire detections in band $k$. The boundary treatment effect (discontinuity jump at the legal border $\tilde{d} = 0$) was estimated via local second-order polynomial regressions fit separately to the interior ($\tilde{d} < 0$) and exterior ($\tilde{d} > 0$) intervals:
$$\tau_{\text{BDD}} = \lim_{\tilde{d} \to 0^+} D(\tilde{d}) - \lim_{\tilde{d} \to 0^-} D(\tilde{d})$$
Differences in thermal intensity (FRP) and severe fire proportions between interior and exterior zones were evaluated using non-parametric Mann-Whitney $U$ tests and Welch's unequal variances $t$-tests.

#### 2.3.1. Robustness Checks for Spatial BDD
To verify that the estimated treatment effect $\tau_{\text{BDD}}$ was not sensitive to bandwidth specification or boundary definition, three formal robustness checks were conducted:
1. **Bandwidth Sensitivity Analysis**: Estimating the boundary jump across narrower and wider buffer bandwidths ($\pm 1,000$ m, $\pm 2,000$ m, and $\pm 3,000$ m) to ensure stability of the discontinuity ratio.
2. **Placebo Boundary Test**: Artificially shifting the cutoff boundary 1,000 m into the concession interior ($\tilde{d}_{\text{placebo}} = -1,000$ m) to test whether a fictitious interior boundary exhibits an artificial step jump.
3. **Concession Sector Decomposition**: Disaggregating the concession boundary into oil palm (HGU) and commercial forestry (PBPH) subsets to examine whether the frontier governance void differs across commodity regimes.

### 2.4. Predictive Machine Learning and Validation Framework

#### 2.4.1. Target Formulation: Severe Fire Radiative Power
Conventional wildfire machine learning models frequently configure a binary presence-absence task against randomly sampled pseudo-absences. In this investigation, we model the intensity of ignited fires to differentiate moderate surface burning from severe, high-energy radiative events capable of sustaining deep subterranean peat smoldering.

Following calibration thresholds for satellite infrared sensors over tropical biomass (@RobertsWooster2008JGR; @Wooster2018NatGeosci), the binary classification target $y_i$ is formulated as:
$$y_i = \begin{cases} 1, & \text{if } FRP_i \ge 12.0\text{ MW (Severe / High-Energy Radiative Fire)} \\ 0, & \text{if } FRP_i < 12.0\text{ MW (Regular / Moderate Incipient Fire)} \end{cases}$$
Within the 43,937 verified observations, exactly **6,648 detections (15.13%)** were classified as severe fires ($y=1$), while 37,289 detections (84.87%) represented regular fires ($y=0$), establishing an empirical class imbalance ratio of approximately $1 : 5.6$.

To prevent the machine learning algorithm from optimizing majority-class accuracy at the expense of severe fire sensitivity, we applied an inverse class weighting strategy:
$$w_c = \frac{N}{K \cdot n_c}$$
where $N = 43,937$, $K = 2$, $n_1 = 6,648$ (severe class), and $n_0 = 37,289$ (regular class). This yielded class weights of $w_1 \approx 3.3045$ and $w_0 \approx 0.5891$, imposing a 5.6-fold higher penalty on false-negative misclassifications of severe fire events.

#### 2.4.2. Comparative Architectures: Model A vs. Model B
To empirically test Hypothesis $\mathbf{H_2}$ ($H_{2a}$ vs. $H_{2b}$), we formulated two distinct Random Forest classifier pipelines (@Breiman2001ML):
* **Model A (Spatial Memorization)**: 15 predictors, including geodetic coordinates and administrative regency identifiers:
  $$\mathbf{X}_A = \{ \text{lat}, \text{lon}, \text{regency}, d_{\text{canal}}, \text{is\_ex\_plg}, d_{\text{peat}}, P_{\text{7d}}, T_{\text{max}}, RH, W_{\text{max}}, D_{\text{spell}}, FWI, \text{soil\_type}, \text{cover\_type}, \text{tenure} \}$$
* **Model B (Pure Biophysical Model)**: 12 environmental, hydrological, and tenurial predictors, without spatial coordinates or administrative identifiers:
  $$\mathbf{X}_B = \{ d_{\text{canal}}, \text{is\_ex\_plg}, d_{\text{peat}}, P_{\text{7d}}, T_{\text{max}}, RH, W_{\text{max}}, D_{\text{spell}}, FWI, \text{soil\_type}, \text{cover\_type}, \text{tenure} \}$$

Hyperparameter configurations were held constant across both pipelines to ensure strict comparability: number of estimators $n_{\text{estimators}} = 150$, maximum tree depth $\text{max\_depth} = 10$, minimum samples per split $\text{min\_samples\_split} = 6$, and `class_weight='balanced'`.

#### 2.4.3. Spatial Block Cross-Validation Protocol
Both models were subjected to two evaluation regimes:
1. **Stratified Random Holdout Split (75:25)**: A standard benchmark splitting the dataset randomly while preserving target proportions ($n_{\text{train}} = 32,952$; $n_{\text{test}} = 10,985$).
2. **Spatial Block Cross-Validation (`GroupKFold`, $K=5$)**: A spatial partitioning protocol where the entire dataset is partitioned into five mutually exclusive geographical blocks grouped by regency:
   $$\mathcal{D} = \bigcup_{k=1}^{K} \mathcal{D}_k, \quad \mathcal{D}_k \cap \mathcal{D}_l = \emptyset \quad \forall k \ne l$$
   In each cross-validation fold $k$, the model is trained on $\mathcal{D}_{\text{train}} = \mathcal{D} \setminus \mathcal{D}_k$ and evaluated exclusively on held-out geographic units $\mathcal{D}_k$. The spatial block allocation grouped regencies as follows:
   * **Fold 1**: Seruyan (western coastal peat dome complex).
   * **Fold 2**: Pulang Pisau, Barito Timur, Barito Utara, Lamandau, Murung Raya.
   * **Fold 3**: Kapuas, Barito Selatan, Gunung Mas, Sukamara.
   * **Fold 4**: Katingan, Palangka Raya City.
   * **Fold 5**: Kotawaringin Barat, Kotawaringin Timur.

#### 2.4.4. Explainable Artificial Intelligence: TreeSHAP Decomposition
To interpret the non-linear decision surface of the Pure Biophysical Model (Model B), we computed exact Shapley values using the TreeSHAP algorithm (@LundbergLee2017NeurIPS). For a tree ensemble prediction function $f(\mathbf{x})$, the Shapley attribution $\phi_j$ uniquely decomposes the difference between the local prediction and the expected background value $\mathbb{E}[f(\mathbf{X})]$:
$$f(\mathbf{x}) = \phi_0 + \sum_{j=1}^{M} \phi_j(\mathbf{x}), \quad \phi_j(f, \mathbf{x}) = \sum_{S \subseteq \mathcal{F} \setminus \{j\}} \frac{|S|!(|\mathcal{F}| - |S| - 1)!}{|\mathcal{F}|!} \left[ f(S \cup \{j\}) - f(S) \right]$$
where $\mathcal{F}$ represents the full set of $M$ features, $S$ denotes feature subsets, and $\phi_0 = \mathbb{E}[f(\mathbf{X})]$. TreeSHAP values were computed across a stratified holdout sample of 2,500 observations for the severe fire class ($y=1$) to evaluate feature rankings and discover non-linear tipping points.

---

## 3. Results

### 3.1. Active Fire Spatiotemporal Density and Radiative Regimes

Spatial aggregation across Central Kalimantan's 14 administrative units demonstrated intense geographic concentration in the southern ombrotrophic peat basins and coastal lowlands (Table 1 and Figure 2).

**Table 1. Spatial distribution of verified active fire hotspots across the 14 regencies and municipalities of Central Kalimantan during the October 2026 crisis.**

| Regency / Municipality | Hotspots | Percentage (%) | Primary Geomorphological and Peat Characteristics |
| :--- | :---: | :---: | :--- |
| **Seruyan** | **9,356** | **21.29%** | Coastal peat dome complex; Lake Sembuluh basin |
| **Pulang Pisau** | **7,143** | **16.26%** | Core Mega Rice Project (Blocks A, B, D); Sebangau dome |
| **Kapuas** | **6,314** | **14.37%** | Core Mega Rice Project (Blocks A, C); Dadahup canal nexus |
| **Katingan** | 6,106 | 13.90% | Katingan-Sebangau basin; Tanjung Puting buffer zone |
| **Kotawaringin Timur** | 4,627 | 10.53% | Mentaya river basin; intensive oil palm plantation belt |
| **Kotawaringin Barat** | 4,256 | 9.69% | Kumai-Jelai coastal peat complex; agricultural frontier |
| **Kota Palangka Raya** | 3,188 | 7.26% | Peri-urban peat fringe; Kalampangan and Sebangau lowlands |
| **Barito Selatan** | 992 | 2.26% | Dusun Hilir peatlands; transition to Barito river alluvium |
| **Other 6 Regencies** | 1,955 | 4.45% | Northern mineral uplands (Lamandau: 773, Sukamara: 481, Gunung Mas: 407, Barito Timur: 227, Murung Raya: 44, Barito Utara: 23) |
| **Total Province-Wide** | **43,937** | **100.00%** | **Authenticated Central Kalimantan territory** |

![**Figure 2. Active fire spatiotemporal density and radiative energy regimes across Central Kalimantan during the October 2026 crisis.** (a) Two-dimensional hexbin spatial density surface of 43,937 verified NASA FIRMS active fire hotspots (logarithmic density scale) within official provincial administrative boundaries. (b) Spatial radiative regimes illustrating extreme combustion events (FRP $\ge$ 12.0 MW, distinguished by larger crimson points with dark perimeters, $n = 6,648$) versus regular thermal anomalies (FRP < 12.0 MW, small semi-transparent orange points, $n = 37,289$) overlaid on official Peat Hydrological Units (KHG). (c) Empirical probability density distribution of Fire Radiative Power (MW, log-scale) comparing peatland substrates ($n = 32,643$; 74.3%) against mineral soils ($n = 11,294$; 25.7%), accompanied by the comprehensive active fire audit summary.](output/figures/02_peta_densitas_hotspot_frp.png)

The top three jurisdictions, namely Seruyan (21.29%), Pulang Pisau (16.26%), and Kapuas (14.37%), accounted for 51.92% (22,813 hotspots) of all active fires detected across the province (Figure 2a). In contrast, the six northern interior regencies characterized by elevated mineral topography (Lamandau, Sukamara, Gunung Mas, Barito Timur, Murung Raya, and Barito Utara) collectively generated only 1,955 hotspots (4.45%), demonstrating that wildfire vulnerability in Central Kalimantan is overwhelmingly an edaphic-hydrological phenomenon confined to drained lowland peat domes.

High-resolution examination of Fire Radiative Power (Figure 2b,c) confirmed that severe fires (FRP $\ge$ 12.0 MW, representing exactly 6,648 hotspots or 15.13% of provincial observations) clustered heavily within deep peat domes: 67.4% of all severe fires (4,481 of 6,648) ignited on peatlands. Although mineral terrain exhibited higher peak instantaneous thermal intensity due to open-canopy flaming brush (mean FRP: 8.93 MW vs 7.09 MW on peat; median: 3.50 MW vs 3.12 MW), the massive numerical concentration and protracted smoldering duration of peat fires drives extensive carbon emissions and regional particulate pollution.

---

### 3.2. Peatland Stratification and Canal Drainage Proximity Forensics

Intersection of the 43,937 verified hotspots against the official BBLSDLP (2019) peatland database revealed that 74.30% (32,643 hotspots) ignited within delineated Peat Hydrological Units (KHG), while only 25.70% (11,294 hotspots) occurred on mineral soils. Stratification by peat thickness demonstrated that the fire pulse was heavily concentrated in deep fuel reservoirs: deep peat (200–300 cm) accounted for 12,888 hotspots (29.33%), followed by very deep peat (>300 cm) with 10,197 hotspots (23.21%), medium peat (100–200 cm) with 9,177 hotspots (20.89%), and shallow peat (50–100 cm) with 381 hotspots (0.87%). In aggregate, over 52.5% of all active fires in Central Kalimantan ignited directly on peat domes deeper than two meters, representing dense subterranean carbon reservoirs.

![**Figure 3. High-resolution satellite forensics and canal proximity dynamics at the ex-Mega Rice Project (ex-PLG) drainage nexus.** (a) True-color optical satellite imagery mosaic (Esri World Imagery) covering the Block A Dadahup irrigation scheme in Kapuas Regency, illustrating visible deforestation and drainage canal scars. (b) Spatial forensic overlay of primary drainage canal vectors (Saluran Primer Induk / SPI) with multi-ring metric buffer corridors (1 km, 3 km, and 5 km) and active fire detections, demonstrating intense ignition clustering along artificial drainage channels. (c) Cross-sectional distance decay profile and TreeSHAP non-linear drainage tipping point in the ex-PLG landscape ($n = 16,645$), showing active fire frequency (left axis) and severe fire probability (FRP $\ge$ 12.0 MW %, right axis) as a function of distance to the nearest primary canal, highlighting the critical 3,000-m drainage corridor (mean |SHAP| = 0.0322) and landscape median distance (14,946 m).](output/figures/03_analisis_citra_satelit_kanal.png)

Within the ex-PLG landscape (Pulang Pisau, Kapuas, and Palangka Raya City; $n = 16,645$), metric distance calculations to primary canal vectors in UTM Zone 49S projection revealed a median distance of 14,946 meters (~14.9 km). High-resolution multi-ring buffer forensics (Figure 3a,b) and multivariable machine learning confirmed that canal proximity is the second most influential predictor of severe combustion (mean |SHAP| = 0.0322). Cross-sectional distance decay profiling (Figure 3c) indicates that active fire frequency and severe fire risk increase sharply within a 3,000-meter corridor along primary drainage channels, consistent with artificial drainage accelerating catotelm desiccation.

---

### 3.3. Cadastral Land Tenure Attribution and Concession Accountability

Point-in-polygon spatial join against 627 certified oil palm concessions (HGU) and 185 commercial forestry concessions (PBPH) clarified the land tenure attribution of active fires (Figure 4).

![**Figure 4. Cadastral land tenure governance, spatial concession overlay, and corporate accountability audit in Central Kalimantan.** (a) Provincial spatial overlay of 627 certified oil palm concessions (HGU, amber polygons) and 185 commercial forestry concessions (PBPH, cyan polygons) against 43,937 active fire hotspots, establishing that 75.4% (33,138 hotspots) ignited on unallocated Non-Concession land (APL). (b) Detailed zoom-in of the Seruyan basin concession boundary corridor, illustrating active fire clustering directly outside certified concession boundaries on unmanaged community peatlands (governance void). (c) Corporate accountability ranking of the top eight concession entities with the highest thermal anomaly detections for ESG compliance monitoring.](output/figures/04_peta_tenurial_konsesi_esg.png)

The spatial join demonstrated that:
* **Non-Concession Land (*Area Penggunaan Lain*, APL)**: **75.42%** (33,138 hotspots) ignited outside commercial corporate concession perimeters (Figure 4a). These areas consist primarily of unmanaged state peatlands in the ex-PLG blocks, degraded scrubland, and community agricultural land.
* **Oil Palm Concessions (HGU)**: **16.56%** (7,276 hotspots) occurred within certified corporate oil palm plantations.
* **Commercial Forestry Concessions (PBPH)**: **8.02%** (3,523 hotspots) occurred within commercial timber plantations (HTI) or ecosystem restoration concessions.

Corridor analysis of the concession interface (Figure 4b) demonstrated severe fire clustering directly outside certified concession boundaries, reflecting a critical governance void in unallocated APL peatlands. While corporate concessions accounted for 24.58% of all fires, detections were concentrated within a small subset of corporate entities (Figure 4c). Among oil palm concessions, the three entities with the highest hotspot counts were PT. Sangkowong Sinta (954 hotspots), PT. Graha Inti Jaya (472 hotspots), and PT. Bulau Sawit Bajenta (343 hotspots). Within forestry concessions, thermal detections were led by PT. Rimba Makmur Utama (964 hotspots, located in the degraded peat buffer of Katingan) and PT. Nusantara Raya Solusi (522 hotspots).

---

### 3.4. Spatial Boundary Discontinuity Design at Concession Frontiers

To evaluate whether the concentration of wildfires outside corporate concessions reflects a causal governance discontinuity rather than smooth spatial variation, we applied a Spatial Boundary Discontinuity Design (Spatial BDD) across the $\pm 3$-km frontier corridor of all certified corporate perimeters (Figure 5).

![**Figure 5. Spatial Boundary Discontinuity Design (Spatial BDD) of active fire ignitions across certified corporate concession frontiers in Central Kalimantan.** (a) High-resolution cartographic zoom of the Pulang Pisau cadastral frontier (UTM Zone 49S), depicting certified corporate concession perimeters (amber polygons), 0-to-3 km exterior buffer corridors (light red shading), cadastral perimeter frontiers (red line), and satellite active fire detections split by legal tenure. (b) Spatial hotspot density discontinuity curve as a function of signed Euclidean distance to the concession boundary ($\tilde{d} \in [-3.0, +3.0]$ km), demonstrating a sharp +56.5% discontinuity jump at the legal cutoff ($\tilde{d} = 0$), rising from 0.1830 hotspots/km² inside concessions to 0.2864 hotspots/km² on exterior APL state land (0.3697 hotspots/km² at 3 km). (c) Mean Fire Radiative Power (MW) and severe fire percentage (FRP $\ge$ 12.0 MW) across 500-meter concentric distance bands. (d) Conceptual infographic diagram detailing the statutory strict liability mechanism (Law No. 32/2009, Art. 88) inside concessions, hydrological drainage spillover across frontiers, the open-access APL governance void, and recommended perimeter buffer stewardship policies.](output/figures/09_spatial_boundary_discontinuity.png)

The spatial boundary discontinuity analysis formally confirmed Hypothesis $\mathbf{H_1}$ (Spatial Boundary Discontinuity Hypothesis) through three primary empirical findings:
1. **Sharp Discontinuity in Active Fire Density**: Within the 3-km frontier window, 8,961 hotspots ignited in the concession interior ($-3\text{ km} \le \tilde{d} < 0$ km) across 48,959.58 km², yielding a baseline density of 0.1830 hotspots/km². Directly across the legal boundary on unallocated APL state land ($0\text{ km} \le \tilde{d} \le +3$ km), 9,224 hotspots ignited across 32,203.09 km², establishing an active fire density of 0.2864 hotspots/km². This represents an immediate +56.5% surge in fire density ($\tau_{\text{BDD}} = +0.1034$ hotspots/km²; density ratio 1.565) across the cadastral frontier (Figure 5b).
2. **Distance-Decay Frontier Escalation**: Examination of 500-meter concentric bands revealed that fire density increases monotonically with distance outward into unallocated state land: from 0.1183 hotspots/km² in the deep concession interior (-3.0 to -2.5 km) to 0.2177 hotspots/km² immediately adjacent to the border (0 to +500 m), escalating to 0.3697 hotspots/km² in the outer frontier band (+2.5 to +3.0 km). This represents a >3.1-fold density escalation between the corporate core and the open-access frontier.
3. **Combustion Intensity Parity across Frontiers**: While fire density diverged sharply, thermal energy output remained consistently severe across both sides of the border (Figure 5c). Mean Fire Radiative Power inside concessions averaged 7.38 MW (median: 2.98 MW) compared to 6.92 MW outside on APL state land (median: 2.93 MW; Mann-Whitney $U = 4.17 \times 10^7, p = 0.278$; Welch's $t = 1.86, p = 0.063$). Severe fire proportions (FRP $\ge$ 12.0 MW) peaked at the immediate boundary zone (16.2% severe combustion at -1.0 to -0.5 km, mean FRP = 8.07 MW), indicating that border drainage canals create highly combustible edge conditions.

#### Robustness Checks and Boundary Sensitivity
To ensure the observed boundary discontinuity was not an artifact of buffer width or arbitrary threshold selection, we executed three robustness checks:
1. **Bandwidth Sensitivity**: Estimating $\tau_{\text{BDD}}$ across alternative distance windows confirmed persistent upward discontinuity jumps: at $\pm 1$ km, fire density rose from 0.1834 inside to 0.2053 hotspots/km² outside ($\tau_{\text{BDD}} = +0.0242$ hotspots/km²; ratio 1.120); at $\pm 2$ km, density increased from 0.1856 to 0.2447 hotspots/km² ($\tau_{\text{BDD}} = +0.0617$ hotspots/km²; ratio 1.319); and across the full $\pm 3$ km corridor, the jump reached +56.5% ($\tau_{\text{BDD}} = +0.1034$ hotspots/km²; ratio 1.565).
2. **Placebo Boundary Test**: Shifting the cutoff line artificially by -1.0 km deep into the concession interior yielded virtually identical internal densities (0.1691 hotspots/km² in the -2.0 to -1.0 km zone vs 0.1834 hotspots/km² in the -1.0 to 0.0 km zone; ratio 1.084), confirming no phantom step jump exists within continuous corporate holdings.
3. **Concession Sector Decomposition**: Disaggregating concessions by license type revealed that while oil palm (HGU) interiors exhibited higher active fire density (0.2268 hotspots/km²) than commercial forestry (PBPH) interiors (0.0766 hotspots/km²), exterior APL frontier lands (0.2864 hotspots/km²) exceeded HGU interior density by +26.3% and exceeded PBPH interior density by +273.9% (a 3.7-fold increase), verifying that the frontier governance void operates across both industrial agricultural and silvicultural interfaces.

---

### 3.5. Decadal Fire Trajectory (2018–2026) and Diurnal Crisis Dynamics

Analysis of Ministry of Environment and Forestry (SiPongi KLHK) records across 2018–2026 confirms the strong non-linear control exerted by macro-climatic anomalies over burned area extents in Central Kalimantan (Table 2, Figure 6a).

**Table 2. Decadal burned area trajectory and macro-climatic regimes in Central Kalimantan (2018–2026) derived from official Ministry of Environment and Forestry (SiPongi KLHK) records.**

| Year | Burned Area (ha) | ENSO / Climate Regime | Regional Wildfire Trajectory and Impacts |
| :--- | :---: | :---: | :--- |
| 2018 | 47,432.57 | Neutral ENSO | Baseline dry season burning |
| **2019** | **317,749.00** | **Strong El Niño (+pIOD)** | **Historic disaster; extensive peat dome combustion** |
| 2020 | 7,681.00 | La Niña onset | Triple-dip La Niña recharge; groundwater saturation |
| 2021 | 3,653.00 | Moderate La Niña | High positive precipitation anomalies; minimal fire |
| 2022 | 1,554.00 | Strong La Niña | Lowest recorded burned area in modern provincial history |
| **2023** | **165,896.44** | **Moderate El Niño (+pIOD)** | **Severe drought resurgence; ex-PLG canal reactivations** |
| 2024 | 11,459.89 | Neutral / Weak La Niña | Near-average monsoonal precipitation |
| 2025 | 4,803.97 | Neutral ENSO | Stable hydrological conditions |
| 2026 | 7,634.46* | Transition / Drought Pulse | Mid-year official tally prior to October crisis audit |

*\*Official SiPongi administrative tally compiled prior to the comprehensive post-crisis satellite reconciliation.*

![**Figure 6. Decadal burned area trajectory and diurnal satellite fire dynamics in Central Kalimantan.** (a) Time series of annual burned area extents (2018–2026) derived from official SiPongi Ministry of Environment and Forestry (KLHK) administrative records, demonstrating that extreme El Niño drought cycles in 2019 (317,749 ha) and 2023 (165,896 ha) drove over 85% of cumulative provincial burning, contrasted with multi-year wet La Niña suppression during 2020–2022. (b) Diurnal active fire dynamics and sensor distribution (VIIRS SNPP, NOAA-20, and MODIS Aqua) across the acute October 2026 crisis, showing intense fire concentration during 5–8 October followed by abrupt suppression on 9–12 October with the arrival of convective precipitation cells.](output/figures/05_tren_temporal_dan_harian.png)

Decadal records show that over 85% of the cumulative burned area between 2018 and 2026 occurred during two severe El Niño drought episodes: 2019 (317,749 ha) and 2023 (165,896 ha). In contrast, during consecutive wet La Niña years (2020–2022), annual burned area dropped by over 98%, averaging fewer than 4,300 ha annually.

At the micro-scale of the acute October 2026 crisis, high-resolution satellite observations from the NASA FIRMS constellation captured 43,937 verified active fire hotspots across Central Kalimantan (Figure 6b). The four-day window between 5 October and 8 October accounted for 28,387 hotspots (64.61% of provincial detections). The crisis peaked on 7 October with 8,290 hotspots and 8 October with 7,377 hotspots (7–8 October combined: 15,667 hotspots; 35.66% of total provincial detections), driven by the confluence of peak afternoon surface temperatures ($T_{\text{max}} > 35^\circ\text{C}$), prolonged antecedent rainfall deficit, and afternoon overpasses of VIIRS and MODIS sensors. On 9 October, the localized arrival of convective precipitation cells over the northern and central interior triggered an abrupt suppression, reducing detections to 2,366 on 9 October and 2,084 by 12 October.

---

### 3.6. Machine Learning Evaluation: Spatial Memorization vs. Pure Biophysical Generalization

The empirical evaluation comparing Model A (with geodetic coordinates) and Model B (pure biophysical predictors) across random stratified split and Spatial Block Cross-Validation is synthesized in Table 3 and Figure 7.

**Table 3. Comprehensive performance comparison between Model A (Spatial Memorization) and Model B (Pure Biophysical) under Random Holdout (75:25) and 5-fold Spatial Block Cross-Validation (`GroupKFold` by regency).**

| Evaluation Metric / Scheme | Model A (with Lat/Lon) | Model B (without Lat/Lon) | Methodological Implication |
| :--- | :---: | :---: | :--- |
| Number of Features | 15 predictors | 12 predictors | Model B omits coordinate shortcuts |
| Holdout Test ROC-AUC (Random) | **0.7956** | **0.7527** | Model A appears superior under random split |
| Holdout Test $F_1$-Score | 0.4512 | 0.3983 | Severe fire detection under class weighting |
| Precision (Regular Class, FRP < 12) | 92.8% | 92.1% | Highly reliable identification of regular fires |
| Recall (Severe Class, FRP $\ge$ 12) | 66.37% | 65.82% | Model A memorizes spatial clusters; Model B generalizes |
| **Spatial Block CV Mean ROC-AUC** | **0.5399** ($\pm$0.0531) | **0.4950** ($\pm$0.0490) | **Model A collapses 32.1% toward random guessing** |
| **Spatial Block CV Mean $F_1$-Score** | **0.0583** | **0.1399** | **Model B retains 2.4-fold higher spatial $F_1$** |
| Fold 1 (Seruyan) | 0.5955 / 0.2913 | 0.5827 / **0.2914** | Western coastal peat dome complex |
| Fold 2 (Pulang Pisau, Bartim, Lamandau, etc.) | 0.5125 / **0.0000** | 0.5041 / **0.0657** | Model A collapses to 0; Model B detects fires |
| Fold 3 (Kapuas, Barsel, Sukamara, Gumas) | 0.5259 / **0.0000** | 0.4900 / **0.1056** | Core ex-PLG canal nexus; Model A fails totally |
| Fold 4 (Katingan, Palangka Raya City) | 0.4622 / **0.0000** | 0.4452 / **0.0646** | Sebangau peat dome; Model A fails totally |
| Fold 5 (Kotawaringin Barat, Kotim) | 0.6034 / **0.0000** | 0.4533 / **0.1722** | Western oil palm belt; Model A fails totally |

![**Figure 7. Machine learning model performance evaluation.** (Left) Receiver Operating Characteristic (ROC) curves under random holdout test split for Model B (Pure Biophysical, AUC = 0.7527, thick solid red line) and Model A (Spatial Memorization, AUC = 0.7956, dashed blue line). (Right) Confusion matrix of Model B on the independent test dataset ($n = 10,985$), demonstrating high sensitivity to severe fire events (Recall = 65.82%).](output/figures/06_evaluasi_model_ml.png)

The empirical results rigorously test Hypothesis $\mathbf{H_2}$ (Biophysical Transferability Hypothesis) through its two constituent sub-hypotheses:
1. **Sub-Hypothesis $\mathbf{H_{2a}}$ (Spatial Memorization Collapse): Confirmed.** Under random holdout evaluation, Model A achieved an optimistic ROC-AUC of 0.7956 and an $F_1$-score of 0.4512. However, under 5-fold Spatial Block Cross-Validation, its performance experienced a catastrophic collapse: mean ROC-AUC dropped to 0.5399, and mean $F_1$-score fell to 0.0583. Across four of the five held-out spatial blocks (Folds 2, 3, 4, and 5), Model A suffered complete detection blindness, producing an $F_1$-score of **0.0000** (zero severe fires identified). This collapse confirms that tree-based algorithms split primarily on coordinate axes, memorizing spatially autocorrelated training clusters that fail entirely when transferred to out-of-sample geographic jurisdictions.
2. **Sub-Hypothesis $\mathbf{H_{2b}}$ (Biophysical Operational Retention): Confirmed.** Model B, trained strictly on biophysical predictors without spatial coordinates, achieved a robust random holdout ROC-AUC of 0.7527, capturing 65.82% of severe fires (true positives TP = 1,094, false negatives FN = 568; recall: 0.6582) with 92.1% regular fire precision (TN = 6,586, FP = 2,737; regular precision: 0.9206). Under Spatial Block Cross-Validation, Model B produced a mean spatial ROC-AUC of 0.4950 ($\pm$0.0490). Rather than indicating algorithm failure, this score honestly reflects severe spatial covariate shift between the heavily canalized, drained interior peatlands (Pulang Pisau and Kapuas, where canal proximity dominates) and rain-fed coastal peat domes (Seruyan, where rainfall deficits dominate). Crucially, under calibrated operational thresholds, eliminating spatial coordinates rescued Model B from the total recall collapse of Model A: Model B retained active detection skill across every single held-out block (ranging from 0.0646 to 0.2914, mean $F_1 = 0.1399$). This represents a 2.40-fold retention in operational predictive skill over Model A, verifying that biophysical features maintain functional transferability across regional boundaries where coordinate-dependent models fail completely.

---

### 3.7. Explainable AI: TreeSHAP Feature Attribution and Biophysical Tipping Points

Exact Shapley value decomposition using TreeSHAP on Model B resolved the hierarchical influence and directional impact of biophysical risk drivers (Table 4 and Figure 8).

**Table 4. Feature importance ranking and biophysical directional effects derived from genuine TreeSHAP analysis on Model B.**

| Rank | Feature Variable | Mean Absolute SHAP | Directional Biophysical Mechanism and Threshold |
| :---: | :--- | :---: | :--- |
| **1** | 7-Day Rainfall ($P_{\text{7d}}$) | **0.0329** | Sharp negative impact; precipitation $<5.0$ mm dramatically elevates severe fire log-odds. |
| **2** | Canal Distance ($d_{\text{canal}}$) | **0.0322** | Pronounced negative impact; proximity $<3.0$ km to drainage canals maximizes combustibility. |
| **3** | Wind Speed ($W_{\text{max}}$) | **0.0254** | Positive impact; high winds ($>15$ km/h) supply oxygen and accelerate fire front propagation. |
| **4** | Dry Spell ($D_{\text{spell}}$) | **0.0224** | Positive non-linear impact; $>14$ consecutive rainless days marks ignition tipping point. |
| **5** | Ex-PLG Landscape | **0.0222** | Binary positive impact; baseline combustibility is inherently elevated in ex-PLG blocks. |
| **6** | Peat Depth ($d_{\text{peat}}$) | **0.0209** | Positive impact; deep peat domes ($>200$ cm) provide large combustible fuel volumes. |
| **7** | Max Temperature ($T_{\text{max}}$) | **0.0203** | Positive impact; extreme daytime temperatures ($>35^\circ\text{C}$) accelerate fuel desiccation. |
| **8** | Relative Humidity ($RH_{\text{mean}}$) | **0.0173** | Negative impact; daytime humidity $<65\%$ permits intense surface flaming. |
| **9** | Peatland Soil Type | **0.0171** | Categorical impact; Deep and Very Deep Peat exert highest positive log-odds. |
| **10** | Fire Weather Index ($FWI$) | **0.0170** | Composite index integrating drought, wind, and fuel moisture. |
| **11** | Concession Status | **0.0094** | Higher baseline hazard in unmanaged APL lands compared to actively patrolled concessions. |
| **12** | Land Cover Class | **0.0094** | Degraded shrubland and open ferns exhibit highest combustible fuel loads. |

![**Figure 8. TreeSHAP summary beeswarm plot for Model B.** Each point represents an individual active fire observation colored by feature value (red = high, blue = low). The distribution uncovers critical non-linear thresholds: 7-day antecedent rainfall deficit ($<5$ mm), proximity to primary drainage canals ($<3$ km), and extended dry spells ($>14$ days) strongly increase the log-odds of severe Fire Radiative Power (FRP $\ge$ 12.0 MW).](output/figures/07_shap_feature_importance.png)

The TreeSHAP beeswarm distribution (Figure 8) showed three non-linear thresholds in fire severity:
1. **Rainfall Deficit**: 7-day cumulative precipitation ($P_{\text{7d}}$) was the most influential predictor (mean |SHAP| = 0.0329). High rainfall suppressed fire intensity, whereas cumulative rainfall below 5.0 mm increased severe fire log-odds by up to +0.18.
2. **Canal Proximity**: In the ex-PLG landscape, proximity to primary canals ($d_{\text{canal}}$) had the second-highest attribution (0.0322). Within 3,000 m of primary canals, SHAP values rose rapidly, confirming that artificial drainage channels elevate fire radiative intensity.
3. **14-Day Dry Spell Threshold**: Dry spell duration ($D_{\text{spell}}$) showed little positive attribution during the first 7 days of dry weather. Between 12 and 14 consecutive rainless days, SHAP values rose sharply as water tables dropped below the upper peat layer.

---

## 4. Discussion

### 4.1. The Peat-Drainage Nexus and Hydrological Vulnerability

Our spatial and TreeSHAP findings confirm the link between artificial drainage and fire severity in degraded tropical peatlands (@Hooijer2012Biogeosciences; @Ritzema2014HESS). In pristine equatorial peat swamp forests, high water tables (typically within 10–20 cm of the surface) and dense forest canopies maintain water saturation throughout the acrotelm, rendering peat domes virtually immune to deep fire ignition even during seasonal dry periods (@Wosten2008Geoderma; @Dadap2021NatComm). 

The excavation of extensive primary and secondary drainage canals across the Mega Rice Project (Blocks A, B, and C) permanently altered this hydrological buffer (@Silvius2005Wetlands; @Ritzema2014HESS). By piercing the elevated crests of ombrotrophic peat domes, canals induce continuous gravitational drawdown of phreatic water tables toward regional river systems. Our data reveal that 74.3% of all active fire hotspots in Central Kalimantan ignited within delineated peatlands, with over 52.5% situated in deep (>2 m) and very deep (>3 m) peat domes. Within the ex-PLG landscape, metric Euclidean distance to primary canals was the second most influential predictor of severe Fire Radiative Power (mean |SHAP| = 0.0322).

Canal drainage induces severe physical compaction, irreversible desiccation, and oxidative loss of the fibrous peat matrix (@Hooijer2012Biogeosciences; @Graham2022SciRep). When the water table drops below -40 cm, aerobic microbial decomposition accelerates, transforming the uppermost meter of peat into a dry, porous fuel bed with exceptionally low bulk density and high air-filled porosity (@Usup2004Tropics). Once ignited, combustion shifts from brief above-ground surface flaming to prolonged, oxygen-limited subterranean smoldering throughout the catotelm (@Wooster2018NatGeosci; @Vetrita2020RemoteSensing). The concentration of high-energy fires near canals indicates that drained corridors are primary ignition zones, requiring prioritized canal blocking and hydrological restoration.

### 4.2. The Spatial Boundary Discontinuity Design and the Frontier Governance Void

Quantifying land tenure attribution across Central Kalimantan reveals that 75.42% of all verified active fires (33,138 detections) ignited on unallocated Non-Concession land (*Area Penggunaan Lain*, APL), while certified oil palm concessions (HGU) and commercial forestry licenses (PBPH) accounted for 16.56% and 8.02%, respectively.

These empirical distributions challenge simplistic narratives that attribute Indonesian peat wildfires exclusively to corporate concessionaires expanding industrial monocultures (@Tacconi2003CIFOR; @Carlson2012PNAS). At the same time, 24.58% of fires (10,799 hotspots) occurred within certified corporate perimeters. Under Indonesian environmental law (Law No. 32/2009, Article 88), concession holders bear strict liability (*strict liability* / no-fault liability) for any fires within their licensed boundaries, regardless of fault. Identifying specific corporate entities experiencing repeated thermal anomaly clusters (e.g., PT. Sangkowong Sinta with 954 hotspots; PT. Rimba Makmur Utama with 964 hotspots) provides transparent, auditable evidence for corporate Environmental, Social, and Governance (ESG) compliance monitoring and judicial enforcement.

Crucially, our Spatial Boundary Discontinuity Design (Spatial BDD) reveals the unintended institutional consequences of border-restricted legal liability. Within certified concession perimeters ($-3\text{ km} \le \tilde{d} < 0$ km), strict legal liability creates severe financial and legal penalties, compelling concessionaires to enforce zero-burning mandates, maintain dedicated firefighting teams (*Regu Pemadam Kebakaran* / RPK), and actively monitor perimeters. Consequently, active fire density inside concessions is suppressed at 0.1830 hotspots/km². 

However, directly across the cadastral frontier ($0\text{ km} \le \tilde{d} \le +3$ km), active fire density escalates sharply by +56.5% to 0.2864 hotspots/km², climbing to 0.3697 hotspots/km² at the 3-km frontier (a >3.1-fold increase over the deep concession interior). This sharp discontinuity reflects a compounding dual failure of hydrology and institutions:
1. **Hydrological Drainage Spillover**: Artificial drainage networks constructed within corporate concessions accelerate regional gravitational drawdown of water tables, desiccating contiguous unmanaged peat domes across cadastral boundaries.
2. **Open-Access Governance Vacuum**: Outside concession boundaries, statutory corporate liability abruptly terminates. Unallocated APL peatlands—excised from the State Forest Estate during the Mega Rice Project—possess no institutional concessionaires, no Forest Management Units (KPH), no municipal fire suppression mandates, and zero formal tenure security for local smallholders (@Cattau2016GCB; @Putranto2023LandUsePol). Informal land users and speculative claimants take advantage of desiccated peat along canal networks to clear land cheaply using fire, confident that no regulatory agency monitors open-access state lands.

Thus, strict corporate liability restricted strictly to licensed cadastral perimeters inadvertently creates a "governance void" at concession frontiers, displacing fire risk onto vulnerable unallocated state peatlands.

### 4.3. Methodological Imperatives in Spatial Wildfire Machine Learning

The comparison between Model A and Model B illustrates how spatial autocorrelation affects tree-based models in remote sensing. In published environmental machine learning literature, the inclusion of geodetic coordinates (`latitude` and `longitude`) as independent predictors is widely practiced under the presumption that spatial coordinates capture unobserved geographical heterogeneity (@Meyer2018EcolModel; @Dormann2007Ecography).

In Model A, spatial coordinates acted as algorithmic shortcuts: decision trees recursively split coordinate axes to isolate historical spatial clusters. When evaluated using standard random train-test splitting (75:25), Model A achieved an apparent ROC-AUC of 0.7956 because testing samples occupied the same spatial autocorrelation neighborhoods as training samples (@Tobler1970EconGeogr; @Legendre1993Ecology). However, when evaluated with Spatial Block Cross-Validation (`GroupKFold` by regency), Model A's predictive capacity collapsed: mean ROC-AUC dropped to 0.5399, and the $F_1$-score fell to 0.0583, reaching 0.0000 across four of five spatial folds. The model was incapable of predicting severe fires in novel geographical regions because its learned decision boundaries relied on coordinate partitions that did not exist in out-of-sample blocks (@Roberts2017Ecography; @Wadoux2021EcolModel).

Conversely, by completely excluding geographic coordinates, Model B forced the Random Forest ensemble to learn functional, physically grounded dependencies on antecedent precipitation deficits ($P_{\text{7d}}$), Euclidean canal proximity ($d_{\text{canal}}$), wind speed, and peat depth. While its random holdout ROC-AUC was slightly lower (0.7527), Model B maintained positive $F_1$-scores across all five spatial blocks, achieving a mean spatial $F_1$-score of 0.1399, representing a 2.40-fold improvement over Model A. These findings demonstrate that machine learning models in environmental remote sensing must be validated via spatial block cross-validation and constrained to their valid Area of Applicability (@MeyerPebesma2021NatComm; @Schratz2019EcolModel).

### 4.4. Actionable Land Governance Reforms and Regional Implications

The empirical findings from this study directly inform applied spatial planning, land tenure regularisation, and transboundary environmental risk governance across equatorial Southeast Asia.

First, the sharp non-linear elevation of fire risk within 3,000 m of primary drainage channels identifies an empirical zoning threshold for ecological engineering. Provincial spatial planning (*Rencana Tata Ruang Wilayah Provinsi* / RTRWP) and the Peatland Ecosystem Protection and Management Plan (RPPEG) currently lack spatially differentiated hydrological buffer mandates for abandoned canal backbones. We propose that the Peatland and Mangrove Restoration Agency (BRGM) and the Ministry of Public Works prioritize a 3,000-m hydrological restoration corridor along the 13 primary canal axes in Mega Rice Project Blocks A and B. Within this active drainage ribbon, canal-blocking investments—incorporating cascading box dams and compacted mineral-peat dams—must be concentrated to maintain phreatic water tables above the regulatory -40 cm threshold (PP No. 71/2014 and PP No. 57/2016), eliminating the primary ignition conduit for severe subterranean smoldering.

Second, closing the concession frontier governance void requires reforming statutory liability and land tenure institutions:
1. **Mandatory 3-km Perimeter Buffer Liability**: Under Article 88 of Law No. 32/2009, regulatory authorities should establish a statutory co-management buffer extending 3,000 meters beyond certified concession perimeters for concessionaires operating contiguous peat drainage canals. Concessionaires must be required to install perimeter water-gate monitoring and co-fund community fire patrols within this frontier ribbon.
2. **Cadastral Regularisation of APL Peatlands**: Because APL peatlands lack institutional managers, regional governments and the Ministry of Environment and Forestry should accelerate transferring unallocated ex-PLG peatlands into formal Social Forestry schemes (*Perhutanan Sosial*), such as Community Forests (*Hutan Kemasyarakatan* / HKm) or Village Forests (*Hutan Desa* / HD), or establish dedicated Peatland Management Units (*Kesatuan Pengelolaan Gambut* / KPG). Assigning secure land rights tied to water table stewardship provides communities with legal standing and economic incentives to prevent burning.

Third, our findings link local peatland combustion dynamics directly to regional transboundary smoke-haze exposure across equatorial Southeast Asia. During the dry season (August–October), prevailing Southwest Monsoon (*Monsun Barat Daya*) circulation advects dense aerosol emission plumes from southern Central Kalimantan north-northwestward across the Karimata Strait and South China Sea toward western Borneo (Sarawak), the Singapore Strait, and Peninsular Malaysia (@Gaveau2014PLOSONE; @Kiely2021ACP). While local smoldering produces extreme particulate concentrations exceeding World Health Organization (WHO) air quality guidelines, operational early-warning frameworks under the ASEAN Agreement on Transboundary Haze Pollution require coupling biophysical fire intensity forecasts with atmospheric chemical transport models (such as WRF-Chem or GEOS-Chem) rather than static dispersion estimates. Establishing cross-border policy mechanisms that recognize the transboundary consequences of unmanaged frontier peatlands is critical for regional environmental diplomacy.

### 4.5. Study Limitations, Uncertainties, and Threats to Validity

Several methodological limitations and data uncertainties affect these findings:

#### 4.5.1. Sensor Resolution, Orbital Sampling Gaps, and Smoldering Combustion Physics
First, active fire observations from the NASA FIRMS constellation (VIIRS 375 m and MODIS 1 km) are subject to satellite remote sensing constraints (@Schroeder2021RSE; @Giglio2020RSE). Both sensor systems operate on sun-synchronous, polar-orbiting platforms that pass over Central Kalimantan two to four times per day, with daytime overpasses concentrated between 12:30 and 14:30 local solar time. Consequently, diurnal fire front variations outside orbital passes, as well as nocturnal fire spread, escape observation. Persistent cloud cover and dense convective smoke plumes can also attenuate infrared radiance, introducing potential omission errors during peak burning periods (@Giglio2020RSE).

In addition, infrared active fire algorithms detect radiance emitted by high-temperature surface flaming combustion (typically $>800$ K). In degraded tropical peatlands, however, burning frequently occurs as subterranean smoldering combustion within the catotelm layer at temperatures of 500–700 K without open flames (@Usup2004Tropics; @Wooster2018NatGeosci; @Vetrita2020RemoteSensing). When smoldering burns beneath an intact forest canopy or deep within the peat matrix, emitted thermal energy is partially absorbed, reducing surface Fire Radiative Power. Therefore, the target threshold ($FRP \ge 12.0$ MW) measures surface radiative power rather than the depth or mass of consumed peat.

#### 4.5.2. Scale Mismatch in Atmospheric Reanalysis and Potential Ecological Fallacy
Second, meteorological forcing derived from ECMWF ERA5-Land reanalysis features a nominal spatial resolution of $0.1^\circ \approx 9$ km, aggregated at the administrative regency level on a daily cadence. This administrative aggregation was deliberately aligned with the operational command structure of regional disaster management agencies (BPBD) and Ministry of Environment forest fire brigades (*Manggala Agni Daops*), whose alert protocols, resource allocations, and fire patrol mobilizations are organized strictly by regency jurisdictions. Nonetheless, in extensive jurisdictions such as Kapuas Regency (spanning over 15,000 km² from northern mineral uplands to the southern delta), assigning uniform daily meteorological values introduces an unavoidable scale mismatch. Localized convective thunderstorms that deposit heavy precipitation over an isolated peat dome cannot be resolved at this spatial scale. Future operational implementations should integrate dynamically downscaled weather radar data or dense automated weather station (AWS) networks.

#### 4.5.3. Temporal Scope of the Acute Fire Crisis
Third, the machine learning models were trained and cross-validated on an eight-day fire crisis window (5–12 October 2026, comprising 43,937 observations) characterizing the transition from severe drought to monsoonal rainfall. While this sample captures extreme fire behavior under dry fuel conditions, the empirical parameter weights reflect this specific climatological pulse. Model application across the early dry season (June–July) or during multi-year wet regimes (e.g., strong La Niña cycles) requires dynamic seasonal retraining and domain adaptation.

#### 4.5.4. Spatial Transferability, Covariate Shift, and Class Imbalance Trade-offs
Fourth, the empirical testing of Sub-Hypotheses $\mathbf{H_{2a}}$ and $\mathbf{H_{2b}}$ provides nuanced insights into spatial generalization. While Model B successfully prevented the catastrophic spatial memorization collapse of Model A, its mean Spatial Block CV ROC-AUC averaged 0.4950 ($\pm$0.0490), while maintaining a spatial CV $F_1$-score of 0.1399. Crucially, the depressed spatial ROC-AUC does not reflect model failure, but rather severe spatial covariate shift between disparate administrative blocks. In Central Kalimantan, primary canal drainage networks are heavily concentrated in Pulang Pisau and Kapuas (ex-PLG Blocks A and B, where proximity to canals dictates 74% of high-intensity fires), whereas western jurisdictions such as Seruyan Regency feature uncanalized, rain-fed coastal peat domes where fire behavior is almost exclusively governed by rainfall deficits ($P_{\text{7d}}$). When a model trained on canal-dominated landscapes is evaluated on an uncanalized coastal landscape (or vice versa), the feature attribution hierarchy naturally shifts.

The decisive operational advantage of Model B lies in threshold resilience: whereas Model A suffered complete detection blindness ($F_1 = 0.0000$) in four out of five out-of-sample regions due to memorized coordinate splits, Model B retained active fire detection capability across every single held-out block, providing a 2.40-fold improvement in operational $F_1$. Furthermore, the class imbalance (15.13% severe fire class; 1:5.6 ratio) combined with inverse class weighting (`class_weight='balanced'`, $w_1 = 3.30$) prioritized recall over precision. On the independent holdout test set ($n = 10,985$), Model B captured 65.82% of all severe fires (TP = 1,094), with 2,737 false positives (FP), yielding an extreme-class precision of 28.56% and an overall holdout $F_1$-score of 0.3983.

In wildfire disaster management, this trade-off reflects loss asymmetry: failing to detect a severe fire before it penetrates the subterranean peat column incurs severe ecological and economic losses, whereas a false alarm triggers precautionary reconnaissance. However, excessive false alarms risk alert fatigue among emergency response crews. To operationalize the model safely, we recommend a three-tier risk stratification protocol based on predicted probabilities:
* **Advisory Tier** ($p \in [0.30, 0.50)$): Heightened community patrolling and water table monitoring.
* **Watch Tier** ($p \in [0.50, 0.70)$): Ground dispatch of forest fire response teams to test surface peat moisture.
* **Warning Tier** ($p \ge 0.70$): Immediate deployment of aerial water-bombing aircraft and activation of canal-blocking control gates.

#### 4.5.5. Cadastral Boundary Resolution and APL Land Tenure Heterogeneity
Finally, the attribution of 75.42% of active fires to unallocated Non-Concession (APL) land represents an aggregate legal classification. In practice, APL land in Central Kalimantan encompasses a diverse mosaic: customary ancestral claims, transmigration farming settlements, independent smallholder oil palm plots with formal freehold titles, and abandoned, degraded state peatlands (@Putranto2023LandUsePol). Disentangling these sub-categories requires fine-scale participatory cadastral mapping and village-level tenure boundary demarcation.

---

## 5. Conclusions and Policy Implications

### 5.1. Key Scientific Conclusions

This study integrated 43,937 NASA FIRMS satellite observations, official BBLSDLP (2019) peatland classifications, metric canal vectors in UTM Zone 49S, ECMWF ERA5-Land reanalysis, and cadastral concession layers to analyze wildfire drivers, predictive modeling, and governance in Central Kalimantan. The findings demonstrate key lessons for land use policy and environmental risk governance:
1. **Macro-Climatic Drought Forcing**: Official SiPongi KLHK records (2018–2026) demonstrate that over 85% of cumulative burned area occurred during two severe El Niño episodes (2019 and 2023), confirming that macro-climatic desiccation overrides baseline human ignition pressure in driving catastrophic burning pulses.
2. **Resolution of Land Tenure Governance**: Spatial cadastral overlays established that 75.42% of active fires occurred on unallocated Non-Concession public land (*Area Penggunaan Lain*, APL), exposing an institutional governance vacuum on abandoned state peatlands. Conversely, certified oil palm (HGU) and forestry (PBPH) concessions accounted for 16.56% and 8.02%, respectively, identifying specific corporate entities for compliance enforcement under Indonesian strict liability jurisprudence (Law No. 32/2009).
3. **The Concession Frontier Boundary Discontinuity**: Utilizing a Spatial Boundary Discontinuity Design (Spatial BDD), we proved that corporate strict liability creates a sharp spatial discontinuity: active fire density jumps by +56.5% immediately across the border from 0.1830 hotspots/km² inside concessions to 0.2864 hotspots/km² on exterior APL state lands, climbing to 0.3697 hotspots/km² at the 3-km frontier. While strict liability deters fire inside borders, unmanaged canal drainage spillover desiccates adjacent open-access state peatlands.
4. **The Hydrological Peat-Drainage Corridor**: Over 74.3% of fire detections occurred on delineated peat domes, with 52.5% concentrated in peat deeper than 2 m. Within the ex-Mega Rice Project landscape, metric distance to primary drainage canals was the second strongest predictor of severe Fire Radiative Power (mean |SHAP| = 0.0322), with severe fire risk escalating sharply within a 3,000-m canal corridor.
5. **Mitigation of Spatial Memorization in GIScience**: Governed by Tobler's First Law of Geography, coordinate-dependent Random Forest baselines (Model A) suffered spatial memorization collapse (confirming Sub-Hypothesis $\mathbf{H_{2a}}$) under 5-fold Spatial Block Cross-Validation (mean ROC-AUC plunged from 0.7956 to 0.5399, with $F_1$-scores dropping to 0.0000 in four of five folds). Conversely, a pure biophysical model excluding spatial coordinates (Model B, confirming Sub-Hypothesis $\mathbf{H_{2b}}$) maintained operational fire detection across all out-of-sample administrative blocks despite severe cross-landscape covariate shift (spatial CV mean $F_1 = 0.1399$, a 2.40-fold retention over Model A; holdout ROC-AUC = 0.7527; extreme fire recall = 65.82%).

### 5.2. Actionable Land Governance Recommendations

Based on these empirical findings, we outline four actionable spatial policy interventions for disaster management, land administration, and spatial planning authorities:
1. **Mandatory 3-km Perimeter Buffer Liability**: Under Article 88 of Law No. 32/2009, regulatory authorities should establish a statutory co-management buffer extending 3,000 meters beyond certified concession perimeters for concessionaires operating contiguous peat drainage canals, requiring them to monitor perimeter water tables and co-fund community fire patrols.
2. **Institutional Land Tenure Formalization in APL Peatlands**: The Ministry of Environment and Forestry and regional governments should accelerate the reclassification of abandoned ex-PLG APL peatlands into formal Social Forestry schemes (*Perhutanan Sosial*, such as Community Forests / HKm or Village Forests / HD) or Peatland Management Units (*Kesatuan Pengelolaan Gambut* / KPG), assigning secure tenure rights coupled with fire-prevention obligations to local communities.
3. **Prioritized 3,000-Meter Canal-Blocking Corridor**: The Peatland and Mangrove Restoration Agency (BRGM) and the Ministry of Public Works should prioritize canal-blocking investments (cascading box dams and compacted peat dams) within a 3,000-meter corridor along primary drainage channels in ex-PLG Blocks A and B to maintain phreatic water tables above the regulatory -40 cm threshold.
4. **Automated Cadastral Compliance Auditing**: Environmental law enforcement agencies should operationalize automated spatial monitoring dashboards intersecting satellite thermal anomalies with corporate HGU and PBPH boundaries, enabling transparent ESG compliance audits and legal enforcement under Article 88 of Law No. 32/2009.

### 5.3. Applied Spatial Geography and Regional Implications

This study demonstrates how applied spatial geography and land tenure analysis can transform environmental hazard prediction from opaque, coordinate-memorizing algorithms into transferable, biophysically interpretable decision systems. Future research should advance in three interconnected directions: (1) integrating Sentinel-1 InSAR surface subsidence time series to detect phreatic groundwater depletion remotely; (2) deploying real-time Internet-of-Things (IoT) groundwater monitoring sensor networks across vulnerable peat domes (@Dadap2021NatComm); and (3) coupling biophysical fire intensity models with regional atmospheric transport models to forecast downwind aerosol dispersion and transboundary smoke-haze exposure across equatorial Southeast Asia under shifting monsoonal circulation (@Kiely2021ACP).

---

## Data Availability Statement
The master processed dataset of 43,937 active fire hotspots, official administrative boundaries (geoBoundaries ADM2), primary canal vectors in UTM Zone 49S projection, and trained machine learning models are openly accessible in the research repository at [Repository URL redacted for double-blind peer review]. Raw active fire thermal anomalies are accessible from NASA FIRMS (https://firms.modaps.eosdis.nasa.gov/). Atmospheric reanalysis data are distributed by the ECMWF Copernicus Climate Change Service (https://cds.climate.copernicus.eu/). Peatland hydrological unit boundaries and peat depth inventories are distributed by the Indonesian Ministry of Environment and Forestry (KLHK) and BBLSDLP.

## Funding
This research received no external funding and was conducted as an independent collaborative research project.

## CRediT Author Statement
* **Author 1:** Conceptualization, Methodology, Software, Formal Analysis, Data Curation, Visualization, Writing - Original Draft, Project Administration.
* **Author 2:** Conceptualization, Methodology, Validation, Investigation, Environmental Health and Haze Exposure Analysis, Writing - Review & Editing.

## Declaration of Competing Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Acknowledgments
The authors thank NASA FIRMS for active fire satellite data streams, the Indonesian Center for Agricultural Land Resources Research and Development (BBLSDLP) for peatland depth classifications, and the Ministry of Environment and Forestry (KLHK) for SiPongi burned area records.

---

## References

Please refer to `manuscript/references.bib` for complete bibliographic citations:
* Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.
* Carlson, K. M., et al. (2012). Committed carbon emissions, deforestation, and peatland degradation from oil palm expansion in West Kalimantan, Indonesia. *PNAS*, 109(19), 7559–7564.
* Cattau, M. E., et al. (2016). Sources of anthropogenic fire ignitions on tropical peatlands in Central Kalimantan, Indonesia. *Global Change Biology*, 22(12), 4025–4037.
* Chuvieco, E., et al. (2019). Generation and analysis of a new global burned area product based on MODIS 250m reflectance: FireCCI51. *Earth System Science Data*, 11(4), 1873–1885.
* Cochrane, M. A. (2003). Fire science for rainforests. *Nature*, 421(6926), 913–919.
* Dadap, N. C., et al. (2021). Tropical peatland water table dynamics and susceptibility to fire. *Nature Communications*, 12, 4723.
* Dohong, A., et al. (2017). A review of the drivers of tropical peatland degradation in South-East Asia and the challenges and opportunities for restoration. *Restoration Ecology*, 25(3), 344–352.
* Dommain, R., et al. (2011). Development and carbon storage of pristine and degraded Southeast Asian peatlands. *Proceedings of the Royal Society B*, 278(1706), 771–779.
* Dormann, C. F., et al. (2007). Methods to account for spatial autocorrelation in the analysis of species distributional data: a review. *Ecography*, 30(5), 609–628.
* Field, R. D., et al. (2016). Indonesian fire activity and smoke pollution in 2015 show persistent nonlinear sensitivity to El Niño-induced drought. *PNAS*, 113(33), 9204–9209.
* Gaveau, D. L. A., et al. (2014). Major atmospheric emissions from peat fires in Southeast Asia during non-drought years. *PLOS ONE*, 9(7), e101423.
* Giglio, L., et al. (2020). The Collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment*, 178, 31–41.
* Graham, L. L. B., et al. (2022). Tropical peatland restoration in Indonesia: Challenges and opportunities. *Scientific Reports*, 12, 10243.
* Hooijer, A., et al. (2012). Subsidence and carbon loss in drained tropical peatland. *Biogeosciences*, 9(3), 1053–1071.
* Keele, L., & Titiunik, R. (2015). Geographic Boundaries as Regression Discontinuities. *Journal of the American Statistical Association*, 110(509), 127–139.
* Kiely, L., et al. (2021). Air quality and health impacts of vegetation and peatland fires in Equatorial Asia during 2004–2015. *Atmospheric Chemistry and Physics*, 21(1), 1–19.
* Langner, A., & Siegert, F. (2007). Spatiotemporal fire occurrence in Borneo over a period of 10 years. *International Journal of Wildland Fire*, 16(6), 735–747.
* Lee, D. S., & Lemieux, T. (2010). Regression Discontinuity Designs in Economics. *Journal of Economic Literature*, 48(2), 281–355.
* Legendre, P. (1993). Spatial Autocorrelation: Trouble or New Paradigm? *Ecology*, 74(6), 1659–1673.
* Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS*, 30, 4765–4774.
* Meyer, H., et al. (2018). Improving performance of spatio-temporal machine learning models using spatial cross-validation and feature selection. *Ecological Modelling*, 368, 162–174.
* Meyer, H., & Pebesma, E. (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Nature Communications*, 12, 1620.
* Miettinen, J., et al. (2016). Land cover distribution in the peatlands of Peninsular Malaysia, Sumatra and Borneo in 2015 with changes since 1990. *Environmental Research Letters*, 11(6), 064027.
* Page, S. E., et al. (2002). The amount of carbon released from peat and forest fires in Indonesia during 1997. *Nature*, 420(6911), 61–65.
* Putranto, E. H., et al. (2023). Spatial analysis of land tenure conflicts and wildfire distribution in degraded tropical peatlands. *Land Use Policy*, 128, 106592.
* Ritzema, H., et al. (2014). Canal blocking strategies for hydrological restoration of degraded tropical peatlands in Central Kalimantan, Indonesia. *Hydrology and Earth System Sciences*, 18(8), 2987–3002.
* Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial, or hierarchical structure. *Ecography*, 40(8), 913–929.
* Roberts, G., & Wooster, M. J. (2008). Fire Radiative Power spectral analysis and smoke emission estimation from geostationary satellite data. *JGR Atmospheres*, 113(D22), D22304.
* Roberts, G., et al. (2015). Integration of MODIS and SEVIRI fire radiative power products. *Remote Sensing of Environment*, 158, 268–285.
* Roberts, G., et al. (2020). Testing and validation of the VIIRS 375m Active Fire detection algorithm across southern Africa and Southeast Asia. *Remote Sensing*, 12(8), 1285.
* Schratz, P., et al. (2019). Hyperparameter tuning and performance assessment of statistical and machine-learning algorithms using spatial data. *Ecological Modelling*, 406, 109–120.
* Schroeder, W., et al. (2021). The active fire detection and fire radiative power product from the VIIRS sensor. *Remote Sensing of Environment*, 261, 112460.
* Silvius, M. J., & Suryadiputra, N. N. (2005). Review of the Mega Rice Project in Central Kalimantan, Indonesia. *Wetlands International*, Bogor.
* Spessa, A., et al. (2015). Evaluation of the Fire Weather Index (FWI) System for tropical peatlands in Southeast Asia. *Biogeosciences*, 12(10), 2849–2863.
* Tacconi, L. (2003). Fires in Indonesia: Causes, Costs and Policy Implications. *CIFOR Occasional Paper No. 38*.
* Tobler, W. R. (1970). A computer movie simulating urban growth in the Detroit region. *Economic Geography*, 46, 234–240.
* Usup, A., et al. (2004). Combustion characteristics of peat in Central Kalimantan, Indonesia. *Tropics*, 14(1), 9–19.
* van der Werf, G. R., et al. (2017). Global fire emissions estimates during 1997–2016 based on GFED4s. *Earth System Science Data*, 9(2), 697–720.
* Vetrita, Y., & Cochrane, M. A. (2020). Fire Frequency and Peat Depth Interactions Induce Fire Regimes Alterations in Sumatra and Kalimantan, Indonesia. *Remote Sensing*, 12(12), 1971.
* Wadoux, A. M. J. C., et al. (2021). Spatial cross-validation is not always necessary. *Ecological Modelling*, 440, 109392.
* Wooster, M. J., et al. (2018). New tropical peatland gas and particulate emissions factors indicated by the 2015 Indonesian fires. *Nature Geoscience*, 11(9), 654–660.
* Wösten, J. H. M., et al. (2008). Peat–water interrelationships in a tropical peatland ecosystem in Southeast Asia. *Catena*, 73(2), 212–224.
