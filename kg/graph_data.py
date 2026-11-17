"""
Knowledge-graph content extracted from the documents in ../corpus.

Every node and relationship carries a `source` property naming the corpus file(s)
the fact was taken from, so each edge in the graph can be traced back to text.

Schema
------
Nodes (all keyed by a unique `id`):
  :Organization (+ :University | :ResearchInstitute | :Company | :Utility | :FundingAgency)
  :Country, :Person, :Project, :Publication, :Site, :Patent, :Technology, :Event

Relationships:
  (Organization)-[:LOCATED_IN]->(Country)
  (FundingAgency)-[:FUNDS {amount, currency, start_year, end_year}]->(Project)
  (Organization)-[:PARTICIPATES_IN {role, contribution}]->(Project)
  (Person)-[:WORKS_ON {role}]->(Project)
  (Person)-[:AFFILIATED_WITH {type, position, start_year, end_year, current}]->(Organization)
  (Person)-[:SUPERVISED {degree, year, status}]->(Person)
  (Person)-[:HOSTED_POSTDOC {start_year, end_year}]->(Person)
  (Person)-[:AUTHORED {position}]->(Publication)
  (Publication)-[:RESULT_OF]->(Project)
  (Publication)-[:CITES {reason}]->(Publication)
  (Publication)-[:ABOUT]->(Technology)
  (Publication)-[:USES_DATA_FROM]->(Site)
  (Publication)-[:PRESENTED_AT]->(Event)
  (Publication)-[:UNDERPINS]->(Patent)
  (Publication)-[:LICENSED_TO]->(Organization)
  (Project)-[:ESTABLISHED]->(Site)
  (Project)-[:FOCUSES_ON]->(Technology)
  (Organization)-[:OPERATES]->(Site)
  (Organization)-[:SUPPLIED_CELLS_TO]->(Site)
  (Person)-[:MANAGES]->(Site)
  (Site)-[:USES_TECHNOLOGY]->(Technology)
  (Site)-[:IMPLEMENTS]->(Patent)
  (Organization)-[:HOLDS]->(Patent)
  (Person)-[:INVENTED]->(Patent)
  (Patent)-[:COVERS]->(Technology)
  (Patent)-[:LICENSED_IN]->(Project)
  (Technology)-[:IS_A]->(Technology)
  (Technology)-[:RELATED_TO]->(Technology)
  (Organization)-[:HOSTED]->(Event)
  (Person)-[:PARTICIPATED_IN {role}]->(Event)
  (Organization)-[:COLLABORATES_WITH {type}]->(Organization)
  (FundingAgency)-[:AWARDED_FELLOWSHIP_TO]->(Person)
"""

# ---------------------------------------------------------------- nodes

COUNTRIES = [
    {"id": "NO", "name": "Norway"},
    {"id": "DE", "name": "Germany"},
    {"id": "IN", "name": "India"},
    {"id": "CA", "name": "Canada"},
    {"id": "BE", "name": "Belgium"},
]

# `kind` becomes an extra label next to :Organization
ORGANIZATIONS = [
    {"id": "HIT", "name": "Halvorsen Institute of Technology", "kind": "University",
     "sector": "public research university", "city": "Trondheim", "country": "NO", "founded": 1962,
     "unit": "Department of Energy Systems / Electrochemical Storage Laboratory",
     "source": "01_halvorsen_institute_of_technology.txt"},
    {"id": "RVU", "name": "Rhine Valley University", "kind": "University",
     "sector": "public university", "city": "Karlsruhe", "country": "DE", "founded": 1957,
     "unit": "Institute for Materials and Recycling",
     "source": "02_rhine_valley_university.txt"},
    {"id": "SPIS", "name": "Southern Peninsula Institute of Science", "kind": "ResearchInstitute",
     "sector": "public research institute", "city": "Chennai", "country": "IN", "founded": 1985,
     "unit": "Centre for Energy Materials",
     "source": "03_southern_peninsula_institute_of_science.txt"},
    {"id": "MRU", "name": "Maple Ridge University", "kind": "University",
     "sector": "public university", "city": "Vancouver", "country": "CA", "founded": 1968,
     "unit": "Faculty of Applied Science / Smart Grid Analytics Group",
     "source": "04_maple_ridge_university.txt"},
    {"id": "LSS", "name": "Lumen Storage Systems", "kind": "Company",
     "sector": "battery manufacturer", "city": "Munich", "country": "DE", "founded": 2014,
     "employees": 320, "source": "05_lumen_storage_systems.txt"},
    {"id": "FJG", "name": "Fjordgrid AS", "kind": "Utility",
     "sector": "regional electricity distribution utility", "city": "Bergen", "country": "NO",
     "source": "06_fjordgrid_as.txt"},
    {"id": "DPC", "name": "Deccan Power Corporation", "kind": "Utility",
     "sector": "state-owned electricity utility", "city": "Hyderabad", "country": "IN",
     "source": "07_deccan_power_corporation.txt"},
    {"id": "PCT", "name": "Pacific Cell Technologies", "kind": "Company",
     "sector": "battery management and dispatch software", "city": "Vancouver", "country": "CA",
     "founded": 2017, "source": "08_pacific_cell_technologies.txt"},
    {"id": "ECEC", "name": "European Clean Energy Council", "kind": "FundingAgency",
     "sector": "funding agency", "city": "Brussels", "country": "BE", "founded": 2010,
     "source": "09_european_clean_energy_council.txt"},
    {"id": "NSEI", "name": "National Science Endowment of India", "kind": "FundingAgency",
     "sector": "government funding body", "city": "New Delhi", "country": "IN",
     "source": "10_national_science_endowment_of_india.txt"},
    {"id": "CIF", "name": "Canadian Innovation Fund", "kind": "FundingAgency",
     "sector": "federal funding programme", "city": "Ottawa", "country": "CA",
     "source": "11_canadian_innovation_fund.txt"},
]

