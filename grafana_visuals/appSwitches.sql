-- doesnt make sense yet
SELECT
    application AS metric,  -- Application will be shown on the X-axis
    SUM(duration)/60 AS value  -- Total time spent in each application
FROM
    activity_log
WHERE
    strftime('%Y-%m', substr(timestamp, 1, 19)) >= '2024-08'
  AND strftime('%Y-%m', substr(timestamp, 1, 19)) <= '2024-09'
GROUP BY
    application
ORDER BY
    value DESC
LIMIT 5;  -- Show only the top 5 applications
