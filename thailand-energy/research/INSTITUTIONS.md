# Who plans Thailand's power system: technical institutions, their tools and key public reports

Version 1.0 · 2026-09-26 (UTC) · public-safe (no private parties, no political content)

**Rules used.** Only sources whose text was read (page or PDF) are included. A tool/model is named only when a source names it; otherwise the cell says **"not stated in public sources found"**. Items that were only visible as search-engine summaries in earlier drafts were either re-checked against the original (noted "re-verified 2026-09-26") or dropped. Access date for all links: 2026-09-25/26 UTC.

## 1. How the planning chain works (sourced)

1. **National Energy Policy Council (NEPC)** submits national energy policy and the energy management/development plan to Cabinet and sets rules for energy pricing (National Energy Policy Council Act 1992, s.6) [N1].
2. **EPPO** (Energy Policy and Planning Office, Ministry of Energy) recommends energy policy and plans, prepares energy forecasts, manages energy information, and its Energy Policy and Planning Division is the **NEPC secretariat** (Ministerial Regulation 2008) [N2].
3. **Load forecast**: PDP demand forecasts are produced by an EPPO-chaired Load Forecast working group/subcommittee (EGAT Annual Report 2024: PDP2018 Rev.1 forecast "prepared by the Load Forecast Working Group chaired by EPPO", approved 18 Jun 2018) [N3]. PDP2015 used **End-Use and Econometric models developed by Thammasat University** [N4]. The PDP2024 draft hearing slides list: residential electricity surveys, sectoral/national econometric models, mixed end-use + econometric models, and a long-term model by **NIDA (2021 update)**, with BAU and "Base" cases (the latter adds rail, EEC, EVs and the Energy Efficiency Plan) [N5].
4. **Generation/transmission expansion**: EGAT drafts the PDP supply plan with the Ministry of Energy; the PDP is one of five plans under the **Thailand Integrated Energy Blueprint (TIEB)** (PDP, EEP, AEDP, Gas, Oil) — TIEB is named as the frame ENTEC's research supports [N6]. The specific in-house EGAT capacity-expansion software is **not stated in public sources found**.
5. **Tariffs**: the **ERC** (Energy Regulatory Commission, Energy Industry Act 2007) licenses operators and sets tariff methodology under NEPC guidelines, including the automatic fuel adjustment (Ft) published every four months [N7][N8].
6. **Efficiency rules**: **DEDE** administers the Building Energy Code (Ministerial Regulation B.E. 2563/2020: new or modified buildings ≥2,000 m² in nine building types) [N9] and the Energy Efficiency Plan (draft **EEP 2024: −36 % energy intensity by 2037** vs 2010, up from −30 % in EEP 2018) [N10].
7. **Climate strategy**: Thailand's revised **LT-LEDS** (UNFCCC, 8 Nov 2022) uses **AIM/EndUse** (bottom-up least-cost technology model) and **AIM/CGE** (macro impacts, calibrated on the NESDC input-output table) [N11]; the modelling team presenting it is at SIIT, Thammasat University [N12].

## 2. Institution table