PEOPLE = [
    {"id": "solberg", "name": "Ingrid Solberg", "title": "Dr.", "source": "16_person_ingrid_solberg.txt"},
    {"id": "weber", "name": "Markus Weber", "title": "Dr.", "source": "17_person_markus_weber.txt"},
    {"id": "raghunathan", "name": "Priya Raghunathan", "title": "Dr.", "source": "18_person_priya_raghunathan.txt"},
    {"id": "okafor", "name": "Daniel Okafor", "title": "Dr.", "source": "19_person_daniel_okafor.txt"},
    {"id": "voss", "name": "Elena Voss", "title": "Dr.", "source": "20_person_elena_voss.txt"},
    {"id": "berg", "name": "Tomas Berg", "title": "Dr.", "source": "21_person_tomas_berg.txt"},
    {"id": "novak", "name": "Katarina Novak", "title": "Dr.", "source": "02_rhine_valley_university.txt"},
    {"id": "lindqvist", "name": "Sofia Lindqvist", "title": None, "source": "16_person_ingrid_solberg.txt"},
    {"id": "menon", "name": "Arjun Menon", "title": None, "source": "03_southern_peninsula_institute_of_science.txt"},
    {"id": "liwei", "name": "Li Wei", "title": "Dr.", "source": "04_maple_ridge_university.txt"},
    {"id": "brooks", "name": "Hannah Brooks", "title": "Dr.", "source": "08_pacific_cell_technologies.txt"},
    {"id": "venkatesan", "name": "Rahul Venkatesan", "title": None, "source": "07_deccan_power_corporation.txt"},
]

PROJECTS = [
    {"id": "ALPINE", "name": "ALPINE", "topic": "Sodium-ion storage for Alpine and Nordic grids",
     "start_year": 2021, "end_year": 2025, "source": "12_project_alpine.txt"},
    {"id": "MONSOON", "name": "MONSOON", "topic": "Stationary batteries reliable in hot and humid climates",
     "start_year": 2022, "end_year": 2027, "source": "13_project_monsoon.txt"},
    {"id": "CASCADE", "name": "CASCADE",
     "topic": "Machine learning to forecast renewable generation and schedule battery charging",
     "start_year": 2022, "end_year": 2025, "source": "14_project_cascade.txt"},
    {"id": "RECLAIM", "name": "RECLAIM",
     "topic": "Economical recovery of materials from end-of-life batteries",
     "start_year": 2022, "end_year": 2027, "source": "15_project_reclaim.txt"},
]

