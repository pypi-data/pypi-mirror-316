# ants-fts
This repository is used to extract features from Antsomi's features.

# Example

```python
import pandas as pd
from datetime import datetime, timedelta
from ants_extractor.IntervalExtractor import IntervalExtractor
from ants_extractor.SkewnessScoreExtractor import SkewnessScoreExtractor
from ants_extractor.DatetimeExtractor import DatetimeExtractor
from ants_extractor.DeductionExtractor import DeductionExtractor
from ants_extractor.PurchasingPowerExtractor import PurchasingPowerExtractor
from ants_extractor.RFMExtractor import RFMExtractor
from datetime import datetime, timedelta
import warnings 
warnings.filterwarnings('ignore')

data = {'customer_phone': {35452: '640327a3423b8329d601c1ff11208337',
  40030: '640327a3423b8329d601c1ff11208337',
  54858: 'be3e7573aa9334c9d2e2c37ef69de838',
  72959: 'be3e7573aa9334c9d2e2c37ef69de838',
  73009: 'be3e7573aa9334c9d2e2c37ef69de838',
  84052: '89a90516cc24ac0d5052dd70150f1b5d',
  85677: '89a90516cc24ac0d5052dd70150f1b5d',
  99817: 'be3e7573aa9334c9d2e2c37ef69de838',
  106287: 'be3e7573aa9334c9d2e2c37ef69de838',
  123339: '89a90516cc24ac0d5052dd70150f1b5d',
  134011: '89a90516cc24ac0d5052dd70150f1b5d',
  150009: '89a90516cc24ac0d5052dd70150f1b5d',
  168649: 'be3e7573aa9334c9d2e2c37ef69de838',
  200112: '640327a3423b8329d601c1ff11208337',
  228401: '640327a3423b8329d601c1ff11208337',
  234409: '640327a3423b8329d601c1ff11208337'},
 'date_created': {35452: pd.Timestamp('2024-11-10 10:02:19'),
  40030: pd.Timestamp('2024-11-06 12:30:11'),
  54858: pd.Timestamp('2024-10-28 20:13:48'),
  72959: pd.Timestamp('2024-09-20 19:05:52'),
  73009: pd.Timestamp('2024-09-19 21:53:27'),
  84052: pd.Timestamp('2024-09-24 18:39:17'),
  85677: pd.Timestamp('2024-09-24 18:33:07'),
  99817: pd.Timestamp('2024-08-24 20:21:43'),
  106287: pd.Timestamp('2024-09-29 20:27:43'),
  123339: pd.Timestamp('2024-05-01 14:42:02'),
  134011: pd.Timestamp('2024-06-14 17:10:20'),
  150009: pd.Timestamp('2024-05-01 13:37:05'),
  168649: pd.Timestamp('2024-03-10 20:22:56'),
  200112: pd.Timestamp('2024-04-19 18:40:13'),
  228401: pd.Timestamp('2024-02-19 19:14:53'),
  234409: pd.Timestamp('2024-04-22 12:07:14')},
 'discount_amount': {35452: 0.0,
  40030: 0.0,
  54858: 75000.0,
  72959: 100000.0,
  73009: 84000.0,
  84052: 108000.0,
  85677: 1000000.0,
  99817: 174500.0,
  106287: 187500.0,
  123339: 0.0,
  134011: 395000.0,
  150009: 150000.0,
  168649: 179000.0,
  200112: 0.0,
  228401: 100000.0,
  234409: 0.0},
 'subtotal_amount': {35452: 100000.0,
  40030: 1500000.0,
  54858: 750000.0,
  72959: 144000.0,
  73009: 840000.0,
  84052: 1870000.0,
  85677: 1785000.0,
  99817: 1745000.0,
  106287: 1875000.0,
  123339: 90000.0,
  134011: 2290000.0,
  150009: 10745000.0,
  168649: 1790000.0,
  200112: 850000.0,
  228401: 1700000.0,
  234409: 0.0},
 'revenue': {35452: 100000.0,
  40030: 1500000.0,
  54858: 675000.0,
  72959: 44000.0,
  73009: 756000.0,
  84052: 1762000.0,
  85677: 785000.0,
  99817: 1570500.0,
  106287: 1687500.0,
  123339: 90000.0,
  134011: 1895000.0,
  150009: 10595000.0,
  168649: 1611000.0,
  200112: 850000.0,
  228401: 1600000.0,
  234409: 0.0}}
df = pd.DataFrame(data)
fts_01 = IntervalExtractor.extract(df, ['customer_phone'], 'date_created')
fts_02 = SkewnessScoreExtractor.extract(df, ['customer_phone'], 'date_created');
fts_03 = DatetimeExtractor.extract(df, ['customer_phone'], 'date_created');
fts_04 = DeductionExtractor.extract(df, ['customer_phone'], 'discount_amount', 'subtotal_amount');
fts_05 = PurchasingPowerExtractor.extract(df, ['customer_phone'], "revenue");
fts_06 = RFMExtractor.extract(df, ['customer_phone'], "date_created", "revenue", "2024-12-15 00:00:00");
fts = fts_01.merge(fts_02, how="left").merge(fts_03,how='left').merge(fts_04,how='left').merge(fts_04,how='left').merge(fts_05,how='left').merge(fts_06,how='left');

```