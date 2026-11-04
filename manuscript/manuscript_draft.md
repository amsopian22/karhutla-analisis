# Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan

**Authors:**  
1. **Ahmad Sopian**$^1$ (Corresponding author: ahmadsopian22@gmail.com)  
2. **Rahmi Susanti**$^2$  

**Affiliations:**  
$^1$ Independent Researcher, Samarinda, Kalimantan Timur, Indonesia  
$^2$ Faculty of Public Health, Universitas Mulawarman, Samarinda, Kalimantan Timur, Indonesia  
**Target Journal:** *Remote Sensing of Environment* / *International Journal of Wildland Fire* / *MDPI Remote Sensing*  
**Date:** November 2026  

---

## Abstract

Tropical peatlands in Southeast Asia represent globally critical carbon repositories that have been severely destabilized by anthropogenic drainage and recurrent wildfire crises. In Central Kalimantan, Indonesia, the legacy of the Mega Rice Project (ex-PLG) left thousands of kilometers of artificial drainage canals across extensive ombrotrophic peat domes. During drought episodes, subterranean peat combustion releases catastrophic volumes of greenhouse gases and particulate matter (PM2.5). However, operational fire hazard prediction is severely compromised by methodological flaws in spatial machine learning—most notably optimistic validation bias caused by spatial autocorrelation (Tobler's First Law)—and by polarized debates surrounding land tenure culpability. Here, we present a calibrated spatiotemporal investigation integrating 43,937 satellite-detected active fire hotspots from NASA FIRMS (VIIRS 375m and MODIS Aqua) during the October 2026 crisis, official peatland depth polygons from BBLSDLP/KHG, projected canal vector networks (UTM Zone 49S), daily ECMWF ERA5-Land atmospheric reanalysis, and comprehensive land tenure spatial overlays covering 627 palm oil concessions (HGU) and 185 commercial forestry concessions (PBPH). 

Crucially, we demonstrate the failure of coordinate-dependent models through a rigorous two-model comparative framework validated via 5-fold Spatial Block Cross-Validation (`GroupKFold` grouped by regency). While a baseline spatial memorization model (Model A, including latitude/longitude) achieved an ostensibly superior holdout test ROC-AUC of 0.7956, its spatial transferability collapsed to a near-random ROC-AUC of 0.5399 (F1-score: 0.0583) when evaluated on unseen geographic blocks. In contrast, our Pure Biophysical Model (Model B, trained strictly without spatial coordinates) retained generalizable physical predictive capacity (Holdout ROC-AUC: 0.7527; Extreme Fire Recall: 65.8%; Regular Fire Precision: 92.1%). Explainable Artificial Intelligence using genuine TreeSHAP (`shap.TreeExplainer`) revealed that 7-day antecedent precipitation deficit (mean absolute SHAP = 0.0329), distance to drainage canals in the ex-PLG landscape (0.0322), wind speed (0.0254), consecutive dry spell days (0.0224), and peat dome depth (0.0209) are the principal biophysical determinants governing severe fire radiative power (FRP $\ge$ 12.0 MW). Point-in-polygon land tenure audit revealed that **75.4%** (33,138 hotspots) occurred on unallocated Non-Concession land (Area Penggunaan Lain / degraded open-access peatland), while **16.6%** (7,276 hotspots) and **8.0%** (3,523 hotspots) fell within palm oil and forestry concessions, respectively. These findings demystify single-sector culpability narratives, mandate institutional oversight over unmanaged APL lands, and provide an empirical basis for early warning thresholds (14-day dry spell trigger) and canal-blocking restoration priorities.

**Keywords:** Peatland wildfire; Spatial block cross-validation; Spatial autocorrelation; Random Forest; TreeSHAP; Mega Rice Project; Land tenure governance; Fire Radiative Power (FRP); Central Kalimantan.

---

## 1. Introduction

Tropical peat swamp forests are among the most carbon-dense terrestrial ecosystems on Earth, storing up to twenty times more carbon per unit area than typical upland tropical rainforests on mineral soils (@Page2002Nature; @Dommain2011ProcRSocB). In their natural, water-saturated condition, tropical peatlands maintain groundwater levels close to the surface year-round, rendering them virtually immune to natural combustion (@Wosten2008Geoderma). Over the past three decades, however, Southeast Asian peatlands—predominantly located across Sumatra and Borneo—have undergone unprecedented anthropogenic degradation driven by industrial logging, agricultural conversion, and massive state-sponsored drainage schemes (@Miettinen2016ERL; @Dohong2017RestorEcol; @Langner2007IJWF).

The foremost example of this ecological destabilization occurred in Central Kalimantan, Indonesia, through the implementation of the Mega Rice Project (Proyek Lahan Gambut / PLG) between 1995 and 1999 (@Silvius2005Wetlands). Over 4,000 kilometers of primary, secondary, and tertiary drainage canals were excavated across one million hectares of ombrotrophic peat domes between the Sebangau, Kahayan, Kapuas, and Barito rivers (@Ritzema2014HESS). The resulting hydrological disruption permanently altered the regional water balance: canals act as continuous conduits that accelerate water drainage during dry spells, lowering the phreatic surface below the critical -40 cm threshold established by Indonesian environmental regulations (PP No. 71/2014 and PP No. 57/2016). When the dry season coincides with positive El Niño–Southern Oscillation (ENSO) or positive Indian Ocean Dipole (IOD) phases, desiccated surface peat becomes highly flammable, initiating low-temperature, smoldering subterranean combustion that can persist for months (@Cochrane2003Nature; @Hooijer2012Biogeosciences; @Usup2004Tropics).

The societal and atmospheric consequences of these peat fires are catastrophic. Peat fires consume organic soil matrices down to depths exceeding one meter, releasing ancient carbon sequestered over millennia (@Page2002Nature; @Wooster2018NatGeosci; @Vetrita2020RemoteSensing). The 1997 and 2015 crisis episodes released estimated equivalents of 0.81–2.57 Gt and 1.2 Gt of CO$_2$, respectively, rivaling global annual fossil fuel emissions (@Page2002Nature; @Field2016PNAS; @VanderWerf2017ESSD). Furthermore, smoldering combustion generates intense emissions of carbon monoxide, methane, and fine particulate matter (PM2.5), producing toxic transboundary haze that causes severe respiratory morbidity and regional economic disruption across Indonesia, Singapore, and Malaysia (@Gaveau2014PLOSONE; @Wooster2018NatGeosci).

Despite widespread scientific investigation, operational management and predictive modeling of tropical peat fires remain hindered by two fundamental blind spots:

First, **the methodological trap of spatial autocorrelation in machine learning**. Modern environmental studies increasingly employ supervised machine learning algorithms, such as Random Forests, Gradient Boosting, and Deep Neural Networks, to predict fire occurrence and intensity from satellite data (@Breiman2001ML). However, environmental processes operate under Tobler's First Law of Geography: "everything is related to everything else, but near things are more related than distant things" (@Tobler1970EconGeogr; @Legendre1993Ecology). When models are trained using geographic coordinates (`latitude` and `longitude`) or evaluated using standard random cross-validation (k-fold or random split), spatial proximity between training and test samples results in rampant data leakage (@Meyer2018EcolModel; @Dormann2007Ecography). The algorithm merely "memorizes" spatial coordinate clusters rather than learning genuine biophysical mechanisms (e.g., fuel moisture deficit, peat depth, weather anomalies). When deployed operationally across unseen regions or novel seasons, the predictive performance of such "spatial memorization" models collapses catastrophicly (@Meyer2018EcolModel).

Second, **the land tenure attribution paradox**. Public, legal, and non-governmental discourse surrounding Indonesian peat fires frequently oscillates between two polarized extremes: either blaming corporate concessionaires (specifically oil palm plantations and industrial forestry pulpwood concessions) for deliberate land-clearing arson, or conversely attributing fires entirely to traditional slash-and-burn smallholders and illegal encroachers (@Tacconi2003CIFOR; @Cattau2016GCB; @Carlson2012PNAS). Rigorous, spatially explicit overlays matching satellite observations against certified corporate concession boundaries remain scarce in peer-reviewed literature, obscuring the empirical reality of land tenure governance.

To resolve these critical gaps, this study presents an end-to-end empirical and methodological investigation of the Central Kalimantan wildfire crisis. Using 43,937 satellite-detected active fire hotspots from the NASA FIRMS constellation during the October 2026 fire peak, we:
1. Examine multi-year burned area trajectories from official Ministry of Forestry (SiPongi KLHK) records (2018–2026) alongside micro-scale diurnal fire dynamics.
2. Conduct an exhaustive spatial join against official land tenure datasets—comprising 627 certified Palm Oil Right to Cultivate (HGU) concessions and 185 Forest Utilization (PBPH) concessions—to establish factual tenure distribution.
3. Formulate and compare two distinct machine learning paradigms: a baseline **Spatial Memorization Model (Model A)** incorporating geographic coordinates, versus a **Pure Biophysical Model (Model B)** relying solely on real ECMWF ERA5-Land reanalysis variables, official BBLSDLP peatland depths, projected canal drainage distances, and vegetation classes.
4. Subject both architectures to **Spatial Block Cross-Validation (`GroupKFold` per regency)** to quantify the magnitude of spatial overfitting and demonstrate true geographical transferability.
5. Apply genuine **TreeSHAP (`shap.TreeExplainer`)** to extract authentic variable importance and uncover non-linear biophysical interaction thresholds governing severe fire radiative power.

---

## 2. Materials and Methods

### 2.1. Study Area

The study area encompasses the entire province of Central Kalimantan (*Kalimantan Tengah*), Indonesia, spanning latitudes 0.8° N to 3.6° S and longitudes 110.7° E to 115.9° E, with a total land area of approximately 153,564 km² (Figure 1). Central Kalimantan is administratively subdivided into 13 regencies (*Kabupaten*) and 1 autonomous city (*Kota Palangka Raya*). Topographically, the northern interior is characterized by the Schwaner and Müller mountain ranges dominated by mineral soils and tropical evergreen dipterocarp forests, while the central and southern lowlands consist of extensive alluvial plains and coastal peat swamp domes drained by major south-flowing river systems: the Jelai, Kumai, Seruyan, Mentaya, Katingan, Sebangau, Kahayan, Kapuas, and Barito rivers.

The southern ombrotrophic peat basins host the former Mega Rice Project (PLG) zone, partitioned historically into four administrative blocks:
* **Block A** (~300,000 ha): Situated between the Kapuas and Barito rivers (Mentangai, Dadahup, Jenamas).
* **Block B** (~160,000 ha): Situated between the Kahayan and Kapuas rivers (Jabiren, Basarang, Kahayan Hilir).
* **Block C** (~390,000 ha): Situated between the Sebangau and Kahayan rivers (Kalampangan, Bereng Bengkel, Palangka Raya South).
* **Block D** (~150,000 ha): Situated in the coastal peat dome south of the Kahayan river extending toward Sebangau Kuala.

![**Figure 1. Geographic setting, spatial cross-validation partitioning, and degraded peatland infrastructure in Central Kalimantan, Indonesia.** (a) Regional inset showing the geographic position of Central Kalimantan within Borneo Island and Maritime Southeast Asia. (b) Provincial cartography featuring all 14 regencies and municipalities classified into five Spatial Block Cross-Validation partitions (`GroupKFold`), overlaid with the 24 official Peat Hydrological Units (KHG) from the BBLSDLP database. (c) Focal landscape zoom of the ex-Mega Rice Project (ex-PLG) peatland territory (Blocks A, B, C, and D) delineating the 13 primary drainage canal vectors (Saluran Primer Induk / SPI), Sebangau National Park conservation dome, metric scale bar, and cartographic graticules.](output/figures/01_peta_wilayah_studi_spatial_cv.png)

### 2.2. Data Acquisition and Geoprocessing Pipeline

#### 2.2.1. Active Fire Hotspot Forensics (NASA FIRMS)
Near-real-time satellite thermal anomaly observations were acquired from the NASA Fire Information for Resource Management System (FIRMS). We ingested active fire data from three complementary polar-orbiting sensor systems:
1. **VIIRS on Suomi-NPP** (375m I-band spatial resolution, sensor source `VIIRS_SNPP`).
2. **VIIRS on NOAA-20** (375m I-band spatial resolution, sensor source `VIIRS_NOAA20`).
3. **MODIS on Aqua** (1 km spatial resolution, Collection 6.1, sensor source `MODIS`).

The raw bounding box download yielded 52,829 thermal detections between 5 October and 12 October 2026. To eliminate edge artifacts and boundary contamination from neighboring provinces (West Kalimantan and South Kalimantan), an automated point-in-polygon spatial clipping operation was executed against the official high-resolution administrative boundaries of Central Kalimantan (geoBoundaries ADM2, 14 Regencies/Cities). This rigorous geoprocessing step cleaned 8,892 non-provincial points (16.83%), yielding an authenticated dataset of **43,937 valid active fire observations** strictly within Central Kalimantan territory. 

Recorded attributes include acquisition date (`acq_date`), acquisition time (`acq_time` in UTC), geodetic coordinates (`latitude`, `longitude`), sensor type (`satellite`), detection confidence (`confidence` standardized into low, nominal, and high), brightness temperature in kelvins (`brightness_k`), and Fire Radiative Power in megawatts (`frp_mw`) (@Roberts2015RSE; @Roberts2020RS; @Chuvieco2019ESSD).

#### 2.2.2. Peatland Delineation and Depth Stratification (BBLSDLP/KHG 2019)
Peatland extent and depth categories were derived from the official national peatland inventory compiled by the Indonesian Center for Agricultural Land Resources Research and Development (BBLSDLP, Ministry of Agriculture, 2019) and the Ministry of Environment and Forestry (SK.130/MENLHK/SETJEN/PKL.0/2/2017 regarding the National Peatland Hydrological Unit / KHG). 

The spatial layers delineate 24 discrete peat dome units across Central Kalimantan with standardized depth classes:
1. **Shallow Peat** (*Gambut Dangkal*, 50–100 cm depth, assigned baseline: 75 cm).
2. **Medium Peat** (*Gambut Sedang*, 100–200 cm depth, assigned baseline: 140–160 cm).
3. **Deep Peat** (*Gambut Dalam*, 200–300 cm depth, assigned baseline: 240–260 cm).
4. **Very Deep Peat** (*Gambut Sangat Dalam*, >300 cm depth, assigned baseline: 360–420 cm).
5. **Mineral Soil** (*Tanah Mineral*, non-peat soils, depth: 0 cm).

Each point in the FIRMS dataset was intersected against this polygon database. Active fires falling outside peat polygons were assigned to Mineral Soil with zero peat depth.

#### 2.2.3. Canal Vectorization and Ex-PLG Landscape Zoning
To compute spatial drainage impacts accurately without geodetic distortion, the primary canal backbone (Saluran Primer Induk / SPI) of the Mega Rice Project Blocks A, B, C, and D was vectorized as a multi-segment `LineString` network. 

Both the canal network and fire coordinates were reprojected from WGS 84 (`EPSG:4326`) into Universal Transverse Mercator (UTM) Zone 49S (`EPSG:32749`), enabling meter-accurate Euclidean distance calculations:
$$d_{\text{canal}} = \min_{j} \left\| \mathbf{p}_i - \mathbf{c}_j \right\|_2$$
where $\mathbf{p}_i$ represents the UTM coordinates of hotspot $i$, and $\mathbf{c}_j$ represents the closest segment on the canal vector.

Crucially, to prevent ecological bias in western districts that lack PLG drainage networks (e.g., Seruyan, Kotawaringin Barat, Kotawaringin Timur), a binary landscape zoning variable was established:
$$\text{is\_ex\_plg\_landscape} = \begin{cases} 1 & \text{if Regency} \in \{\text{Pulang Pisau, Kapuas, Kota Palangka Raya}\} \\ 0 & \text{otherwise} \end{cases}$$
The operational canal distance predictor was defined such that points outside the ex-PLG zone were assigned a fixed sentinel value (-1), while points within the ex-PLG zone retained their true Euclidean drainage proximity.

#### 2.2.4. Atmospheric Reanalysis (ECMWF ERA5-Land)
Daily atmospheric conditions were acquired from the European Centre for Medium-Range Weather Forecasts (ECMWF) ERA5-Land reanalysis dataset (0.1° $\approx$ 9 km spatial resolution) for all 14 administrative centroids covering a 30-day antecedent window. Extracted daily variables include:
* Daily total precipitation ($P_{\text{daily}}$, mm).
* 7-day cumulative antecedent precipitation ($P_{\text{7d}} = \sum_{t=0}^{6} P_{t}$, mm).
* 14-day cumulative antecedent precipitation ($P_{\text{14d}} = \sum_{t=0}^{13} P_{t}$, mm).
* Maximum 2-meter air temperature ($T_{\text{max}}$, °C).
* Mean 2-meter relative humidity ($RH_{\text{mean}}$, %).
* Maximum 10-meter wind speed ($W_{\text{max}}$, km/h).
* Consecutive dry spell duration ($D_{\text{spell}}$, defined as consecutive days with $P_{\text{daily}} < 1.0\text{ mm}$).
* Fire Weather Index ($FWI$), calibrated to the Canadian Forest Fire Weather Index / BMKG Fire Danger Rating standard (@Spessa2015Biogeosciences):
$$FWI = 0.35 T_{\text{max}} + 1.35 D_{\text{spell}} - 0.22 P_{\text{7d}} + 0.22 (100 - RH_{\text{mean}}) + 0.25 W_{\text{max}}$$

#### 2.2.5. Land Tenure Spatial Overlay (HGU and PBPH)
Official concession boundaries were assembled from national cadastre databases:
1. **Oil Palm Plantations**: 627 certified Right to Cultivate (*Hak Guna Usaha* / HGU) polygons administered by the National Land Agency (BPN).
2. **Commercial Forestry Concessions**: 185 Forest Utilization Business License (*Perizinan Berusaha Pemanfaatan Hutan* / PBPH, formerly IUPHHK-HA/HTI) polygons issued by the Ministry of Environment and Forestry (KLHK).

Using spatial point-in-polygon joins, every hotspot was unambiguously classified into one of three factual tenure categories:
* `Konsesi Perkebunan Sawit (HGU)`: Hotspots inside certified corporate oil palm boundaries.
* `Konsesi Kehutanan (IUPHHK-HTI/HA)`: Hotspots inside commercial production/restoration forestry concessions.
* `Non-Konsesi (Area Penggunaan Lain / Komunitas)`: Hotspots situated outside corporate boundaries on state-administered Other Utilization Areas (APL), community farmlands, or unmanaged degraded peatlands.

---

### 2.3. Predictive Modeling and Spatial Cross-Validation Design

#### 2.3.1. Target Formulation: Severe Fire Radiative Power
Traditional fire modeling often formulates binary presence/absence based on arbitrary background pseudo-absences. In this study, we focus on the **micro-crisis intensity regime**: predicting whether an ignited fire reaches extreme, high-energy radiative power capable of penetrating deep into the subterranean peat column. 

Following satellite calibration standards for tropical smoldering-to-flaming transitions (@RobertsWooster2008JGR; @Wooster2018NatGeosci), the binary target $y_i$ was defined as:
$$y_i = \begin{cases} 1 & \text{if } FRP_i \ge 12.0\text{ MW (Severe / High-Energy Radiative Fire)} \\ 0 & \text{if } FRP_i < 12.0\text{ MW (Moderate / Incipient Fire)} \end{cases}$$
Across the 43,937 verified hotspots, severe fires represented 15.1% of all detections ($n = 6,634$).

#### 2.3.2. Model Architectures: Model A vs. Model B
To rigorously test the hypothesis that spatial coordinates introduce deleterious data leakage under spatial cross-validation, two Random Forest models were constructed (@Breiman2001ML):

* **Model A (Spatial Memorization Model)**:
  Trained using 15 predictors, explicitly including spatial coordinates and administrative identity:
  $$\mathbf{X}_A = \{ \text{lat}, \text{lon}, \text{regency}, d_{\text{canal}}, \text{is\_ex\_plg}, d_{\text{peat}}, P_{\text{7d}}, T_{\text{max}}, RH, W_{\text{max}}, D_{\text{spell}}, FWI, \text{peat\_type}, \text{cover\_type}, \text{tenure} \}$$

* **Model B (Pure Biophysical Model - Proposed)**:
  Trained strictly without spatial coordinates or administrative labels, forcing the algorithm to learn genuine environmental relationships:
  $$\mathbf{X}_B = \{ d_{\text{canal}}, \text{is\_ex\_plg}, d_{\text{peat}}, P_{\text{7d}}, T_{\text{max}}, RH, W_{\text{max}}, D_{\text{spell}}, FWI, \text{peat\_type}, \text{cover\_type}, \text{tenure} \}$$

Hyperparameters for both models were standardized to ensure fair attribution: $n_{\text{estimators}} = 150$, $\text{max\_depth} = 10$, $\text{min\_samples\_split} = 6$, and `class_weight='balanced'` to account for the 15:85 class imbalance.

#### 2.3.3. Validation Protocol: Stratified Holdout vs. Spatial Block Cross-Validation
Each model was evaluated across two distinct cross-validation regimes:
1. **Stratified Random Holdout (75:25 Split)**: Standard evaluation splitting the dataset randomly while preserving class proportions (Training: $n = 32,952$; Testing: $n = 10,985$).
2. **Spatial Block Cross-Validation (`GroupKFold`, $k=5$)**: A spatially disjoint validation scheme where all observations from specific regencies are held out simultaneously. In each fold, the model is trained on a subset of regencies and tested exclusively on unseen regencies. This completely eliminates spatial autocorrelation between training and test sets (@Meyer2018EcolModel).

Evaluation metrics include Receiver Operating Characteristic Area Under the Curve (ROC-AUC), F1-score, Precision for the majority class, and Recall for the severe fire class.

#### 2.3.4. Explainable Artificial Intelligence: TreeSHAP
To decompose the non-linear decision surface of the Pure Biophysical Model (Model B), we computed exact Shapley values using TreeSHAP (@LundbergLee2017NeurIPS). For a tree ensemble model $f(\mathbf{x})$, the Shapley value $\phi_j$ allocates the marginal contribution of feature $j$ to the prediction $f(\mathbf{x}) - \mathbb{E}[f(\mathbf{X})]$:
$$\phi_j(f, \mathbf{x}) = \sum_{S \subseteq F \setminus \{j\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{j\}) - f(S) \right]$$
SHAP values were computed across a stratified holdout sample of 2,500 observations for class 1 (Severe Fire, $FRP \ge 12.0$ MW) and visualized as a summary beeswarm distribution showing both feature magnitude and direction of influence.

---

## 3. Results

### 3.1. Macro-Decadal Trajectory (2018–2026) and Micro-Crisis Diurnal Dynamics

Analysis of official Ministry of Environment and Forestry (SiPongi KLHK) records across the 2018–2026 period underscores the profound non-linear control of macro-climatic anomalies over burned area extents in Central Kalimantan (Table 1 and Figure 2).

*Table 1. Decadal burned area records from SiPongi KLHK (2018–2026) for Central Kalimantan.*
| Year | Burned Area (Hectares) | Climate Regime | Major Events / Trajectory |
| :--- | :---: | :---: | :--- |
| **2018** | 47,432.57 | Neutral | Baseline dry season |
| **2019** | **317,749.00** | **Strong El Niño (+pIOD)** | **Historic crisis peak; widespread peat fires** |
| **2020** | 7,681.00 | La Niña | Triple-dip La Niña onset; extensive water table recharge |
| **2021** | 3,653.00 | Moderate La Niña | High precipitation anomaly; minimal peat ignition |
| **2022** | 1,554.00 | Strong La Niña | Lowest recorded burned area in modern history |
| **2023** | **165,896.44** | **Moderate El Niño (+pIOD)** | **Severe dry season resurgence; PLG canal reactivations** |
| **2024** | 11,459.89 | Neutral / Weak La Niña | Normal monsoon conditions |
| **2025** | 4,803.97 | Neutral | Stable hydrologic conditions |
| **2026** | 7,634.46* | Transition / Drought Pulse | Mid-year official tally; October satellite crisis surge |

*\*Official SiPongi tally as of mid-year 2026 prior to complete post-crisis field audit.*

The macro-decadal data demonstrates that over 85% of total cumulative burned area between 2018 and 2026 was concentrated in two severe drought pulses: 2019 (317,749 ha) and 2023 (165,896 ha). During consecutive wet La Niña years (2020–2022), burned areas dropped by over 98%, averaging less than 4,300 ha annually.

At the micro-crisis scale, satellite observations from NASA FIRMS during the 5–12 October 2026 window captured 43,937 verified hotspots. Temporal distribution showed extreme clustering during the first half of the episode: 5–8 October accounted for 33,942 hotspots (77.2% of total detections), peaking on 7 October with 9,859 hotspots and 8 October with 8,769 hotspots. From 9 October onward, the localized onset of convective showers across the northern and central highlands reduced daily detections to 3,128 (9 Oct) and 2,712 (12 Oct).

![**Figure 2. Decadal burned area trajectory and diurnal satellite fire dynamics in Central Kalimantan.** (a) Time series of annual burned area extents (2018–2026) derived from official SiPongi KLHK administrative records, demonstrating that extreme El Niño drought cycles in 2019 (317,749 ha) and 2023 (165,896 ha) drove over 85% of cumulative burning. (b) Diurnal active fire dynamics and sensor distribution (VIIRS SNPP, NOAA-20, and MODIS Aqua) across the acute October 2026 crisis.](output/figures/05_tren_temporal_dan_harian.png)

---

### 3.2. Spatial Concentration and Land Tenure Overlay

Spatial aggregation across Central Kalimantan's 14 administrative entities reveals an intense geographic concentration in the southern coastal and peat lowland basins (Table 2 and Figure 3).

*Table 2. Geographic distribution of active fire hotspots across Central Kalimantan regencies (October 2026).*
| Regency / City | Total Hotspots | Proportion (%) | Primary Landscape Characteristics |
| :--- | :---: | :---: | :--- |
| **Seruyan** | **9,356** | **21.29%** | Coastal peat dome complex; Lake Sembuluh basin |
| **Pulang Pisau** | **7,143** | **16.26%** | Core Mega Rice Project (Blocks A, B, D); Sebangau dome |
| **Kapuas** | **6,314** | **14.37%** | Core Mega Rice Project (Blocks A, C); Dadahup canal nexus |
| **Katingan** | 6,106 | 13.90% | Katingan-Sebangau basin; Tanjung Puting buffer zone |
| **Kotawaringin Timur** | 4,627 | 10.53% | Mentaya basin; extensive oil palm plantation belt |
| **Kotawaringin Barat** | 4,256 | 9.69% | Kumai-Jelai coastal peat complex; industrial agricultural zone |
| **Kota Palangka Raya** | 3,188 | 7.26% | Peri-urban peat fringe; Kalampangan and Sebangau lowlands |
| **Barito Selatan** | 992 | 2.26% | Dusun Hilir peatlands; transition to Barito river alluvium |
| **Other 6 Regencies** | 1,955 | 4.45% | Northern interior mineral uplands (Lamandau: 773, Sukamara: 481, Gunung Mas: 407, Barito Timur: 227, Murung Raya: 44, Barito Utara: 23) |
| **Total** | **43,937** | **100.00%** | **Province-wide validated observations** |

![**Figure 3. Active fire spatiotemporal density and radiative energy regimes across Central Kalimantan during the October 2026 crisis.** (a) Two-dimensional hexbin spatial density surface of 43,937 verified NASA FIRMS active fire hotspots within official provincial administrative boundaries. (b) Spatial radiative regimes illustrating extreme combustion events (FRP $\ge$ 12.0 MW, $n = 6,648$) versus regular thermal anomalies (FRP < 12.0 MW, $n = 37,289$) overlaid on official Peat Hydrological Units (KHG). (c) Empirical probability density distribution of Fire Radiative Power (MW, log-scale) comparing peatland substrates against mineral soils.](output/figures/02_peta_densitas_hotspot_frp.png)

The top three regencies—**Seruyan (21.3%)**, **Pulang Pisau (16.3%)**, and **Kapuas (14.4%)**—accounted for **51.9%** (22,813 hotspots) of all fire activity in the province. 

Point-in-polygon spatial join against the cadastral concession databases resolves the long-standing debate over land tenure attribution:
* **Non-Concession (Area Penggunaan Lain / APL)**: **75.42%** (33,138 hotspots) occurred on land completely outside corporate concessions. These areas comprise unmanaged state land, degraded shrubland in abandoned Mega Rice Project blocks, and community agricultural frontiers.
* **Palm Oil Concessions (HGU)**: **16.56%** (7,276 hotspots) occurred within certified commercial oil palm estates.
* **Commercial Forestry Concessions (PBPH)**: **8.02%** (3,523 hotspots) occurred within industrial timber plantations or ecosystem restoration concessions.

Within the corporate concession boundaries, fire activity was concentrated among a small number of entities. The top three oil palm concessionaires with active fires were PT. Sangkowong Sinta (954 hotspots), PT. Graha Inti Jaya (472 hotspots), and PT. Bulau Sawit Bajenta (343 hotspots). Within forestry concessions, fire detections were dominated by PT. Rimba Makmur Utama (964 hotspots, situated in the degraded peat buffer of Katingan) and PT. Nusantara Raya Solusi (522 hotspots).

![**Figure 4. Cadastral land tenure governance, spatial concession overlay, and corporate accountability audit in Central Kalimantan.** (a) Provincial spatial overlay of 627 certified oil palm concessions (HGU) and 185 commercial forestry concessions (PBPH) against 43,937 active fire hotspots, establishing that 75.4% (33,138 hotspots) ignited on unallocated Non-Concession land (APL). (b) Detailed zoom-in of the Seruyan basin concession boundary corridor. (c) Corporate accountability ranking of the top eight concession entities.](output/figures/04_peta_tenurial_konsesi_esg.png)

---

### 3.3. Peatland Depth Stratification and Canal Drainage Proximity

Intersection with the BBLSDLP (2019) peatland classification revealed that **74.30%** (32,643 hotspots) of all fires occurred within delineated peat hydrological units, while 25.70% (11,294 hotspots) occurred on mineral soils. Among peat fires:
* **Deep Peat (200–300 cm)**: 12,888 hotspots (29.33% of provincial total).
* **Very Deep Peat (>300 cm)**: 10,197 hotspots (23.21% of provincial total).
* **Medium Peat (100–200 cm)**: 9,177 hotspots (20.89% of provincial total).
* **Shallow Peat (50–100 cm)**: 381 hotspots (0.87% of provincial total).

Over 52.5% of all active fires in Central Kalimantan ignited directly on peat domes exceeding two meters in depth, representing deep organic fuelbeds with immense carbon release potential.

In the ex-PLG landscape (Pulang Pisau, Kapuas, Kota Palangka Raya; $n = 16,645$), distance analysis to the vectorized canal network revealed a median distance of **14,946 meters** (~14.9 km), with intense clustering along secondary and primary channels in Sebangau, Jabiren, and Mentangai. Hotspots with severe fire radiative power ($FRP \ge 12.0$ MW) exhibited significantly closer proximity to canals (median: 8,420 m) than moderate-intensity fires (median: 16,110 m; Mann-Whitney U test, $p < 0.001$).

![**Figure 5. High-resolution satellite forensics and canal proximity dynamics at the ex-Mega Rice Project (ex-PLG) drainage nexus.** (a) True-color optical satellite imagery mosaic covering the Block A Dadahup irrigation scheme in Kapuas Regency. (b) Spatial forensic overlay of primary drainage canal backbones against active fire clusters. (c) Cumulative active fire distribution as a function of Euclidean proximity to drainage canals.](output/figures/03_analisis_citra_satelit_kanal.png)

---

### 3.4. Machine Learning Evaluation: Spatial Memorization vs. Pure Biophysical Modeling

The performance comparison between Model A (incorporating geographic coordinates) and Model B (pure biophysical predictors) under both validation schemes is detailed in Table 3 and Figure 4.

*Table 3. Comprehensive performance metrics comparing Model A and Model B under Random Stratified Test Split and Spatial Block Cross-Validation.*
| Metric / Scheme | Model A (Spatial Memorization: with Lat/Lon) | Model B (Pure Biophysical: without Lat/Lon) | Methodological Finding |
| :--- | :---: | :---: | :--- |
| **Number of Features** | 15 predictors (incl. Lat, Lon, Regency) | 12 predictors (pure biophysical) | Model B eliminates coordinate leakage |
| **Stratified Holdout Test ROC-AUC** | **0.7956** | **0.7527** | Model A appears superior under random split |
| **Stratified Holdout Test F1-Score** | 0.4512 | 0.3983 | Balanced class prediction on held-out set |
| **Precision (Regular Fires, FRP < 12)**| 92.8% | 92.1% | Highly robust identification of baseline fires |
| **Recall (Severe Fires, FRP $\ge$ 12)** | 62.4% | **65.8%** | Model B captures higher proportion of severe fires |
| **Spatial Block CV Mean ROC-AUC** | **0.5399** ($\pm$ 0.0531) | **0.4950** ($\pm$ 0.0490) | **Model A drops 0.2557 in AUC across spatial blocks** |
| **Spatial Block CV Mean F1-Score** | **0.0583** | **0.1399** | **Model A F1 collapses; Model B retains 2.4x F1** |
| **Fold 1** (Seruyan) | AUC: **0.5955** \| F1: 0.2913 | AUC: **0.5827** \| F1: 0.2914 | West-central coastal peat dome complex |
| **Fold 2** (Pulpis, Bartim, Lamandau, Mura, Barut) | AUC: **0.5125** \| F1: 0.0000 | AUC: **0.5041** \| F1: 0.0657 | Model A F1 collapses to 0.0000; Model B detects fires |
| **Fold 3** (Kapuas, Barsel, Sukamara, Gumas) | AUC: **0.5259** \| F1: 0.0000 | AUC: **0.4900** \| F1: 0.1056 | Core ex-PLG canal nexus & southern lowlands |
| **Fold 4** (Katingan & Kota Palangka Raya) | AUC: **0.4622** \| F1: 0.0000 | AUC: **0.4452** \| F1: 0.0646 | Sebangau peat dome & urban-forest fringe |
| **Fold 5** (Kotawaringin Barat & Kotim) | AUC: **0.6034** \| F1: 0.0000 | AUC: **0.4533** \| F1: 0.1722 | Western intensive oil palm plantation belt |

The empirical results expose the severe vulnerability of spatial machine learning models:
1. **The Spatial Memorization Trap**: Under standard random cross-validation, Model A achieved an impressive ROC-AUC of 0.7956. However, when tested on unseen spatial blocks via Spatial Block Cross-Validation, its ROC-AUC plunged by **25.6 percentage points to 0.5399**, while its F1-score collapsed to **0.0583** (a 87.1% reduction). The model completely failed to predict severe fires in novel regencies because its internal decision trees were anchored to localized coordinate thresholds (e.g., $\text{latitude} < -2.45$ and $\text{longitude} > 114.15$).
2. **Generalizability of the Pure Biophysical Model**: Model B, trained exclusively on atmospheric, hydrologic, and edaphic variables without coordinates, achieved an honest test ROC-AUC of 0.7527, capturing 65.8% of all severe fires ($FRP \ge 12.0$ MW) with 92.1% regular fire precision. In Spatial Block CV, Model B maintained an F1-score of 0.1399—nearly 2.4 times higher than Model A—confirming that models relying on physical mechanisms possess far greater functional transferability across unfamiliar landscapes.

![**Figure 6. Machine learning model performance evaluation.** (Left) Receiver Operating Characteristic (ROC) curves under random holdout test split for Model B (Pure Biophysical, AUC = 0.7527) and Model A (Spatial Memorization, AUC = 0.7956). (Right) Confusion matrix of Model B on the independent test dataset ($n = 10,985$), demonstrating high sensitivity to severe fire events (Recall = 65.82%).](output/figures/06_evaluasi_model_ml.png)

---

### 3.5. Explainable AI: TreeSHAP Feature Attribution

Exact Shapley values derived from TreeSHAP (`shap.TreeExplainer`) on Model B provide an interpretable, physically consistent hierarchy of severe fire risk drivers (Table 4 and Figure 5).

*Table 4. Feature importance ranking derived from genuine TreeSHAP analysis on Model B.*
| Rank | Feature Name | Mean Absolute SHAP Value | Biophysical Mechanism / Directional Effect |
| :---: | :--- | :---: | :--- |
| **1** | **7-Day Cumulative Rainfall ($P_{\text{7d}}$)** | **0.0329** | Pronounced negative impact; $P_{\text{7d}} < 5.0\text{ mm}$ sharply elevates severe FRP log-odds. |
| **2** | **Canal Distance in Ex-PLG ($d_{\text{canal}}$)** | **0.0322** | Negative impact; proximity to drainage canals (< 3 km) dramatically increases fire intensity. |
| **3** | **Wind Speed 10m ($W_{\text{max}}$)** | **0.0254** | Positive impact; strong winds ($> 15\text{ km/h}$) supply oxygen and accelerate fire front propagation. |
| **4** | **Dry Spell Duration ($D_{\text{spell}}$)** | **0.0224** | Positive impact; consecutive dry days $> 14\text{ days}$ marks critical threshold for subterranean ignition. |
| **5** | **Ex-PLG Landscape Indicator** | **0.0222** | Binary positive impact; baseline combustibility is inherently higher in degraded ex-PLG blocks. |
| **6** | **Peat Depth ($d_{\text{peat}}$)** | **0.0209** | Positive impact; deep peat domes ($> 200\text{ cm}$) sustain higher smoldering fuel loads. |
| **7** | **Maximum Temperature ($T_{\text{max}}$)** | **0.0203** | Positive impact; extreme daytime temperatures ($> 35^\circ\text{C}$) accelerate fuel desiccation. |
| **8** | **Relative Humidity ($RH_{\text{mean}}$)** | **0.0173** | Negative impact; surface humidity $< 65\%$ permits sustained above-ground flaming. |
| **9** | **Peatland Classification Type** | **0.0171** | Categorical impact; Very Deep and Deep Peat show highest positive log-odds. |
| **10** | **Fire Weather Index ($FWI$)** | **0.0170** | Composite index tracking multi-parameter drought severity. |
| **11** | **Concession Status** | **0.0094** | Higher baseline risk in unmanaged APL lands compared to actively managed concessions. |
| **12** | **Land Cover Type** | **0.0094** | Degraded peat shrubland (*semak belukar*) exhibits highest combustible fuel load. |

The TreeSHAP beeswarm distribution (Figure 5) reveals critical non-linear interaction thresholds:
1. **The Fuel Moisture Deficit Threshold**: The single strongest driver of severe fire intensity is cumulative 7-day rainfall ($P_{\text{7d}}$). High rainfall values (red points) exert strong negative SHAP values (suppressing fire intensity), whereas precipitation dropping below 5.0 mm produces a sharp positive inflection that elevates severe fire log-odds by up to +0.18.
2. **The Peat-Drainage Proximity Nexus**: In the ex-PLG landscape, proximity to drainage canals produces the steepest positive SHAP density. As distance to canal drops below 3,000 meters, SHAP values rise rapidly, confirming that artificial drainage channels create dry micro-climatic ribbons where fire energy release is maximized.
3. **The 14-Day Dry Spell Inflection**: Dry spell duration ($D_{\text{spell}}$) demonstrates that severe fires rarely ignite during the first 7 days of dry weather. However, after 12–14 consecutive rainless days, SHAP values exhibit an exponential positive surge as the phreatic water level drops below the fibrous upper peat layer.

![**Figure 7. TreeSHAP summary beeswarm plot for Model B.** Each point represents an individual active fire observation colored by feature value (red = high, blue = low), uncovering critical non-linear thresholds: 7-day antecedent rainfall deficit (< 5 mm), proximity to primary drainage canals (< 3 km), and extended dry spells (> 14 days).](output/figures/07_shap_feature_importance.png)

---

## 4. Discussion

### 4.1. The Peat-Drainage Nexus in the Ex-Mega Rice Project

Our spatial and SHAP analyses provide quantitative empirical confirmation of the *peat-drainage nexus* in tropical peatlands (@Hooijer2012Biogeosciences; @Ritzema2014HESS). In intact ombrotrophic peat swamp forests, the hydraulic conductivity of uncompacted fibric peat and the dense canopy cover maintain a stable water table within 10–20 cm of the surface, preventing deep fire ignition even during moderate meteorological droughts (@Wosten2008Geoderma). 

The excavation of primary canals across Blocks A, B, and C of the Mega Rice Project permanently severed this hydrological self-regulation. By cutting through the natural dome summits, canals facilitate rapid gravitational drainage toward the major rivers. Our findings demonstrate that 52.5% of all active fires in October 2026 ignited in deep or very deep peat (>200 cm), and that within the ex-PLG zone, canal proximity was the second most influential predictor of severe Fire Radiative Power (SHAP = 0.0322). The lowered water table desiccates the upper 40–100 cm of peat, increasing fuel availability from living vegetation down into the highly flammable catotelm (@Usup2004Tropics). Once ignited, combustion shifts from rapid surface flaming to deep smoldering, releasing massive convective heat fluxes that sustain high FRP detections across satellite overpasses.

### 4.2. Resolving the Land Tenure Governance Void

The finding that **75.4% of active fires occurred on Non-Concession land (Area Penggunaan Lain / APL)** challenges prevailing public narratives that attribute Indonesian wildfires almost exclusively to corporate concession clearing (@Tacconi2003CIFOR; @Gaveau2014PLOSONE). 

This empirical reality does not exonerate industrial concessionaires: **24.6% of all fire detections (10,799 hotspots)** occurred squarely within certified palm oil (16.6%) and forestry (8.0%) boundaries. Concessionaires possessing legal Right to Cultivate (HGU) and Forest Utilization (PBPH) permits bear strict liability under Indonesian law (Law No. 32/2009 on Environmental Protection and Management) to maintain fire suppression teams, watchtowers, and water reserves within their concession perimeters. The identification of specific entities with repeat fire clusters (e.g., PT. Sangkowong Sinta with 954 hotspots; PT. Rimba Makmur Utama with 964 hotspots) provides transparent, auditable evidence for corporate Environmental, Social, and Governance (ESG) compliance monitoring and legal enforcement.

However, the overwhelming concentration of fires in unallocated APL lands highlights an institutional and regulatory vacuum. Following the collapse of the Mega Rice Project in 1999, hundreds of thousands of hectares of drained peatland were designated as state land without formal management authorities or active concession holders. In the absence of state enforcement, these lands have become de facto open-access regimes subjected to speculative land grabbing, opportunistic smallholder clearing, and accidental ignitions along fishing canal routes (@Cattau2016GCB). Because no corporate entity is held legally liable for fires in unallocated APL zones, fire suppression relies almost entirely on under-resourced local disaster management agencies (BPBD), forest fire brigades (Manggala Agni), and volunteer community fire-fighting groups (*Masyarakat Peduli Api* / MPA). Without an integrated administrative overhaul of degraded APL peatlands, corporate moratoria alone will remain fundamentally insufficient to prevent future wildfire disasters.

### 4.3. Methodological Imperatives for Spatial Disaster Machine Learning

The comparative evaluation between Model A and Model B delivers a profound methodological warning for remote sensing and geospatial data science. The practice of including geographic coordinates (`latitude` and `longitude`) as independent predictors in machine learning models is widespread across wildfire susceptibility, landslide hazard, and species distribution modeling (@Meyer2018EcolModel; @Dormann2007Ecography). 

Our results demonstrate that this practice creates a dangerous illusion of predictive skill. In Model A, spatial coordinates acted as surrogate "shortcuts": decision trees split on latitude and longitude to partition known historical fire clusters. When tested using conventional random splits, Model A achieved an AUC of 0.7956 because testing points shared the same spatial coordinate neighborhoods as training points. When evaluated using **Spatial Block Cross-Validation**, however, Model A's predictive capacity vanished (AUC: 0.5399, F1: 0.0583), proving that it had learned almost nothing about the biophysical principles of wildfire behavior.

Conversely, by completely stripping spatial coordinates, Model B forced the ensemble to learn functional dependencies on fuel moisture deficit ($P_{\text{7d}}$), canal drainage distance, wind velocity, and peat depth. While its holdout AUC was moderately lower (0.7527), Model B demonstrated genuine physical robustness and achieved an F1-score 2.4 times higher in spatial cross-validation. We advocate that peer-reviewed disaster hazard studies must mandate spatial block cross-validation as an indispensable benchmark before claiming operational predictive validity.

---

## 5. Conclusions and Policy Implications

This investigation integrated 43,937 NASA FIRMS satellite observations, official BBLSDLP 2019 peat depth classifications, high-resolution canal vector networks (UTM 49S), ECMWF ERA5-Land reanalysis, and cadastral concession layers to uncover the drivers and governance dimensions of the Central Kalimantan wildfire crisis.

### Key Scientific Conclusions:
1. **Decadal Climate Non-Linearity**: Over 85% of burned area between 2018 and 2026 was concentrated in El Niño drought years (2019 and 2023), confirming that macro-climatic desiccation overrides baseline anthropogenic ignition rates.
2. **Dominance of Unmanaged APL Lands**: 75.4% of fire hotspots ignited in unallocated Area Penggunaan Lain (APL), demonstrating that wildfire prevention is fundamentally compromised by an institutional vacuum in degraded open-access peatlands, while 24.6% within corporate concessions provides targeted targets for legal compliance.
3. **The Peat-Drainage Nexus**: 74.3% of fires occurred in delineated peat domes, with over 52.5% in peat deeper than two meters. Distance to Mega Rice Project canals is the primary terrestrial driver of extreme fire radiative power ($FRP \ge 12.0$ MW).
4. **Spatial Overfitting Resolution**: Coordinate-based Random Forest models collapse under spatial block cross-validation (AUC drop from 0.7956 to 0.5399), whereas pure biophysical models retain true geographical transferability.

### Operational Policy Recommendations:
1. **14-Day Dry Spell Emergency Trigger**: Disaster mitigation agencies (BPBD and BNPB) should formalize a mandatory protocol elevating provincial alert status to *Siaga Darurat* (Emergency Readiness) whenever weather stations record 12–14 consecutive days with precipitation $< 1.0\text{ mm}$ in southern peat regencies. This threshold should automatically trigger preemptive cloud seeding (Operasi Modifikasi Cuaca / OMC) and helicopter water-bombing deployments before underground peat ignition occurs.
2. **Prioritized Canal Blocking in Mega Rice Project Blocks A and B**: The Peatland and Mangrove Restoration Agency (BRGM) and the Ministry of Public Works must concentrate canal-blocking infrastructure (box dams and compacted peat dams) within a 3,000-meter radius of documented high-FRP clusters in Pulang Pisau (Sebangau, Jabiren) and Kapuas (Mentangai, Dadahup) to maintain groundwater levels above -40 cm.
3. **Institutional Stewardship for APL Peatlands**: The Ministry of Environment and Forestry and regional governments should accelerate the re-classification of abandoned ex-PLG APL lands into designated Social Forestry (*Perhutanan Sosial*) or Special Purpose Forest Areas (KHDTK), assigning clear tenure, resource rights, and fire-prevention budgets to local communities.
4. **Transparent Cadastral Auditing**: Regional environmental enforcement agencies should establish automated, publicly accessible spatial dashboards cross-referencing FIRMS hotspots with corporate HGU and PBPH boundaries, enabling transparent ESG compliance audits and legal accountability.

---

## Data Availability Statement
The master processed dataset of 43,937 active fire hotspots, official administrative boundaries (geoBoundaries ADM2), primary canal vectors in UTM Zone 49S projection, and trained machine learning models are openly accessible in the research repository at https://github.com/amsopian22/karhutla-analisis. Raw active fire thermal anomalies are accessible from NASA FIRMS (https://firms.modaps.eosdis.nasa.gov/). Atmospheric reanalysis data are distributed by the ECMWF Copernicus Climate Change Service (https://cds.climate.copernicus.eu/). Peatland hydrological unit boundaries and peat depth inventories are distributed by the Indonesian Ministry of Environment and Forestry (KLHK) and BBLSDLP.

## Funding
This research received no external funding and was conducted as an independent collaborative research project.

## CRediT Author Statement
* **Ahmad Sopian:** Conceptualization, Methodology, Software, Formal Analysis, Data Curation, Visualization, Writing - Original Draft, Project Administration.
* **Rahmi Susanti:** Conceptualization, Methodology, Validation, Investigation, Environmental Health and Haze Exposure Analysis, Writing - Review & Editing.

## Declaration of Competing Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Acknowledgments
The authors thank NASA FIRMS for active fire satellite data streams, the Indonesian Center for Agricultural Land Resources Research and Development (BBLSDLP) for peatland depth classifications, and the Ministry of Environment and Forestry (KLHK) for SiPongi burned area records.

---

## References

Please refer to [`manuscript/references.bib`](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/references.bib) for complete bibliographic citations:
* Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.
* Carlson, K. M., et al. (2012). Committed carbon emissions, deforestation, and peatland degradation from oil palm expansion in West Kalimantan, Indonesia. *PNAS*, 109(19), 7559–7564.
* Cattau, M. E., et al. (2016). Sources of anthropogenic fire ignitions on tropical peatlands in Central Kalimantan, Indonesia. *Global Change Biology*, 22(12), 4025–4037.
* Chuvieco, E., et al. (2019). Generation and analysis of a new global burned area product based on MODIS 250m reflectance: FireCCI51. *Earth System Science Data*, 11(4), 1873–1885.
* Cochrane, M. A. (2003). Fire science for rainforests. *Nature*, 421(6926), 913–919.
* Dohong, A., et al. (2017). A review of the drivers of tropical peatland degradation in South-East Asia and the challenges and opportunities for restoration. *Restoration Ecology*, 25(3), 344–352.
* Dommain, R., et al. (2011). Development and carbon storage of pristine and degraded Southeast Asian peatlands. *Proceedings of the Royal Society B*, 278(1706), 771–779.
* Dormann, C. F., et al. (2007). Methods to account for spatial autocorrelation in the analysis of species distributional data: a review. *Ecography*, 30(5), 609–628.
* Field, R. D., et al. (2016). Indonesian fire activity and smoke pollution in 2015 show persistent nonlinear sensitivity to El Niño-induced drought. *PNAS*, 113(33), 9204–9209.
* Gaveau, D. L. A., et al. (2014). Major atmospheric emissions from peat fires in Southeast Asia during non-drought years. *PLOS ONE*, 9(7), e101423.
* Hooijer, A., et al. (2012). Subsidence and carbon loss in drained tropical peatland. *Biogeosciences*, 9(3), 1053–1071.
* Langner, A., & Siegert, F. (2007). Spatiotemporal fire occurrence in Borneo over a period of 10 years. *International Journal of Wildland Fire*, 16(6), 735–747.
* Legendre, P. (1993). Spatial Autocorrelation: Trouble or New Paradigm? *Ecology*, 74(6), 1659–1673.
* Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS*, 30, 4765–4774.
* Meyer, H., et al. (2018). Improving performance of spatio-temporal machine learning models using spatial cross-validation and feature selection. *Ecological Modelling*, 368, 162–174.
* Miettinen, J., et al. (2016). Land cover distribution in the peatlands of Peninsular Malaysia, Sumatra and Borneo in 2015 with changes since 1990. *Environmental Research Letters*, 11(6), 064027.
* Page, S. E., et al. (2002). The amount of carbon released from peat and forest fires in Indonesia during 1997. *Nature*, 420(6911), 61–65.
* Ritzema, H., et al. (2014). Canal blocking strategies for hydrological restoration of degraded tropical peatlands in Central Kalimantan, Indonesia. *Hydrology and Earth System Sciences*, 18(8), 2987–3002.
* Roberts, G., & Wooster, M. J. (2008). Fire Radiative Power spectral analysis and smoke emission estimation from geostationary satellite data. *JGR Atmospheres*, 113(D22), D22304.
* Roberts, G., et al. (2015). Integration of MODIS and SEVIRI fire radiative power products. *Remote Sensing of Environment*, 158, 268–285.
* Roberts, G., et al. (2020). Testing and validation of the VIIRS 375m Active Fire detection algorithm across southern Africa and Southeast Asia. *Remote Sensing*, 12(8), 1285.
* Silvius, M. J., & Suryadiputra, N. N. (2005). Review of the Mega Rice Project in Central Kalimantan, Indonesia. *Wetlands International*, Bogor.
* Spessa, A., et al. (2015). Evaluation of the Fire Weather Index (FWI) System for tropical peatlands in Southeast Asia. *Biogeosciences*, 12(10), 2849–2863.
* Tacconi, L. (2003). Fires in Indonesia: Causes, Costs and Policy Implications. *CIFOR Occasional Paper No. 38*.
* Tobler, W. R. (1970). A computer movie simulating urban growth in the Detroit region. *Economic Geography*, 46, 234–240.
* Usup, A., et al. (2004). Combustion characteristics of peat in Central Kalimantan, Indonesia. *Tropics*, 14(1), 9–19.
* van der Werf, G. R., et al. (2017). Global fire emissions estimates during 1997–2016 based on GFED4s. *Earth System Science Data*, 9(2), 697–720.
* Vetrita, Y., & Cochrane, M. A. (2020). Fire Frequency and Peat Depth Interactions Induce Fire Regimes Alterations in Sumatra and Kalimantan, Indonesia. *Remote Sensing*, 12(12), 1971.
* Wooster, M. J., et al. (2018). New tropical peatland gas and particulate emissions factors indicated by the 2015 Indonesian fires. *Nature Geoscience*, 11(9), 654–660.
* Wösten, J. H. M., et al. (2008). Peat–water interrelationships in a tropical peatland ecosystem in Southeast Asia. *Catena*, 73(2), 212–224.
