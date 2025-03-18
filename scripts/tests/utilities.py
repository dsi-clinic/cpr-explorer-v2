from pathlib import Path
import pandas as pd
from config import GROUNDTRUTH_DIR, DATA_ENDPOINT

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

class ComparisonRunner():
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
  
  def get_merged_tables(self, config):
    groundtruth_data = self.groundtruth.dfs[config["groundtruth"]]
    test_data = self.get_test_data(config)
    if "sort_by" in config:
      test_data = test_data.sort_values(config["sort_by"])
    if config.get("add_row_id") == True:
      test_data = test_data.reset_index()
      test_data["ROW_ID"] = test_data.index + 1
    if config.get("keep_cols"):
      test_data = test_data[config['keep_cols']]
    
    return test_data.merge(groundtruth_data, left_on=config['left_on'], right_on=config['right_on'], how="inner")
  
  def run_table_equality_test(self,config):
    merged = self.get_merged_tables(config)
    for cols in config["comparison_cols"]:
      merged[cols[0] + "_comparison"] = (merged[cols[0]] - merged[cols[1]]) / merged[cols[0]]
      ave_diff = merged[cols[0] + "_comparison"].mean()
      assert ave_diff < config["threshold"]

      print("\nPASSED", f"{round(ave_diff*100, 3)}% average difference\n", config["name"], config["type"], cols)
      self.results[f"{config['name']} :: {cols[1]}"] = f"{round(ave_diff*100, 3)}%"
  
  def run_correlation_test(self, config):
    merged = self.get_merged_tables(config)
    for cols in config["comparison_cols"]:
      correlation = merged[cols[0]].corr(merged[cols[1]])
      self.results[f"{config['name']} :: {cols[1]}" + ' r-squared'] = round((correlation**2)*100, 3)
      assert correlation > config["threshold"]
      print("\nPASSED", f"{round(correlation*100, 3)}% correlation\n", config["name"], config["type"], cols)

  def run_sum_total_test(self, config):
    groundtruth_data = self.groundtruth.dfs[config["groundtruth"]]
    test_data = self.get_test_data(config)
    for cols in config["comparison_cols"]:
      [sum_test, sum_ground] = [test_data[cols[0]].sum(), groundtruth_data[cols[1]].sum()]
      diff = (sum_test - sum_ground) / sum_test
      assert abs(diff) < config["threshold"]
      print("\nPASSED", f"{round(diff*100, 3)}% average difference\n", config["name"], config["type"], cols)
      self.results[f"{config["name"]} {cols[1]}"] = f"{round(diff*100, 3)}%"

  def run_test(self, test_id):
    test = self.test_config.get(test_id)
    match test["type"]:
      case "table_equality":
        self.run_table_equality_test(test)
      case "correlation":
        self.run_correlation_test(test)
      case "sum_total":
        self.run_sum_total_test(test)
      case _:
        print("Test type not supported")
                              
  def oneshot_run_tests(self):
    for test in self.test_config:
      self.run_test(test)
