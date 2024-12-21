import pandas as pd
import numpy as np


class Statistics:
    def __init__(self, df_name=None):
        """Initialize with an optional DataFrame name."""
        self.df_name = df_name

    def get_leading_zeros(self, df):
        """Get leading zeros in string columns of the DataFrame."""
        lz_cols = {}
        string_cols = df.select_dtypes(include=["object", "string"]).columns

        for col in string_cols:
            filtered_df = df[df[col].astype(str).fillna("").str.startswith("0")]
            if not filtered_df.empty:
                leading_zero_values = filtered_df[col].unique()
                lz_cols[col] = leading_zero_values.tolist()

        max_length = max(len(v) for v in lz_cols.values()) if lz_cols else 0
        for key in lz_cols.keys():
            while len(lz_cols[key]) < max_length:
                lz_cols[key].append(None)

        return pd.DataFrame(lz_cols)

    def get_outliers(self, series):
        """Identify outliers in a Series using the IQR method."""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (series < lower_bound) | (series > upper_bound)

    def get_str_stats(self, stats_data, df, col):
        """Calculate statistics for string columns."""
        unique_dtypes = df[col].apply(type).unique()
        dtype_str = ", ".join([dtype.__name__ for dtype in unique_dtypes])

        stats_data["DTypes"].append(dtype_str)
        stats_data["NaNs"].append(df[col].isna().sum())
        stats_data["0_values"].append((df[col] == 0).sum())
        stats_data["Unique"].append(len(df[col].unique()))
        stats_data["Duplicates"].append(df[col].duplicated().sum())

    def get_float_stats(self, stats_data, df, col):
        """Calculate statistics for float columns."""
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0).astype(float)
            stats_data["Min"].append(df[col].min())
            stats_data["Max"].append(df[col].max())
            stats_data["Mean"].append(df[col].mean())
            stats_data["Median"].append(df[col].median())
            stats_data["STD"].append(df[col].std())
            stats_data["STD (%)"].append(
                (df[col].std() / df[col].mean()) * 100
                if df[col].mean() != 0
                else np.nan
            )
            stats_data["Totals"].append(df[col].sum())
            stats_data["Outliers"].append(self.get_outliers(df[col]).sum())
        else:
            for key in [
                "Min",
                "Max",
                "Mean",
                "Median",
                "STD",
                "STD (%)",
                "Outliers",
                "Totals",
            ]:
                stats_data[key].append(np.nan)

    def get_stats(self, df):
        """Calculate various statistics for the DataFrame."""
        stats_data = {
            "DTypes": [],
            "NaNs": [],
            "0_values": [],
            "Unique": [],
            "Duplicates": [],
            "Totals": [],
            "Min": [],
            "Max": [],
            "Mean": [],
            "Median": [],
            "STD": [],
            "STD (%)": [],
            "Outliers": [],
        }

        for col in df.columns:
            self.get_str_stats(stats_data, df, col)
            self.get_float_stats(stats_data, df, col)

        return pd.DataFrame(stats_data, index=df.columns), len(df)

    def show_stats(self, df):
        """Display statistics and leading zeros for the DataFrame."""

        # Set pandas display options
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)
        pd.set_option("display.max_colwidth", 30)
        pd.set_option("display.float_format", "{:,.2f}".format)

        # Use stored DataFrame name or fallback to default
        display_name = self.df_name if self.df_name else "DataFrame"

        lz = self.get_leading_zeros(df)
        stats, length_of_df = self.get_stats(df)

        print(f"{' ' * 100}")
        print(f"{'=' * 50} {display_name} {'=' * 50}")

        print("Leading zeros in columns\n")
        print(lz.head(3))

        print("\nGeneral stats\n")
        print(stats)

        print(f"Overall data frame length: {length_of_df}")


# Module-level function that users can call directly
def show_stats(df):
    """Display statistics for the given DataFrame."""
    statistics = Statistics(df_name="df_1")
    return statistics.show_stats(df)


# Tests
# import gendummy as gd
# show_stats(gd.gendf_auto(cols=5, rows=10))
