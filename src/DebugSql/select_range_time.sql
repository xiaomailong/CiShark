SELECT session_id,FROM_UNIXTIME(log_tv_sec),log_tv_usec,get_log_type_name(log_type),log_content
FROM `log20140929`
WHERE session_id = 236 AND log_type IN (165,166,167,168,169,170,171,0) AND log_tv_sec >= 1411971400 AND log_tv_sec <= 1411971600
ORDER BY log_tv_sec,log_tv_usec
