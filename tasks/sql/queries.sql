
SELECT user_id, 
       COUNT(CASE WHEN status = 'Pending' THEN 1 END) AS pending,
       COUNT(CASE WHEN status = 'In Progress' THEN 1 END) AS in_progress,
       COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS completed
FROM tasks
GROUP BY user_id;