PUBLICATIONS = [
    {"id": "P_DEGRADATION", "title": "Sodium-Ion Cell Degradation Under Variable Grid Loads", "year": 2023,
     "venue": "Journal of Energy Storage Engineering", "source": "22_paper_sodium_ion_cell_degradation.txt"},
    {"id": "P_CATHODE", "title": "Sodium-Ion Cathode Stability in Solid-State Electrolytes", "year": 2022,
     "venue": "Advanced Electrochemical Materials", "source": "23_paper_cathode_stability.txt"},
    {"id": "P_THERMAL", "title": "Thermal Management Strategies for Stationary Batteries in Hot Climates",
     "year": 2024, "venue": "International Journal of Thermal Energy Systems",
     "source": "24_paper_thermal_management.txt"},
    {"id": "P_FORECAST", "title": "Probabilistic Load Forecasting with Gradient-Boosted Models", "year": 2023,
     "venue": "Transactions on Smart Grid Analytics", "source": "25_paper_probabilistic_load_forecasting.txt"},
    {"id": "P_HYDROMET", "title": "Hydrometallurgical Recovery of Sodium-Ion Cathode Materials", "year": 2024,
     "venue": "Journal of Sustainable Materials Processing", "source": "26_paper_hydrometallurgical_recovery.txt"},
    {"id": "P_DISPATCH", "title": "Forecast-Aware Dispatch of Grid Batteries", "year": 2025,
     "venue": "Energy Systems Control Letters", "source": "27_paper_forecast_aware_dispatch.txt"},
]

SITES = [
    {"id": "VESTFJORD", "name": "Vestfjord Pilot Site", "location": "near Bergen, Norway", "country": "NO",
     "commissioned": 2024, "capacity": "2 MWh", "chemistry": "sodium-ion",
     "source": "28_vestfjord_pilot_site.txt"},
    {"id": "TIRUVALLUR", "name": "Tiruvallur Test Bed", "location": "near Chennai, India", "country": "IN",
     "commissioned": 2025, "capacity": "1.5 MWh", "chemistry": "sodium-ion",
     "source": "29_tiruvallur_test_bed.txt"},
    {"id": "FRASER", "name": "Fraser Valley Demonstration Site", "location": "British Columbia, Canada",
     "country": "CA", "commissioned": 2024, "capacity": "800 kWh + solar array",
     "chemistry": "lithium iron phosphate", "source": "30_fraser_valley_demonstration_site.txt"},
]

PATENTS = [
    {"id": "LSS-PAT-2020-114", "title": "Layered Sodium-Ion Cell with Composite Electrolyte Interface",
     "filed": 2020, "granted": 2022, "source": "32_patent_lss_pat_2020_114.txt"},
]

TECHNOLOGIES = [
    {"id": "T_RECHARGEABLE", "name": "Rechargeable Battery", "source": "33_technology_sodium_ion_battery.txt"},
    {"id": "T_SODIUM_ION", "name": "Sodium-Ion Battery", "source": "33_technology_sodium_ion_battery.txt"},
    {"id": "T_LITHIUM_ION", "name": "Lithium-Ion Battery", "source": "33_technology_sodium_ion_battery.txt"},
    {"id": "T_LFP", "name": "Lithium Iron Phosphate Battery", "source": "33_technology_sodium_ion_battery.txt"},
    {"id": "T_THERMAL", "name": "Thermal Management", "source": "34_technology_thermal_management.txt"},
    {"id": "T_FORECAST", "name": "Load Forecasting", "source": "35_technology_load_forecasting.txt"},
]

EVENTS = [
    {"id": "NSS2023", "name": "Nordic Storage Symposium 2023", "city": "Trondheim", "country": "NO",
     "start_date": "2023-06-14", "end_date": "2023-06-16", "participants": 200,
     "source": "31_nordic_storage_symposium_2023.txt"},
    {"id": "ABSW2024", "name": "Asian Battery Safety Workshop 2024", "year": 2024,
     "source": "03_southern_peninsula_institute_of_science.txt"},
]

# ---------------------------------------------------------------- relationships
# Each entry: (from_label, from_id, REL_TYPE, to_label, to_id, {props})

def _r(fl, fid, rel, tl, tid, source, **props):
    props["source"] = source
    return (fl, fid, rel, tl, tid, props)


O, PE, PR, PU, S, PA, T, E, C = (
    "Organization", "Person", "Project", "Publication", "Site", "Patent", "Technology", "Event", "Country")

RELATIONSHIPS = []
add = RELATIONSHIPS.append

# --- organization locations
for o in ORGANIZATIONS:
    add(_r(O, o["id"], "LOCATED_IN", C, o["country"], o["source"]))
for s in SITES:
    add(_r(S, s["id"], "LOCATED_IN", C, s["country"], s["source"]))

# --- funding (amounts as stated in the agency and project documents)
add(_r(O, "ECEC", "FUNDS", PR, "ALPINE", "09_european_clean_energy_council.txt; 12_project_alpine.txt",
       amount=4_200_000, currency="EUR", start_year=2021, end_year=2025))
