import csv
import sys
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import streamlit as st
except ImportError:
    st = None

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    px = None
    go = None

CSV_PATH = 'urbanmart_sales.csv'


# ============= Data Loading =============
def read_with_csv_module(csv_path):
    """Read CSV using csv module and return list of dicts."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []


def read_with_pandas(csv_path):
    """Read CSV using pandas."""
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error reading CSV with pandas: {e}")
        return None


def prepare_df_for_dashboard(df):
    """Convert date column to datetime."""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df


# ============= Sanity Checks =============
def sanity_checks_list(rows):
    """Basic sanity checks for list of dicts."""
    print(f"Total records: {len(rows)}")
    if rows:
        print(f"Columns: {list(rows[0].keys())}")


def sanity_checks_df(df):
    """Basic sanity checks for DataFrame."""
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes}")


# ============= Analysis Functions =============
def count_channels_manual(rows):
    """Count channels manually from list of dicts."""
    ch_count = {}
    for row in rows:
        ch = row.get('channel', 'Unknown')
        ch_count[ch] = ch_count.get(ch, 0) + 1
    return ch_count


def revenue_summaries(df):
    """Calculate revenue summaries."""
    revenue_by_category = df.groupby('product_category')['line_revenue'].sum().sort_values(ascending=False)
    revenue_by_store = df.groupby('store_location')['line_revenue'].sum().sort_values(ascending=False)
    revenue_by_channel = df.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)
    top_customers = df.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False)
    return {
        'revenue_by_category': revenue_by_category,
        'revenue_by_store': revenue_by_store,
        'revenue_by_channel': revenue_by_channel,
        'top_customers': top_customers
    }


# Optional reusable filter function
def filter_data(df, start_date=None, end_date=None, store=None, channel=None):
    """Filter pandas DataFrame step by step. start_date/end_date accept strings or datetime."""
    if pd is None or not isinstance(df, pd.DataFrame):
        raise ValueError("filter_data expects a pandas DataFrame")
    out = df
    if start_date is not None:
        out = out[out['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        out = out[out['date'] <= pd.to_datetime(end_date)]
    if store is not None and store != 'All':
        out = out[out['store_location'].isin(store if isinstance(store, (list, tuple)) else [store])]
    if channel is not None and channel != 'All':
        out = out[out['channel'] == channel]
    return out


# ============= CLI Menu =============
def welcome():
    """Print welcome message."""
    print("\n" + "="*50)
    print("Welcome to UrbanMart Sales Analysis")
    print("="*50 + "\n")


def cli_menu(data, using_pandas=True):
    """Simple CLI menu for data exploration."""
    while True:
        print("\n--- Options ---")
        print("1. View summary statistics")
        print("2. View top records")
        print("3. Exit")
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            if using_pandas:
                print("\nSummary Statistics:")
                print(data.describe())
            else:
                print(f"Total records: {len(data)}")
        elif choice == '2':
            if using_pandas:
                print("\nFirst 5 records:")
                print(data.head())
            else:
                print("\nFirst 5 records:")
                for i, row in enumerate(data[:5]):
                    print(row)
                    if i == 4:
                        break
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



# ----------------------- Main execution -----------------------
if __name__ == '__main__':
    welcome()
    # Ask user which option to use to read data
    print("Choose data loading option:")
    print("A. Use csv module (list of dicts)")
    print("B. Use pandas (DataFrame) — preferred for dashboard")
    choice = input("Enter A or B (default B): ").strip().upper() or 'B'
    try:
        if choice == 'A':
            rows = read_with_csv_module(CSV_PATH)
            sanity_checks_list(rows)
            # manual channel counts
            ch_counts = count_channels_manual(rows)
            print("Channel counts (manual):", ch_counts)
            cli_menu(rows, using_pandas=False)
        else:
            if pd is None:
                print("pandas not installed — falling back to csv module")
                rows = read_with_csv_module(CSV_PATH)
                sanity_checks_list(rows)
                cli_menu(rows, using_pandas=False)
            else:
                df = read_with_pandas(CSV_PATH)
                df = prepare_df_for_dashboard(df)
                sanity_checks_df(df)
                summaries = revenue_summaries(df)
                print("Top 5 stores by revenue:")
                print(summaries['revenue_by_store'].head(5))
                cli_menu(df, using_pandas=True)
    except FileNotFoundError:
        print(f"File not found: {CSV_PATH}. Please make sure the CSV is present in the working directory.")
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        sys.exit(1)