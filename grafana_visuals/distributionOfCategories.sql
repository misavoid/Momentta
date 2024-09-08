SELECT
    category AS metric,  -- Category will be shown in the legend
    SUM(duration)/60 AS value  -- Total time spent in each category
FROM
    activity_log
WHERE
    strftime('%Y-%m', substr(timestamp, 1, 19)) >= '2024-08'
  AND strftime('%Y-%m', substr(timestamp, 1, 19)) <= '2024-09'
GROUP BY
    category
ORDER BY
    value DESC;
