import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


def countryCodes_humans():
    country_query_humans = """
    SELECT countryCode, COUNT(*) AS count
    FROM logs
    WHERE Agent_Type = 'H'
    AND status_code <> 404
    AND strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    GROUP BY countryCode
    ORDER BY count DESC
    """
    grandparent = Path(__file__).resolve().parents[2]
    path2db = Path(grandparent, 'logs/data.philiplessner.com/logs.db')
    conn = sqlite3.connect(path2db)
    yesterday = (datetime.now(tz=timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    past = (datetime.now(tz=timezone.utc) - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
    country_counts_humans = conn.execute(country_query_humans, (past, yesterday)).fetchall()
    conn.close()
    countryCodes_humans = [countryCode for countryCode, _ in country_counts_humans]
    counts_humans = [count for _, count in country_counts_humans]
    total = sum(counts_humans)
    percentages_humans = [count/total*100. for count in counts_humans]
    chart_data = {
        'countryCodes': countryCodes_humans[:10],
        'percentages': percentages_humans[:10],
        'title': f'Percent Website Visits by Country for {past} to {yesterday}',
    }
    return chart_data


def endpoints_humans():
    endpoint_query_humans = """
    SELECT endpoint, COUNT(*) AS count
    FROM logs
    WHERE Agent_Type = 'H'
    AND strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    GROUP BY endpoint
    ORDER BY count DESC
    """
    grandparent = Path(__file__).resolve().parents[2]
    path2db = Path(grandparent, 'logs/data.philiplessner.com/logs.db')
    conn = sqlite3.connect(path2db)
    yesterday = (datetime.now(tz=timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    past = (datetime.now(tz=timezone.utc) - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
    endpoint_counts_humans = conn.execute(endpoint_query_humans, (past, yesterday)).fetchall()
    conn.close()
    endpoints_humans = [endpoint for endpoint, _ in endpoint_counts_humans]
    counts_humans = [count for _, count in endpoint_counts_humans]
    total = sum(counts_humans)
    percentages_humans = [count/total*100. for count in counts_humans]
    chart_data = {
        'endpoints': endpoints_humans[:10],
        'percentages': percentages_humans[:10],
        'title': f'Percent Website Visits by Endpoint for {past} to {yesterday}',
    }
    return chart_data
