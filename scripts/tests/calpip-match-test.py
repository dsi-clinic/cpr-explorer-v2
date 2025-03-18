# %%
import json
from config import GROUNDTRUTH_FILES, TEST_CONFIG
from utilities import GroundTruthDataParser, ComparisonRunner

groundtruth = GroundTruthDataParser(GROUNDTRUTH_FILES)
test_runner =  ComparisonRunner(TEST_CONFIG, groundtruth)

def test_run_county_totals():
  test_runner.run_test("2022 :: County totals")

def test_run_county_correlation():
  test_runner.run_test("2022 :: County correlation")

def test_run_county_ag_totals():
  test_runner.run_test("2020 :: County ag totals")

def test_run_county_ag_correlation():
  test_runner.run_test("2020 :: County ag correlation")

def test_run_county_non_ag_totals():
  test_runner.run_test("2022 :: County non-ag totals")

def test_run_county_non_ag_correlation():
  test_runner.run_test("2022 :: County non-ag correlation")

def test_run_tract_sum_total():
  test_runner.run_test("Tract Sum Total")

def test_run_school_districts_sum_total():
  test_runner.run_test("School Districts Sum Total")

def test_run_zcta_sum_total():
  test_runner.run_test("ZCTA Sum Total")

def test_run_townships_total():
  test_runner.run_test("Townships Total")

def test_run_section_total():
  test_runner.run_test("Section Total")

def test_run_sac_total():
  test_runner.run_test("Sections Sacramento Alfalfa Total")

def test_run_sac_correlation():
  test_runner.run_test("Sections Sacramento alfalfa correlation")

def test_export_results():
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
      new_lines.append(f"| {key} | {value} |\n")
    
    new_lines += lines[end_idx:]
    
    with open("../README.md", "w") as f:
      f.writelines(new_lines)
