# %%
from pathlib import Path
import pandas as pd
import json
# %%
DATA_ENDPOINT = "https://d3lsdszfx9jqxt.cloudfront.net/data-query/"
DEVIATION_THRESHOLD = 0.1
GROUNDTRUTH_DIR = Path("../public/groundtruth/csv_records")

GROUNDTRUTH_FILES = {
  "12472378904908_241206074018": {
    "desc": "All counties, 2022, Ag and Non-Ag. No other filters",
    "drop_cols": ["ADJUVANT", "YEAR", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "12472378904908_241206074507":{
    "desc": "All counties, 2022, Non-Ag only. No other filters",
    "drop_cols": ["ADJUVANT", "YEAR", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "12495048391211_241206085403":{
    "desc": "All counties, 2020, Ag only. No other filters",
    "drop_cols": ["ADJUVANT", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "12472378904908_241206074829": {
    "desc": "Sacramento Acounty, 2020. Ag only, Alfalfa site.",
    "drop_cols": ["ADJUVANT", "YEAR"],
    "group_cols": ["COMTRS"]
  },
  "12489387854613_241206083511": {
    "desc": "Sacramento Acounty, 2020. Ag only, Mineral oil AI.",
    "drop_cols": ["ADJUVANT"],
  }
}

GEO_ENDPOINTS = {
  "tract":"6744f2bbdb91810008024956",
  "school_district": "674518c90507860008cda24f",
  "county": "674513830507860008cda249",
  "section": "67451c010507860008cda252",
  "township": "6744f63adb91810008024959",
  "zip":"674516220507860008cda24c",
}

TIMESERIES_ENDPOINTS = {
  "active_ingredient": "6745e18280f7590008e360e0"
}

COUNTY_DEFAULT_TEST_CONFIG = {
    "endpoint": GEO_ENDPOINTS["county"],
    "filters": {  "start": "2022-01", "end": "2022-12" },
    "type": "table_equality",
    "sort_by": "Area Name",
    "add_row_id": True,
    "keep_cols": ["ROW_ID", "lbs_chm_used", "lbs_prd_used"],
    "left_on": ["ROW_ID"],
    "right_on": ["COUNTY_CODE"],
    "comparison_cols": [
      ("lbs_chm_used", "SUM_LBS_CHEMICAL"),
      ("lbs_prd_used", "SUM_LBS_PRODUCT")
    ],
    "threshold": DEVIATION_THRESHOLD
}

TEST_CONFIG = [
  # {
  #   **COUNTY_DEFAULT_TEST_CONFIG,
  #   "name": "2022 County Totals",
  #   "groundtruth": "12472378904908_241206074018",
  # },
  # {
  #   **COUNTY_DEFAULT_TEST_CONFIG,
  #   "name": "2022 County Non-ag totals",
  #   "groundtruth": "12472378904908_241206074507",
  #   "filters": {
  #     **COUNTY_DEFAULT_TEST_CONFIG["filters"],
  #     "usetype": "NON-AG"
  #   }
  # },
  # {
  #   **COUNTY_DEFAULT_TEST_CONFIG,
  #   "name": "2020 County Ag totals",
  #   "groundtruth": "12495048391211_241206085403",
  #   "filters": {
  #     "usetype": "AG",
  #     "start": "2020-01",
  #     "end": "2020-12"
  #   }
  # },
  {
    "name": "Tract Sum Total",
    "groundtruth": "12495048391211_241206085403",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["tract"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG"
    },
    "comparison_cols": [
      ("lbs_chm_used", "SUM_LBS_CHEMICAL"),
      ("lbs_prd_used", "SUM_LBS_PRODUCT")
    ]
  },
  {
    "name": "School Districts Sum Total",
    "groundtruth": "12495048391211_241206085403",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["school_district"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG"
    },
    "comparison_cols": [
      ("lbs_chm_used", "SUM_LBS_CHEMICAL"),
      ("lbs_prd_used", "SUM_LBS_PRODUCT")
    ]
  },
  {
    "name": "Zip Sum Total",
    "groundtruth": "12495048391211_241206085403",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["zip"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG"
    },
    "comparison_cols": [
      ("lbs_chm_used", "SUM_LBS_CHEMICAL"),
      ("lbs_prd_used", "SUM_LBS_PRODUCT")
    ]
  },
  {
    "name": "Townships Total",
    "groundtruth": "12495048391211_241206085403",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["township"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG"
    },
    "comparison_cols": [
      ("lbs_chm_used", "SUM_LBS_CHEMICAL"),
      ("lbs_prd_used", "SUM_LBS_PRODUCT")
    ]
  },
  {
    "name": "Section Total",
    "groundtruth": "12495048391211_241206085403",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["section"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG"
    },
    "comparison_cols": [
      ("lbs_chm_used", "SUM_LBS_CHEMICAL"),
      ("lbs_prd_used", "SUM_LBS_PRODUCT")
    ]
  },
]

class GroundTruthDataParser():
  dfs = {}
  groundtruth_config = {}

  def __init__(self, groundtruth_config):
    self.groundtruth_config = groundtruth_config
    for key in groundtruth_config:
      config = groundtruth_config[key]
      df = pd.read_csv(Path.joinpath(GROUNDTRUTH_DIR, key + '.txt'), sep="\t")\
        .replace("N/A", 0)
      if "drop_cols" in config:
        df = df.drop(columns=config["drop_cols"])
      if "group_cols" in config:
        df = df.groupby(config["group_cols"]).sum().reset_index()
      self.dfs[key] = df

class TestRunner():
  results: {} = {}

  def __init__(self, test_config, groundtruth):
    self.test_config = test_config
    self.groundtruth = groundtruth

  def get_test_data(self,config):
    test_data_url = DATA_ENDPOINT + config["endpoint"]
    if config["filters"]:
      for idx, key in enumerate(config["filters"]):
        test_data_url += "?" if idx == 0 else "&"
        test_data_url += f"{key}={config['filters'][key]}"
    return pd.read_json(test_data_url)
  
  def run_table_equality_test(self,config):
    groundtruth_data = self.groundtruth.dfs[config["groundtruth"]]
    test_data = self.get_test_data(config)
    if "sort_by" in config:
      test_data = test_data.sort_values(config["sort_by"])
    if config.get("add_row_id") == True:
      test_data = test_data.reset_index(names=['ROW_ID'])
    if config.get("keep_cols"):
      test_data = test_data[config['keep_cols']]
    
    merged = test_data.merge(groundtruth_data, left_on=config['left_on'], right_on=config['right_on'])
    for cols in config["comparison_cols"]:
      merged[cols[0] + "_comparison"] = (merged[cols[0]] / merged[cols[1]]) / merged[cols[0]]
      ave_diff = merged[cols[0] + "_comparison"].mean()
      assert ave_diff < config["threshold"]

      print("\nPASSED", f"{round(ave_diff*100, 3)}% average difference\n", config["name"], config["type"], cols)
      self.results[f"{config["name"]} :: {cols[1]}"] = round(ave_diff*100, 3)

  def run_sum_total_test(self, config):
    groundtruth_data = self.groundtruth.dfs[config["groundtruth"]]
    test_data = self.get_test_data(config)
    for cols in config["comparison_cols"]:
      [sum_test, sum_ground] = [test_data[cols[0]].sum(), groundtruth_data[cols[1]].sum()]
      diff = (sum_test - sum_ground) / sum_test
      assert abs(diff) < config["threshold"]
      print("\nPASSED", f"{round(diff*100, 3)}% average difference\n", config["name"], config["type"], cols)
      self.results[f"{config["name"]} {cols[1]}"] = round(diff*100, 3)

  def run_tests(self):
    for test in self.test_config:
      if test['type'] == 'table_equality':
        self.run_table_equality_test(test)
      if test['type'] == "sum_total":
        self.run_sum_total_test(test)

if __name__ == "__main__":
  groundtruth = GroundTruthDataParser(GROUNDTRUTH_FILES)
  test_runner =  TestRunner(TEST_CONFIG, groundtruth)
  test_runner.run_tests()
  with open("test_results.json", "w") as f:
    json.dump(test_runner.results, f)
  
  with open("../README.md", "r") as f:
    lines = f.readlines()

  start_idx = end_idx = None
  for i, line in enumerate(lines):
    if "<!-- LATEST TEST HERE -->" in line:
      start_idx = i
    if "<!-- END LATEST TEST -->" in line:
      end_idx = i

  if start_idx is not None and end_idx is not None:
    new_lines = lines[:start_idx+1] + [
      "\n| Test Name | Deviation |\n",
      "|-----------|-----------|\n"
    ]
    
    for key, value in test_runner.results.items():
      new_lines.append(f"| {key} | {value}% |\n")
    
    new_lines += lines[end_idx:]
    
    with open("../README.md", "w") as f:
      f.writelines(new_lines)
# %%
