#!/usr/bin/python

import paramiko
import psycopg2

server1 = "10.10.154.100"
server2 = "10.10.154.101"

for server in (server1,server2):
	try:

		conn = psycopg2.connect(
			 database="opensips", user='postgres', password='postgres', host=server, port= '5432'
		)
		conn.autocommit = True
		cursor = conn.cursor()
		cursor.execute("truncate load_balancer RESTART IDENTITY CASCADE;")

		file = open("gsm.csv").readlines()
		for line in file:
			if line != "":
				data = line.strip().split(',')
				sql = (int(data[0]),data[1].replace('"',''),data[2].replace('"',''),int(data[3]),data[4].replace('"',''))
				cursor.execute('''
					INSERT INTO load_balancer(group_id,dst_uri,resources,probe_mode,description) \
					VALUES {}'''.format(sql))

		conn.commit()
		conn.close()
	
	except: pass

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
for server in (server1,server2):
	try:
		ssh.connect(server, username="root", password="Pls@1234!")
		stdin,stdout,stderr = ssh.exec_command("opensipsctl fifo lb_reload")
	except: pass