| Institution | Role in policy (sourced) | Data / models / tools (only if sourced) | Key public outputs | Sources |
|---|---|---|---|---|
| **Ministry of Energy** | Parent ministry of EPPO, DEDE, DOEB etc.; co-owner of PDP with EGAT; joint work programme with EGAT and IEA | PLEXOS model of the Thai system built by IEA with EGAT (used in the joint programme) | TIEB family of plans; PDP2018 Rev.1 (official); PDP2024 draft (hearing Jun 2024); draft PDP 2026 (consultation from 8 Sep 2026) | N6, N13, N14 |
| **EPPO** | Policy & plan recommendations; NEPC secretariat; national energy forecasts & statistics; chairs load-forecast working group | Open data portal (CKAN) with monthly generation, sales, peak, fuel tables (used in this study); trained on **LEAP** and **NEMO** by SEI for PDP scenario work (spring 2024); GIZ-supported Community of Practice on data for energy modelling (Oct 2025) | Energy statistics; PDP/EEP/AEDP drafts & hearing documents; load forecasts | N2, N3, N5, N15, N16, N17 |
| **EGAT** (incl. system planning) | State generator, transmission owner, single buyer and system operator; drafts PDP supply side | IEA–EGAT **PLEXOS** model (2023 report: production-cost + capacity-expansion modules); earlier 30-minute production-cost modelling in IEA flexibility study (2021); Renewable Energy Forecast Center and Demand Response Control Center (DR pilot 50 MW) | Annual Report (net heat rate, peak, contracted capacity); public hourly-demand pages (archived hourly data on Zenodo, CC-BY) | N3, N13, N18, N19, N20 |
| **ERC / OERC** | Independent regulator under Energy Industry Act 2007: licensing, tariff methodology, Ft, grid codes | Ft formula and four-monthly Ft decisions published on ERC site | Ft announcements; annual reports; NREL-drafted BESS technical-standards report written for ERC (2021) | N7, N8, N21 |
| **DEDE** | Energy conservation & renewable promotion; building code; labels & MEPS coordination; EEP implementation | Public data catalogue (pei.dede.go.th, electricity by economic sector CSV) | BEC 2020 + 2021 notification; EEP 2018 / draft EEP 2024 | N9, N10, N22 |
| **MEA / PEA** | Distribution utilities (Bangkok metro / rest of country); load aggregators in EGAT DR pilot; rooftop-solar scheme operators | Loss statistics in reports: PEA distribution loss **5.03 % (2024)**; MEA **2.13 % (2022)** | PEA sustainability report; MEA sales/loss reports; published tariff schedules | N20, N23, N24, N25 |
| **NSTDA / ENTEC** | National Energy Technology Center, NSTDA's 5th national centre (Cabinet approval 9 Jun 2020); mission: research supporting **TIEB**; bridge to DEDE and industry | Research areas: PV modelling & forecasting, batteries/storage, biofuels, smart grid (named on ENTEC pages) | R&D outputs; no national planning model identified | N6, N26 |
| **TDRI** | Independent policy think-tank | not stated in public sources found | 2026-04 energy-policy article: targeted instead of universal subsidies, TOU to cut peaks, "efficiency first" incl. AC/lighting/controls retrofits, link EEP with PDP, rooftop PV/TPA | N27 |
| **JGSEE (KMUTT)** | Graduate school and centre of excellence on energy & environment; Energy and Environmental Policy Laboratory (EEPL) produces policy studies/decision tools | EEPL "decision-making tools" (not individually named) | Policy studies; journal (JSEE) | N28 |
| **Chulalongkorn University Energy Research Institute (ERI)** | University policy research; co-author with Agora Energiewende of *Thailand's Natural Gas Crossroads* (2025); participant in EPPO/GIZ modelling Community of Practice | not stated in public sources found | *Natural Gas Crossroads* (2025): diversify gas, fewer new gas plants, integrated planning with digital DR/DER/storage/EV | N17, N29 |
| **TGO** (Thailand Greenhouse Gas Management Organization) | Public organization (Royal Decree 2007) promoting and managing GHG mitigation | Runs **T-VER** voluntary crediting (ISO 14064-2/-3; VVB oversight; registry) | T-VER / Premium T-VER guidelines | N30, N31 |
| **Thammasat University (SIIT, Faculty of Economics)** / **NIDA** | Modelling providers to government | AIM/EndUse & AIM/CGE for LT-LEDS; End-Use & Econometric models for PDP2015; NIDA long-term model (2021) for PDP2024 draft | LT-LEDS modelling | N4, N5, N11, N12 |

## 3. International technical partners

| Partner | What they did with Thai institutions (sourced) | Tool named | Sources |
|---|---|---|---|
| **IEA** | Joint work programme with EGAT and Ministry of Energy; *Thailand Power System Flexibility Study* (2021) and *Thailand's Clean Electricity Transition* (2023). Findings: contract flexibility (take-or-pay) cuts operating cost up to ~2 %, vs <0.05 % plant retrofits and <0.1 % storage at 2021 conditions; PDP2018 emissions would exceed targets by 44 % (2030) and 80 % (2037); "VRE Plus" adds 32 GW wind+solar by 2030 and 42 GW more by 2037 (re-verified 2026-09-26 in PDFs) | PLEXOS (2023); 30-min production-cost model (2021) | N13, N18 |
| **GIZ (Thai-German cooperation)** | PACT project with EPPO: Community of Practice on data acquisition for energy modelling (event 31 Oct 2025; data fragmentation across agencies noted by EPPO) | LEAP-based planning referenced | N17 |
| **SEI** | Trained EPPO (and EGAT) staff on LEAP/NEMO, ran PDP scenarios (presented spring 2024) | LEAP, NEMO | N16 |
| **USAID / NREL** | BESS technical-standards report for ERC (2021); Clean Power Asia programme guidance on BESS, DPV, EV (2016–21); Greater Mekong grid-integration training (2023) | not a planning model | N21, N32, N33 |
| **Agora Energiewende** | Co-authored gas study with Chula ERI (2025) | not stated | N29 |
| **ERIA** | *Energy Outlook and Energy Saving Potential in East Asia 2023*, Thailand chapter: APS 2050 primary energy −25 % vs BAU | not stated in chapter | N34 |
| **JICA** | Commissioned *Survey on Effective Energy Conservation Measures of Commercial Buildings in Bangkok* (final report 13 Mar 2020; walk-through audits of public and commercial buildings, notes DEDE subsidy programmes); no JICA power-planning model for Thailand found | not stated | N35 |
| **IRENA** | *Renewable Energy Outlook: Thailand* (2017) prepared with Ministry of Energy | REmap | N36 |

