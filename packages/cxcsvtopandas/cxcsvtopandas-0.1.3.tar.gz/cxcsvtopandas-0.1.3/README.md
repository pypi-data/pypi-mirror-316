# cxpandascsvloader
A simple example package for loading and processing CSV data into Pandas DataFrames.

## Installation
You can install the `cxpandascsvloader` package using pip:

```sh
pip install cxcsvtopandas
```

## Usage
```sh
% python                        
Python 3.9.20 (main, Oct 19 2024, 17:36:14) 
[Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import cxcsvtopandas.dataframeloader as dfl
>>> dfl.printinfo()
dataframeloader module loaded.
```

## Examples
Using the generic `dataframeloader` method to read files with specific prefix.
```python
import cxcsvtopandas.dataframeloader as dfl
root = '../../.dataDir'
df = dfl.loadDataFrameFromFileRegex(root, "ASSESS*")
```

Optionally specify date range for filtering csv files;
```python
import cxcsvtopandas.dataframeloader as dfl
root = '../../.dataDir'
fromDt = '2024-11-10'
toDt = '2024-12-10'
df = dfl.loadDataFrameFromFileRegex(root, "ASSESS*", daterange=[fromDt, toDt])
```

Propritary timeseries reporting;
```python
import cxcsvtopandas.dataframeloader as dfl
root = '../../.dataDir'
fromDt = '2024-11-10'
toDt = '2024-12-10'
metricsArr = ['cpu_used','task_queue_length', 'memory_used']
daterange=[fromDt, toDt]
df = dfl.loadApplianceTimeSeriesData(root, metricsArr, daterange)
appliance_id='58e98e10-1b19-4c84-93c0-db2ad5903b80'
## fromDt and toDt can also be a subset of the total dataframe.
fig  = dfl.plotMetricsFacetForApplianceId(df, appliance_id)
fig.show()
```