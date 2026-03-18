from pathlib import Path

DATA_ENDPOINT = "https://d3lsdszfx9jqxt.cloudfront.net/data-query/"
DEVIATION_THRESHOLD = 0.01
ROOT_DIR = Path(__file__).parent.parent.parent
GROUNDTRUTH_DIR = Path.joinpath(ROOT_DIR, "public", "groundtruth", "csv_records")

GROUNDTRUTH_FILES = {
  "12472378904908_241206074018": {
    "desc": "All counties, 2022, Ag and Non-Ag. No other filters",
    "drop_cols": ["ADJUVANT", "YEAR", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "140488361239316_260313130416": {
    "desc": "All counties, 2023, Ag and Non-Ag. No other filters",
    "drop_cols": ["ADJUVANT", "YEAR", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "12472378904908_241206074507":{
    "desc": "All counties, 2022, Non-Ag only. No other filters",
    "drop_cols": ["ADJUVANT", "YEAR", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "140488361239316_260313130447":{
    "desc": "All counties, 2023, Non-Ag only. No other filters",
    "drop_cols": ["ADJUVANT", "YEAR", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "12495048391211_241206085403":{
    "desc": "All counties, 2020, Ag only. No other filters",
    "drop_cols": ["ADJUVANT", "COUNTY_NAME"],
    "group_cols": ["COUNTY_CODE"]
  },
  "12472378904908_241206074829": {
    "desc": "Sacramento county, 2020. Ag only, Alfalfa site.",
    "drop_cols": ["ADJUVANT", "YEAR"],
    "group_cols": ["COMTRS"]
  },
  "142340312794115_260318072125": {
    "desc": "Sacramento county, 2023. Ag only, Alfalfa site.",
    "drop_cols": ["ADJUVANT", "YEAR"],
    "group_cols": ["COMTRS"]
  },
  "12489387854613_241206083511": {
    "desc": "Sacramento county, 2020. Ag only, Mineral oil AI.",
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

COUNTY_DEFAULT_TEST_CONFIG_22 = {
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

COUNTY_DEFAULT_TEST_CONFIG_23 = {
  **COUNTY_DEFAULT_TEST_CONFIG_22,
    "filters": {  "start": "2023-01", "end": "2023-12" },
}
TEST_CONFIG = {
  "2022 :: County totals": {
    **COUNTY_DEFAULT_TEST_CONFIG_22,
    "name": "2022 County Totals",
    "groundtruth": "12472378904908_241206074018",
  },
  "2022 :: County correlation": {
    **COUNTY_DEFAULT_TEST_CONFIG_22,
    "name": "2022 County correlation",
    "groundtruth": "12472378904908_241206074018",
    "type": "correlation",
    "threshold": 0.95
  },
  "2022 :: County non-ag totals": {
    **COUNTY_DEFAULT_TEST_CONFIG_22,
    "name": "2022 County non-ag totals",
    "groundtruth": "12472378904908_241206074507",
    "filters": {
      **COUNTY_DEFAULT_TEST_CONFIG_22["filters"],
      "usetype": "NON-AG"
    }
  },
  "2022 :: County non-ag correlation": {
    **COUNTY_DEFAULT_TEST_CONFIG_22,
    "name": "2022 County non-ag correlation",
    "groundtruth": "12472378904908_241206074507",
    "filters": {
      **COUNTY_DEFAULT_TEST_CONFIG_22["filters"],
      "usetype": "NON-AG"
    },
    "type": "correlation",
    "threshold": 0.95
  },
  


  "2023 :: County totals": {
    **COUNTY_DEFAULT_TEST_CONFIG_23,
    "name": "2023 County Totals",
    "groundtruth": "140488361239316_260313130416",
  },
  "2023 :: County correlation": {
    **COUNTY_DEFAULT_TEST_CONFIG_23,
    "name": "2023 County correlation",
    "groundtruth": "140488361239316_260313130416",
    "type": "correlation",
    "threshold": 0.95
  },
  "2023 :: County non-ag totals": {
    **COUNTY_DEFAULT_TEST_CONFIG_23,
    "name": "2023 County non-ag totals",
    "groundtruth": "140488361239316_260313130447",
    "filters": {
      **COUNTY_DEFAULT_TEST_CONFIG_23["filters"],
      "usetype": "NON-AG"
    }
  },
  "2023 :: County non-ag correlation": {
    **COUNTY_DEFAULT_TEST_CONFIG_23,
    "name": "2023 County non-ag correlation",
    "groundtruth": "140488361239316_260313130447",
    "filters": {
      **COUNTY_DEFAULT_TEST_CONFIG_23["filters"],
      "usetype": "NON-AG"
    },
    "type": "correlation",
    "threshold": 0.95
  },

  "2020 :: County ag totals": {
    **COUNTY_DEFAULT_TEST_CONFIG_22,
    "name": "2020 County ag totals",
    "groundtruth": "12495048391211_241206085403",
    "filters": {
      "usetype": "AG",
      "start": "2020-01",
      "end": "2020-12"
    }
  },
  "2020 :: County ag correlation": {
    **COUNTY_DEFAULT_TEST_CONFIG_22,
    "name": "2020 County ag correlation",
    "groundtruth": "12495048391211_241206085403",
    "filters": {
      "usetype": "AG",
      "start": "2020-01",
      "end": "2020-12"
    },
    "type": "correlation",
    "threshold": 0.95
  },
  "Tract Sum Total": {
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
  "School Districts Sum Total": {
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
  "ZCTA Sum Total" :{
    "name": "ZCTA Sum Total",
    "groundtruth": "12495048391211_241206085403",
    "type": "sum_total",
    "threshold": 0.03,
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
  "Townships Total":{
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
  "Section Total": {
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
  "2020 :: Sections Sacramento Alfalfa Total": {
    "name": "2020 :: Sections Sacramento alfalfa total",
    "groundtruth": "12472378904908_241206074829",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["section"],
    "left_on": ["comtrs"],
    "right_on": ["COMTRS"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG",
      "site": "23001",
      "county": "34"
    },
    "comparison_cols": [
      ("lbs_chm_used", "POUNDS_CHEMICAL_APPLIED"),
      ("lbs_prd_used", "POUNDS_PRODUCT_APPLIED")
    ]
  },
  "2020 :: Sections Sacramento alfalfa correlation": {
    "name": "2020 :: Sections Sacramento alfalfa correlation",
    "groundtruth": "12472378904908_241206074829",
    "type": "correlation",
    "threshold": .99,
    "left_on": ["comtrs"],
    "right_on": ["COMTRS"],
    "endpoint": GEO_ENDPOINTS["section"],
    "filters": {
      "start": "2020-01",
      "end": "2020-12",
      "usetype": "AG",
      "site": "23001"
    },
    "comparison_cols": [
      ("lbs_chm_used", "POUNDS_CHEMICAL_APPLIED"),
      ("lbs_prd_used", "POUNDS_PRODUCT_APPLIED")
    ]
  },
  "2023 :: Sections Sacramento Alfalfa Total": {
    "name": "2023 :: Sections Sacramento alfalfa total",
    "groundtruth": "142340312794115_260318072125",
    "type": "sum_total",
    "threshold": DEVIATION_THRESHOLD,
    "endpoint": GEO_ENDPOINTS["section"],
    "left_on": ["comtrs"],
    "right_on": ["COMTRS"],
    "filters": {
      "start": "2023-01",
      "end": "2023-12",
      "usetype": "AG",
      "site": "23001",
      "county": "34"
    },
    "comparison_cols": [
      ("lbs_chm_used", "POUNDS_CHEMICAL_APPLIED"),
      ("lbs_prd_used", "POUNDS_PRODUCT_APPLIED")
    ]
  },
  "2023 :: Sections Sacramento alfalfa correlation": {
    "name": "2023 :: Sections Sacramento alfalfa correlation",
    "groundtruth": "142340312794115_260318072125",
    "type": "correlation",
    "threshold": .99,
    "left_on": ["comtrs"],
    "right_on": ["COMTRS"],
    "endpoint": GEO_ENDPOINTS["section"],
    "filters": {
      "start": "2023-01",
      "end": "2023-12",
      "usetype": "AG",
      "site": "23001"
    },
    "comparison_cols": [
      ("lbs_chm_used", "POUNDS_CHEMICAL_APPLIED"),
      ("lbs_prd_used", "POUNDS_PRODUCT_APPLIED")
    ]
  }
}