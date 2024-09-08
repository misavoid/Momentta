WITH top_apps AS (
    SELECT
        application,
        SUM(duration) AS total_time
    FROM
        activity_log
    GROUP BY
        application
    ORDER BY
        total_time DESC
    LIMIT 5  -- Get the top 5 applications
)

SELECT
    CAST(strftime('%s', substr(timestamp, 1, 19)) AS INTEGER) AS time,  -- Convert to Unix timestamp
    application AS metric,  -- Application to track usage
    SUM(duration) / 60.0 AS value  -- Convert duration to minutes
FROM
    activity_log
WHERE
    application IN (SELECT application FROM top_apps)  -- Limit to the top 5 applications
GROUP BY
    time, application
ORDER BY
    time ASC;
