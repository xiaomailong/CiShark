SELECT session_id,FROM_UNIXTIME(log_tv_sec),log_tv_usec,get_log_type_name(log_type),log_content
FROM `log20150323`
WHERE session_id = 138 
	AND log_type IN (165,166,167,168,169,170,171,0) 
	AND log_tv_sec >= UNIX_TIMESTAMP('2015-03-23 09:25:00') 
	/*AND log_tv_sec <= UNIX_TIMESTAMP('2015-03-23 09:40:00')*/
ORDER BY log_tv_sec,log_tv_usec