add(_r(O, "ECEC", "FUNDS", PR, "RECLAIM", "09_european_clean_energy_council.txt; 15_project_reclaim.txt",
       amount=3_100_000, currency="EUR", start_year=2022, end_year=2027))
add(_r(O, "NSEI", "FUNDS", PR, "MONSOON", "10_national_science_endowment_of_india.txt",
       amount=380_000_000, currency="INR", start_year=2022, end_year=2027))
add(_r(O, "CIF", "FUNDS", PR, "CASCADE", "11_canadian_innovation_fund.txt; 14_project_cascade.txt",
       amount=2_800_000, currency="CAD", start_year=2022, end_year=2025))

# --- consortium membership and roles
add(_r(O, "HIT", "PARTICIPATES_IN", PR, "ALPINE", "12_project_alpine.txt",
       role="coordinator", contribution="coordinated the consortium"))
add(_r(O, "RVU", "PARTICIPATES_IN", PR, "ALPINE", "12_project_alpine.txt; 02_rhine_valley_university.txt",
       role="materials", contribution="developed solid-state electrolytes"))
add(_r(O, "LSS", "PARTICIPATES_IN", PR, "ALPINE", "12_project_alpine.txt; 05_lumen_storage_systems.txt",
       role="manufacturing", contribution="manufactured the cells"))
add(_r(O, "FJG", "PARTICIPATES_IN", PR, "ALPINE", "12_project_alpine.txt; 06_fjordgrid_as.txt",
       role="pilot operation", contribution="operated the pilot"))

add(_r(O, "SPIS", "PARTICIPATES_IN", PR, "MONSOON", "13_project_monsoon.txt",
       role="coordinator", contribution="leads the project"))
add(_r(O, "DPC", "PARTICIPATES_IN", PR, "MONSOON", "13_project_monsoon.txt; 07_deccan_power_corporation.txt",
       role="pilot operation", contribution="co-operates test bed; grid connection and operational data"))
add(_r(O, "MRU", "PARTICIPATES_IN", PR, "MONSOON", "13_project_monsoon.txt; 10_national_science_endowment_of_india.txt",
       role="modelling", contribution="contributes modelling expertise (foreign partner)"))

add(_r(O, "MRU", "PARTICIPATES_IN", PR, "CASCADE", "14_project_cascade.txt",
       role="coordinator", contribution="led the project"))
add(_r(O, "PCT", "PARTICIPATES_IN", PR, "CASCADE", "14_project_cascade.txt; 08_pacific_cell_technologies.txt",
       role="software integration", contribution="integrated the algorithms into commercial software"))
add(_r(O, "HIT", "PARTICIPATES_IN", PR, "CASCADE", "14_project_cascade.txt; 11_canadian_innovation_fund.txt",
       role="research partner", contribution="provided battery degradation models (international partner)"))

add(_r(O, "RVU", "PARTICIPATES_IN", PR, "RECLAIM", "15_project_reclaim.txt",
       role="coordinator", contribution="leads the work"))
add(_r(O, "LSS", "PARTICIPATES_IN", PR, "RECLAIM", "15_project_reclaim.txt",
       role="industrial partner", contribution="supplies production scrap and used cells"))

# --- people on projects
add(_r(PE, "solberg", "WORKS_ON", PR, "ALPINE", "12_project_alpine.txt", role="principal investigator"))
add(_r(PE, "novak", "WORKS_ON", PR, "ALPINE", "02_rhine_valley_university.txt", role="solid-state electrolyte researcher"))
add(_r(PE, "weber", "WORKS_ON", PR, "ALPINE", "17_person_markus_weber.txt", role="senior contributor"))
add(_r(PE, "voss", "WORKS_ON", PR, "ALPINE", "20_person_elena_voss.txt", role="Lumen representative"))
add(_r(PE, "berg", "WORKS_ON", PR, "ALPINE", "21_person_tomas_berg.txt", role="Fjordgrid representative"))
add(_r(PE, "raghunathan", "WORKS_ON", PR, "MONSOON", "13_project_monsoon.txt", role="principal investigator"))
add(_r(PE, "venkatesan", "WORKS_ON", PR, "MONSOON", "13_project_monsoon.txt", role="Deccan Power representative"))
add(_r(PE, "menon", "WORKS_ON", PR, "MONSOON", "13_project_monsoon.txt", role="doctoral student"))
add(_r(PE, "okafor", "WORKS_ON", PR, "MONSOON", "19_person_daniel_okafor.txt", role="collaborator"))
add(_r(PE, "okafor", "WORKS_ON", PR, "CASCADE", "14_project_cascade.txt", role="principal investigator"))
add(_r(PE, "weber", "WORKS_ON", PR, "RECLAIM", "15_project_reclaim.txt", role="principal investigator"))
add(_r(PE, "voss", "WORKS_ON", PR, "RECLAIM", "20_person_elena_voss.txt", role="Lumen representative"))

