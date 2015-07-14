SELECT log.session_id,FROM_UNIXTIME(log.log_tv_sec),log.log_tv_usec,get_log_type_name(log.log_type),log.log_content
FROM LOG,SESSION
WHERE 
	log.session_id = session.`session_id`
	AND session.run_counter = 15
	AND session.ip = '192.168.1.200'
	/*AND log.log_type IN (165,166,167,168,169,170,171,176,0)*/
ORDER BY log.log_tv_sec,log.log_tv_usec
