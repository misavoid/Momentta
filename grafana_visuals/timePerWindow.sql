SELECT
    window_title AS metric,  -- Window title shown on the X-axis
    SUM(duration)/60 AS value  -- Total time spent on each window title
FROM
    activity_log
WHERE
    strftime('%Y-%m', substr(timestamp, 1, 19)) >= '2024-08'
  AND strftime('%Y-%m', substr(timestamp, 1, 19)) <= '2024-09'
GROUP BY
    window_title
HAVING
    SUM(duration) >= 5  -- Filter to show only window titles with a total duration of 5 or more
ORDER BY
    value DESC;