# --- affiliations (type: employment | study | visiting)
add(_r(PE, "solberg", "AFFILIATED_WITH", O, "RVU", "16_person_ingrid_solberg.txt",
       type="study", position="doctoral student", end_year=2005, current=False))
add(_r(PE, "solberg", "AFFILIATED_WITH", O, "HIT", "16_person_ingrid_solberg.txt",
       type="employment", position="professor; director, Electrochemical Storage Laboratory",
       start_year=2008, current=True))
add(_r(PE, "weber", "AFFILIATED_WITH", O, "RVU", "17_person_markus_weber.txt",
       type="employment", position="professor; head, Institute for Materials and Recycling", current=True))
add(_r(PE, "voss", "AFFILIATED_WITH", O, "RVU", "20_person_elena_voss.txt",
       type="employment", position="postdoctoral researcher", start_year=2015, end_year=2019, current=False))
add(_r(PE, "voss", "AFFILIATED_WITH", O, "LSS", "20_person_elena_voss.txt",
       type="employment", position="senior engineer, CTO since 2022", start_year=2019, current=True))
add(_r(PE, "novak", "AFFILIATED_WITH", O, "RVU", "02_rhine_valley_university.txt; 32_patent_lss_pat_2020_114.txt",
       type="employment", position="senior researcher", current=True))
add(_r(PE, "berg", "AFFILIATED_WITH", O, "HIT", "21_person_tomas_berg.txt",
       type="study", position="doctoral student", end_year=2016, current=False))
add(_r(PE, "berg", "AFFILIATED_WITH", O, "FJG", "21_person_tomas_berg.txt",
       type="employment", position="lead storage engineer", start_year=2016, current=True))
add(_r(PE, "lindqvist", "AFFILIATED_WITH", O, "HIT", "16_person_ingrid_solberg.txt; 27_paper_forecast_aware_dispatch.txt",
       type="study", position="doctoral student", current=True))
add(_r(PE, "raghunathan", "AFFILIATED_WITH", O, "SPIS", "18_person_priya_raghunathan.txt",
       type="employment", position="associate professor; head, Centre for Energy Materials", current=True))
add(_r(PE, "raghunathan", "AFFILIATED_WITH", O, "MRU", "18_person_priya_raghunathan.txt",
       type="visiting", position="visiting scholar (sabbatical)", start_year=2019, end_year=2019, current=False))
add(_r(PE, "menon", "AFFILIATED_WITH", O, "SPIS", "03_southern_peninsula_institute_of_science.txt",
       type="study", position="doctoral student (NSEI fellow)", current=True))
add(_r(PE, "okafor", "AFFILIATED_WITH", O, "MRU", "19_person_daniel_okafor.txt",
       type="employment", position="professor; lead, Smart Grid Analytics Group", current=True))
add(_r(PE, "liwei", "AFFILIATED_WITH", O, "MRU", "04_maple_ridge_university.txt",
       type="employment", position="research scientist", current=True))
add(_r(PE, "brooks", "AFFILIATED_WITH", O, "MRU", "04_maple_ridge_university.txt; 08_pacific_cell_technologies.txt",
       type="study", position="doctoral student", end_year=2018, current=False))
add(_r(PE, "brooks", "AFFILIATED_WITH", O, "PCT", "04_maple_ridge_university.txt; 08_pacific_cell_technologies.txt",
       type="employment", position="head of software division", start_year=2018, current=True))
add(_r(PE, "venkatesan", "AFFILIATED_WITH", O, "DPC", "07_deccan_power_corporation.txt",
       type="employment", position="project manager", current=True))

# --- supervision / mentoring
add(_r(PE, "weber", "SUPERVISED", PE, "solberg", "16_person_ingrid_solberg.txt; 17_person_markus_weber.txt",
       degree="doctorate", year=2005, status="completed"))
add(_r(PE, "solberg", "SUPERVISED", PE, "berg", "16_person_ingrid_solberg.txt; 21_person_tomas_berg.txt",
       degree="doctorate", year=2016, status="completed"))
add(_r(PE, "solberg", "SUPERVISED", PE, "lindqvist", "16_person_ingrid_solberg.txt",
       degree="doctorate", status="ongoing"))