## 4. Gaps (stated plainly)
- EGAT's in-house capacity-expansion software and the load-forecast model code are **not public**.
- No public hourly end-use breakdown (e.g. share of AC in the evening peak) from any Thai agency.
- MEA loss rates after 2022 and EGAT transmission loss rate not found in public reports.

## 5. Sources
| ID | Source | URL | Date |
|---|---|---|---|
| N1 | National Energy Policy Council Act B.E. 2535 (English) | http://www.thailawforum.com/database1/national-energy-act.html | 1992 |
| N2 | Ministerial Regulation on the Organization of EPPO B.E. 2551 (ESCAP database) | https://policy.asiapacificenergy.org/node/3410 | 2008 |
| N3 | EGAT Annual Report 2024 (p.22–23 load forecast; heat rate) | https://www.egat.co.th (Annual Report 2024 PDF) | 2025 |
| N4 | Thailand Power Development Plan 2015–2036 (PDP2015), §load forecast | https://policy.asiapacificenergy.org/sites/default/files/PDP2015_Eng.pdf | 2015 |
| N5 | EPPO Draft PDP2024 hearing slides — unofficial slide-by-slide English translation (third party) | https://norway-connect.com/wp-content/uploads/2026/01/MOE-Draft-PDP-2024-Slide-by-Slide-English-Translation-260102.pdf | 2024 slides / 2026-01 translation |
| N6 | ENTEC — Vision and Mission | https://www.entec.or.th/aboutus/vision-and-mission/ | accessed 2026-09-26 |
| N7 | Energy Industry Act B.E. 2550 (English, EPPO) | https://www.eppo.go.th/images/law/ENG/energy_industry_act-2007.pdf | 2007 |
| N8 | ERC automatic tariff (Ft) page | https://www.erc.or.th/th/automatic | accessed 2026-09-25 |
| N9 | Ministerial Regulation on Building Energy Conservation (BEC) B.E. 2563, DEDE | https://2e-building.dede.go.th/sites/default/files/2022-11/1.-ministerial-regulation-prescribing-criteria-and-procedures-in-building-energy-conservation-bec-b.e.-2563.pdf | 2020 |
| N10 | APEC EGNRET: Thailand's Energy Efficiency Policies (EEP 2024 draft −36 % EI by 2037) | https://www.egnret.ewg.apec.org/Upload/2025052217317588b4881.pdf | 2025-05 |
| N11 | Thailand LT-LEDS (Revised), UNFCCC | https://unfccc.int/sites/default/files/resource/Thailand%20LT-LEDS%20%28Revised%20Version%29_08Nov2022.pdf | 2022-11-08 |
| N12 | IGES slides: Climate Change Mitigation & AIM in Thailand (SIIT, Thammasat) | https://www.iges.or.jp/sites/default/files/inline-files/2-4_Bundit_AIM%20_%20Thailand%2012Nov2022.pdf | 2022-11 |
| N13 | IEA, Thailand's Clean Electricity Transition | https://iea.blob.core.windows.net/assets/dd5b10b2-b655-4c7d-8c09-d3d7efe6bd50/ThailandsCleanElectricityTransition.pdf | 2023-08-08 |
| N14 | Nation Thailand — draft PDP 2026 consultation | https://www.nationthailand.com/sustaination/40070547 | 2026-09-02 |
| N15 | EPPO open data (CKAN) — tables 11_26…11_83 | https://www.eppo.go.th (data portal) | accessed 2026-09-25 |
| N16 | SEI — Thailand bolsters energy resilience using SEI tools | https://www.sei.org/features/thailand-energy-resilience-net-zero/ | 2024 |
| N17 | Thai-German Cooperation — GIZ-EPPO CoP on data acquisition for energy modelling | https://www.thai-german-cooperation.info/news/giz-eppo-strengthening-thailands-energy-planning-via-cop-on-data-acquisition-for-energy-modelling/ | 2025-11 |
| N18 | IEA, Thailand Power System Flexibility Study | https://iea.blob.core.windows.net/assets/ba95b0f3-ec1d-42d3-8288-78438dafad03/ThailandPowerSystemFlexibilityStudy.pdf | 2021 |
| N19 | Bunnak, P. — Thai Power System hourly generation/demand 2023–2024 (from EGAT website), Zenodo, CC-BY-4.0 | https://zenodo.org/records/17109911 | 2025-09-13 |
| N20 | EGAT — REFC & DRCC opening, DR pilot 50 MW, MEA/PEA as aggregators | https://www.egat.co.th/home/en/20230824e/ | 2023-08-24 |
| N21 | NREL/TP-7A40-78780 — BESS technical standards for Thailand (for ERC) | https://docs.nrel.gov/docs/fy21osti/78780.pdf | 2021-01 |
| N22 | DEDE data catalogue — electricity by economic sector | https://pei.dede.go.th/ | accessed 2026-09-25 |
| N23 | PEA Sustainability Report 2024 (distribution loss 5.03 %) | https://www.pea.co.th | 2025 |
| N24 | MEA electricity sales report Dec 2565 (loss 2.13 %) | https://www.mea.or.th | 2023 |
| N25 | PEA Electricity Tariffs (May 2023, EN) | https://www.pea.co.th/sites/default/files/documents/tariff/EN_Electricity_Tariffs_May_2023.pdf | 2023 |
| N26 | NSTDA — Cabinet approves establishment of ENTEC | https://www.nstda.or.th/en/news/news-years-2020/cabinet-greenlights-an-establish-of-national-energy-technology-entec.html | 2020-06 |
| N27 | TDRI — energy policy, stability and structural transition | https://tdri.or.th/2026/04/energy-policy-stability-structural-transition/ | 2026-04 |
| N28 | JGSEE — Energy and Environmental Policy Laboratory | https://www.jgsee.kmutt.ac.th/v3/eepl/ | accessed 2026-09-26 |
| N29 | Agora Energiewende & Chula ERI — Thailand's Natural Gas Crossroads | https://www.agora-energiewende.org/fileadmin/Partnerpublikationen/2025/Thailands-Natural-Gas-Crossroads-Report.pdf | 2025 |
| N30 | Royal Decree establishing TGO B.E. 2550 (FAOLEX) | https://faolex.fao.org/docs/pdf/tha100209.pdf | 2007 |
| N31 | TGO — T-VER overview | https://tver.tgo.or.th/en/about-us/en-overview | accessed 2026-09-26 |
| N32 | USAID Clean Power Asia final report (implementer archive) | https://www.abtglobal.com/files/insights/reports/2021/cpa-finalreport-june2021-smvert.pdf | 2021-06 |
| N33 | NREL — Greater Mekong grid integration training (NREL/PR-5R00-85265) | https://docs.nrel.gov/docs/fy23osti/85265.pdf | 2023-02 |
| N34 | ERIA — Energy Outlook & Saving Potential East Asia 2023, Ch.16 Thailand | https://www.eria.org/uploads/media/Books/2023-Energy-Outlook/22_Ch.16-Thailand.pdf | 2023 |
| N35 | JICA Thailand Office — Survey on Effective Energy Conservation Measures of Commercial Buildings in Bangkok, Final Report | https://openjicareport.jica.go.jp/pdf/1000057590_02.pdf | 2020-03-13 |
| N36 | IRENA — Renewable Energy Outlook: Thailand | https://www.irena.org/publications/2017/Nov/Renewable-Energy-Outlook-Thailand | 2017-11 |

**Dropped from earlier drafts (not re-verifiable in time):** IEA *Energy and AI* SE-Asia doubling figure; AEO8 nuclear GW figures (IEEJ citation); NREL–Chula DPV utility-impact study (OSTI page unavailable); GEIDCO 2020 outlook; CSG Lancang-Mekong interview figures; Tsinghua items; CHEAA China→Thailand AC export growth %. The previously "summary-level" World Bank loss figure (7.16 %, 2023) was re-verified directly from the World Bank API and is kept.
