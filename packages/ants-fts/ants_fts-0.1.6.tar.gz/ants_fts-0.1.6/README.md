<h2>Antsomi Extractors<h2>

<p>Installation:</p> `pip install ants-fts`
<br>
<p>Importation:</p> `import ants_extractor`
<br>
<body>
  <pre><code class="python">
import pandas as pd
from ants_extractor.IntervalExtractor import IntervalExtractor
from ants_extractor.SkewnessScoreExtractor import SkewnessScoreExtractor
from ants_extractor.DatetimeExtractor import DatetimeExtractor
from ants_extractor.DeductionExtractor import DeductionExtractor
from ants_extractor.PurchasingPowerExtractor import PurchasingPowerExtractor
from ants_extractor.RFMExtractor import RFMExtractor
from datetime import datetime, timedelta
import warnings 
warnings.filterwarnings('ignore')

def test():
	df = pd.read_csv("<file path>", \
						sep = "\t", \
						dtype = {"customer_phone": str});
	df['date_created'] = pd.to_datetime(df['date_created'], format="%Y-%m-%d %H:%M:%S", errors="coerce");

	itv_fts = IntervalExtractor.extract(df, ['customer_phone'], 'date_created');
	print("Got interval features")

	df['int_date_created'] = df['int_date_created'] = (df['date_created'] - pd.to_datetime("1970-01-01 00:00:00")).dt.total_seconds()/(24 * 3600);
	skewness_score_fts = SkewnessScoreExtractor.extract(df, ['customer_phone'], 'int_date_created');
	print("Got skewness score features")

	dt_fts = DatetimeExtractor.extract(df, ['customer_phone'], 'date_created');
	print("Got datetime features")

	deduction_fts = DeductionExtractor.extract(df, ['customer_phone'], 'discount_amount', 'subtotal_amount')
	print("Got deduction features")

	purchasing_power_fts = PurchasingPowerExtractor.extract(df, ["customer_phone"], "revenue");
	print("Got purchasing power features");

	recency_fts = RFMExtractor.extract_recency(df, ["customer_phone"], "date_created", "2024-12-15 00:00:00");
	print("Got recency features");

	fts = itv_fts.merge(skewness_score_fts, how='left')\
					.merge(dt_fts, how = 'left')\
					.merge(deduction_fts, how='left')\
					.merge(purchasing_power_fts, how='left')\
					.merge(recency_fts, how = 'left');

	print(fts.tail(2).T)
	return;

test()
  </code></pre>
</body>