add(_r(PE, "okafor", "SUPERVISED", PE, "brooks", "19_person_daniel_okafor.txt; 08_pacific_cell_technologies.txt",
       degree="doctorate", year=2018, status="completed"))
add(_r(PE, "raghunathan", "SUPERVISED", PE, "menon", "18_person_priya_raghunathan.txt",
       degree="doctorate", status="ongoing"))
add(_r(PE, "weber", "HOSTED_POSTDOC", PE, "voss", "17_person_markus_weber.txt; 20_person_elena_voss.txt",
       start_year=2015, end_year=2019))

# --- authorship (position = author order)
for pub, authors in {
    "P_DEGRADATION": ["solberg", "lindqvist", "berg"],
    "P_CATHODE": ["novak", "solberg", "voss"],
    "P_THERMAL": ["raghunathan", "menon", "okafor"],
    "P_FORECAST": ["okafor", "liwei", "brooks"],
    "P_HYDROMET": ["weber", "novak"],
    "P_DISPATCH": ["brooks", "lindqvist", "okafor"],
}.items():
    src = next(p["source"] for p in PUBLICATIONS if p["id"] == pub)
    for i, a in enumerate(authors, start=1):
        add(_r(PE, a, "AUTHORED", PU, pub, src, position=i))

# --- publication context
add(_r(PU, "P_DEGRADATION", "RESULT_OF", PR, "ALPINE", "22_paper_sodium_ion_cell_degradation.txt"))
add(_r(PU, "P_CATHODE", "RESULT_OF", PR, "ALPINE", "23_paper_cathode_stability.txt"))
add(_r(PU, "P_THERMAL", "RESULT_OF", PR, "MONSOON", "24_paper_thermal_management.txt"))
add(_r(PU, "P_FORECAST", "RESULT_OF", PR, "CASCADE", "25_paper_probabilistic_load_forecasting.txt"))
add(_r(PU, "P_HYDROMET", "RESULT_OF", PR, "RECLAIM", "26_paper_hydrometallurgical_recovery.txt"))
add(_r(PU, "P_DISPATCH", "RESULT_OF", PR, "CASCADE", "27_paper_forecast_aware_dispatch.txt"))

add(_r(PU, "P_DEGRADATION", "CITES", PU, "P_CATHODE", "22_paper_sodium_ion_cell_degradation.txt",
       reason="baseline material properties of the cells"))
add(_r(PU, "P_THERMAL", "CITES", PU, "P_DEGRADATION", "24_paper_thermal_management.txt",
       reason="ageing model"))
add(_r(PU, "P_HYDROMET", "CITES", PU, "P_CATHODE", "26_paper_hydrometallurgical_recovery.txt",
       reason="choice of cathode chemistry"))
add(_r(PU, "P_DISPATCH", "CITES", PU, "P_FORECAST", "27_paper_forecast_aware_dispatch.txt",
       reason="forecasting method"))
add(_r(PU, "P_DISPATCH", "CITES", PU, "P_DEGRADATION", "27_paper_forecast_aware_dispatch.txt",
       reason="degradation model"))

add(_r(PU, "P_DEGRADATION", "ABOUT", T, "T_SODIUM_ION", "22_paper_sodium_ion_cell_degradation.txt"))
add(_r(PU, "P_CATHODE", "ABOUT", T, "T_SODIUM_ION", "23_paper_cathode_stability.txt"))
add(_r(PU, "P_THERMAL", "ABOUT", T, "T_THERMAL", "24_paper_thermal_management.txt"))
add(_r(PU, "P_THERMAL", "ABOUT", T, "T_SODIUM_ION", "24_paper_thermal_management.txt"))
add(_r(PU, "P_FORECAST", "ABOUT", T, "T_FORECAST", "25_paper_probabilistic_load_forecasting.txt"))
add(_r(PU, "P_HYDROMET", "ABOUT", T, "T_SODIUM_ION", "26_paper_hydrometallurgical_recovery.txt"))
add(_r(PU, "P_DISPATCH", "ABOUT", T, "T_FORECAST", "27_paper_forecast_aware_dispatch.txt"))

add(_r(PU, "P_DEGRADATION", "USES_DATA_FROM", S, "VESTFJORD", "22_paper_sodium_ion_cell_degradation.txt; 28_vestfjord_pilot_site.txt"))
add(_r(PU, "P_THERMAL", "USES_DATA_FROM", S, "TIRUVALLUR", "24_paper_thermal_management.txt; 29_tiruvallur_test_bed.txt"))
add(_r(PU, "P_FORECAST", "USES_DATA_FROM", S, "FRASER", "25_paper_probabilistic_load_forecasting.txt; 30_fraser_valley_demonstration_site.txt"))

