import sqlite3
from pathlib import Path


def countryCodes_humans(start_time, end_time):
    country_query_humans = """
    SELECT countryCode, COUNT(*) AS count
    FROM logs
    WHERE Agent_Type = 'H'
    AND status_code <> 404
    AND strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    GROUP BY countryCode
    ORDER BY count DESC
    """
    country_counts_humans = execute_query(country_query_humans, start_time, end_time)
    countryCodes_humans, percentages_humans = barchart_values(country_counts_humans)
    chart_data = {
        'countryCodes': countryCodes_humans[:10],
        'percentages': percentages_humans[:10],
        'title': f'Website Visits by Country for {start_time[:10]} to {end_time[:10]}',
    }
    return chart_data


def countryCodes_robots(start_time, end_time):
    country_query_robots = """
    SELECT countryCode, COUNT(*) AS count
    FROM logs
    WHERE Agent_Type = 'R'
    AND strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    GROUP BY countryCode
    ORDER BY count DESC
    """
    country_counts_robots = execute_query(country_query_robots, start_time, end_time)
    countryCodes_robots, percentages_robots = barchart_values(country_counts_robots)
    chart_data = {
        'countryCodes': countryCodes_robots[:10],
        'percentages': percentages_robots[:10],
        'title': f'Website Visits by Country for {start_time[:10]} to {end_time[:10]}',
    }
    return chart_data


def endpoints_humans(start_time, end_time):
    endpoint_query_humans = """
    SELECT endpoint, COUNT(*) AS count
    FROM logs
    WHERE Agent_Type = 'H'
    AND strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    GROUP BY endpoint
    ORDER BY count DESC
    """
    endpoint_counts_humans = execute_query(endpoint_query_humans, start_time, end_time)
    endpoints_humans, percentages_humans = barchart_values(endpoint_counts_humans)
    chart_data = {
        'endpoints': endpoints_humans[:10],
        'percentages': percentages_humans[:10],
        'title': f'Website Visits by Endpoint for {start_time[:10]} to {end_time[:10]}',
    }
    return chart_data


def endpoints_robots(start_time, end_time):
    endpoint_query_robots= """
    SELECT endpoint, COUNT(*) AS count
    FROM logs
    WHERE Agent_Type = 'R'
    AND strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    GROUP BY endpoint
    ORDER BY count DESC
    """
    endpoint_counts_robots = execute_query(endpoint_query_robots, start_time, end_time)
    endpoints_robots, percentages_robots = barchart_values(endpoint_counts_robots)
    chart_data = {
        'endpoints':endpoints_robots[:10],
        'percentages': percentages_robots[:10],
        'title': f'Website Visits by Endpoint for {start_time[:10]} to {end_time[:10]}',
    }
    return chart_data


def visits(start_time, end_time):
    visits_query = """
    SELECT DATE(datetime) AS visit_day,
        COUNT(*) AS total_visits,
        COUNT(CASE WHEN Agent_Type = 'H' THEN 1 END) AS human_visits,
        COUNT(CASE WHEN Agent_Type = 'R' THEN 1 END) AS robot_visits
    FROM logs
    WHERE strftime('%Y-%m-%d %H:%M:%S', datetime) BETWEEN ? AND ?
    AND status_code <> 404
    GROUP BY DATE(datetime)
    ORDER BY visit_day;
    """
    visits_counts = execute_query(visits_query, start_time, end_time)
    dates, humans, robots = linechart_values(visits_counts)
    chart_data = {
        'dates': dates,
        'humans': humans,
        'robots': robots,
    }
    return chart_data


def execute_query(query, start_time, end_time):
    grandparent = Path(__file__).resolve().parents[2]
    path2db = Path(grandparent, 'logs/data.philiplessner.com/logs.db')
    conn = sqlite3.connect(path2db)
    results = conn.execute(query, (start_time, end_time)).fetchall()
    conn.close()
    return results


def barchart_values(query_results):
    category_values = [category for category, _ in query_results]
    y_absolute_values = [count for _, count in query_results]
    total = sum(y_absolute_values)
    percentages = [count/total*100. for count in y_absolute_values]
    return category_values, percentages


def linechart_values(query_results):
    dates = [date for date, _, _, _ in query_results]
    humans = [human for _,_, human, _ in query_results]
    robots = [robot for _, _, _, robot in query_results]
    return dates, humans, robots
