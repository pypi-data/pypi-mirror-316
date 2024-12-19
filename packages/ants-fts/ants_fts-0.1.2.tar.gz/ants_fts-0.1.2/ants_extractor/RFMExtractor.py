import pandas as pd
from BaseExtractor import BaseExtractor

class RFMExtractor(BaseExtractor):

    def __init__(self):
        pass

    @staticmethod
    def extract_recency(df, grouped_columns, key_date_column, reference_date):
        reference_date = pd.to_datetime(reference_date, format="%Y-%m-%d %H:%M:%S");
        recency_fts = df.groupby(by=grouped_columns)\
                        .agg(_max_dt = (key_date_column, "max"))\
                        .reset_index();

        recency_fts['_recency'] = (reference_date - recency_fts._max_dt).dt.total_seconds()/86400;
        recency_fts = recency_fts[grouped_columns + ['_recency']];
        return recency_fts;

    pass