add(_r(PU, "P_DEGRADATION", "PRESENTED_AT", E, "NSS2023", "22_paper_sodium_ion_cell_degradation.txt"))
add(_r(PU, "P_FORECAST", "PRESENTED_AT", E, "NSS2023", "25_paper_probabilistic_load_forecasting.txt"))

add(_r(PU, "P_CATHODE", "UNDERPINS", PA, "LSS-PAT-2020-114", "23_paper_cathode_stability.txt; 32_patent_lss_pat_2020_114.txt"))
add(_r(PU, "P_FORECAST", "LICENSED_TO", O, "PCT", "25_paper_probabilistic_load_forecasting.txt; 08_pacific_cell_technologies.txt"))

# --- projects, sites, technology
add(_r(PR, "ALPINE", "ESTABLISHED", S, "VESTFJORD", "28_vestfjord_pilot_site.txt; 12_project_alpine.txt"))
add(_r(PR, "MONSOON", "ESTABLISHED", S, "TIRUVALLUR", "29_tiruvallur_test_bed.txt; 13_project_monsoon.txt"))
add(_r(PR, "CASCADE", "ESTABLISHED", S, "FRASER", "30_fraser_valley_demonstration_site.txt; 11_canadian_innovation_fund.txt"))

add(_r(PR, "ALPINE", "FOCUSES_ON", T, "T_SODIUM_ION", "12_project_alpine.txt; 33_technology_sodium_ion_battery.txt"))
add(_r(PR, "MONSOON", "FOCUSES_ON", T, "T_SODIUM_ION", "33_technology_sodium_ion_battery.txt"))
add(_r(PR, "MONSOON", "FOCUSES_ON", T, "T_THERMAL", "34_technology_thermal_management.txt"))
add(_r(PR, "CASCADE", "FOCUSES_ON", T, "T_FORECAST", "35_technology_load_forecasting.txt"))
add(_r(PR, "RECLAIM", "FOCUSES_ON", T, "T_SODIUM_ION", "33_technology_sodium_ion_battery.txt; 15_project_reclaim.txt"))
add(_r(PR, "RECLAIM", "FOCUSES_ON", T, "T_LITHIUM_ION", "15_project_reclaim.txt"))

add(_r(O, "HIT", "OPERATES", S, "VESTFJORD", "28_vestfjord_pilot_site.txt; 01_halvorsen_institute_of_technology.txt"))
add(_r(O, "FJG", "OPERATES", S, "VESTFJORD", "28_vestfjord_pilot_site.txt; 06_fjordgrid_as.txt"))
add(_r(O, "SPIS", "OPERATES", S, "TIRUVALLUR", "29_tiruvallur_test_bed.txt; 03_southern_peninsula_institute_of_science.txt"))
add(_r(O, "DPC", "OPERATES", S, "TIRUVALLUR", "29_tiruvallur_test_bed.txt; 07_deccan_power_corporation.txt"))
add(_r(O, "MRU", "OPERATES", S, "FRASER", "30_fraser_valley_demonstration_site.txt; 04_maple_ridge_university.txt"))
add(_r(O, "PCT", "OPERATES", S, "FRASER", "30_fraser_valley_demonstration_site.txt; 08_pacific_cell_technologies.txt"))

add(_r(O, "LSS", "SUPPLIED_CELLS_TO", S, "VESTFJORD", "05_lumen_storage_systems.txt; 28_vestfjord_pilot_site.txt"))
add(_r(O, "LSS", "SUPPLIED_CELLS_TO", S, "TIRUVALLUR", "05_lumen_storage_systems.txt; 29_tiruvallur_test_bed.txt"))

add(_r(PE, "berg", "MANAGES", S, "VESTFJORD", "28_vestfjord_pilot_site.txt; 21_person_tomas_berg.txt"))
add(_r(PE, "venkatesan", "MANAGES", S, "TIRUVALLUR", "29_tiruvallur_test_bed.txt"))

