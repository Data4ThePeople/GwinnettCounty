import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
print(download("https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/list1_2023.xlsx", "omb/list1_2023.xlsx"))
print(download("https://www.fhfa.gov/hpi/download/annual/hpi_at_county.csv", "fhfa/hpi_at_county.xlsx"))
for y in range(2007, 2022):
    download(f"https://www2.census.gov/econ/bps/County/co{y}a.txt", f"bps/co{y}a.txt")
print("bps ok")