add(_r(S, "VESTFJORD", "USES_TECHNOLOGY", T, "T_SODIUM_ION", "28_vestfjord_pilot_site.txt"))
add(_r(S, "TIRUVALLUR", "USES_TECHNOLOGY", T, "T_SODIUM_ION", "29_tiruvallur_test_bed.txt"))
add(_r(S, "TIRUVALLUR", "USES_TECHNOLOGY", T, "T_THERMAL", "29_tiruvallur_test_bed.txt; 34_technology_thermal_management.txt"))
add(_r(S, "FRASER", "USES_TECHNOLOGY", T, "T_LFP", "30_fraser_valley_demonstration_site.txt"))
add(_r(S, "FRASER", "USES_TECHNOLOGY", T, "T_FORECAST", "30_fraser_valley_demonstration_site.txt; 35_technology_load_forecasting.txt"))

add(_r(S, "VESTFJORD", "IMPLEMENTS", PA, "LSS-PAT-2020-114", "28_vestfjord_pilot_site.txt; 32_patent_lss_pat_2020_114.txt"))
add(_r(S, "TIRUVALLUR", "IMPLEMENTS", PA, "LSS-PAT-2020-114", "32_patent_lss_pat_2020_114.txt"))

# --- patent
add(_r(O, "LSS", "HOLDS", PA, "LSS-PAT-2020-114", "32_patent_lss_pat_2020_114.txt; 05_lumen_storage_systems.txt"))
add(_r(PE, "voss", "INVENTED", PA, "LSS-PAT-2020-114", "32_patent_lss_pat_2020_114.txt; 20_person_elena_voss.txt"))
add(_r(PE, "novak", "INVENTED", PA, "LSS-PAT-2020-114", "32_patent_lss_pat_2020_114.txt; 20_person_elena_voss.txt"))
add(_r(PA, "LSS-PAT-2020-114", "COVERS", T, "T_SODIUM_ION", "32_patent_lss_pat_2020_114.txt"))
add(_r(PA, "LSS-PAT-2020-114", "LICENSED_IN", PR, "ALPINE", "32_patent_lss_pat_2020_114.txt"))

# --- technology taxonomy
add(_r(T, "T_SODIUM_ION", "IS_A", T, "T_RECHARGEABLE", "33_technology_sodium_ion_battery.txt"))
add(_r(T, "T_LITHIUM_ION", "IS_A", T, "T_RECHARGEABLE", "33_technology_sodium_ion_battery.txt"))
add(_r(T, "T_LFP", "IS_A", T, "T_RECHARGEABLE", "33_technology_sodium_ion_battery.txt"))
add(_r(T, "T_THERMAL", "RELATED_TO", T, "T_RECHARGEABLE", "34_technology_thermal_management.txt"))
add(_r(T, "T_FORECAST", "RELATED_TO", T, "T_RECHARGEABLE", "35_technology_load_forecasting.txt"))

# --- events
add(_r(O, "HIT", "HOSTED", E, "NSS2023", "31_nordic_storage_symposium_2023.txt; 01_halvorsen_institute_of_technology.txt"))
add(_r(O, "SPIS", "HOSTED", E, "ABSW2024", "03_southern_peninsula_institute_of_science.txt"))
add(_r(PE, "solberg", "PARTICIPATED_IN", E, "NSS2023", "31_nordic_storage_symposium_2023.txt", role="keynote speaker"))
add(_r(PE, "voss", "PARTICIPATED_IN", E, "NSS2023", "31_nordic_storage_symposium_2023.txt", role="industry panelist"))
add(_r(PE, "okafor", "PARTICIPATED_IN", E, "NSS2023", "31_nordic_storage_symposium_2023.txt", role="presenter"))
add(_r(PE, "weber", "PARTICIPATED_IN", E, "NSS2023", "31_nordic_storage_symposium_2023.txt", role="invited guest"))

# --- bilateral organisational agreements (outside projects)
add(_r(O, "HIT", "COLLABORATES_WITH", O, "FJG", "01_halvorsen_institute_of_technology.txt",
       type="long-standing industrial partnership"))
add(_r(O, "RVU", "COLLABORATES_WITH", O, "LSS", "02_rhine_valley_university.txt",
       type="collaboration agreement"))
add(_r(O, "SPIS", "COLLABORATES_WITH", O, "MRU", "03_southern_peninsula_institute_of_science.txt",
       type="exchange agreement"))
add(_r(O, "PCT", "COLLABORATES_WITH", O, "HIT", "08_pacific_cell_technologies.txt",
       type="forecast-aware control for sodium-ion systems"))
add(_r(O, "PCT", "COLLABORATES_WITH", O, "MRU", "08_pacific_cell_technologies.txt",
       type="licenses forecasting algorithm"))

add(_r(O, "NSEI", "AWARDED_FELLOWSHIP_TO", PE, "menon", "10_national_science_endowment_of_india.txt"))
