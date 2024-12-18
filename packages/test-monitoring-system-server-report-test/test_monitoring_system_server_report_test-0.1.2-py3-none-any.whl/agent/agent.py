import socket
import time
from metrics_utils import collect_metrics
import psutil
import platform
import  os


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Connect to a public IP to determine the local IP
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Error retrieving local IP: {e}")
        return None

def send_metrics(server_ip, server_port, hostname):
    """Send metrics to the server."""
    while True:
        metrics = collect_metrics()
        for metric, value in metrics.items():
            # print("cpu states --", )

            message = f"{hostname}|{metric}|{value}"
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((server_ip, server_port))
                print(psutil.cpu_count())

                client.send(message.encode())
                response = client.recv(1024)
                print(f"Server response: {response.decode()}")
                client.close()
            except Exception as e:
                print(f"Error: {e}")
        time.sleep(1)



def main():
    SERVER_PORT = 10053
    HOSTNAME = "test-host"

    # Dynamically fetch the server's IP address
    SERVER_IP = get_local_ip()
    if SERVER_IP:
        print(f"Using dynamically determined IP: {SERVER_IP}")
        send_metrics(SERVER_IP, SERVER_PORT, HOSTNAME)
    else:
        print("Could not determine the local IP address.")

if __name__ == "__main__":
    main()

# import psutil
# import pymysql
# import psycopg2
# import requests
#
#
# # MySQL Monitoring Function
# def get_mysql_sessions(db_params):
#     try:
#         conn = pymysql.connect(**db_params)
#         cursor = conn.cursor()
#         cursor.execute("SELECT COUNT(*) FROM information_schema.processlist WHERE COMMAND != 'Sleep';")
#         active_sessions = cursor.fetchone()[0]
#         cursor.close()
#         conn.close()
#         return active_sessions
#     except Exception as e:
#         print(f"Error with MySQL: {e}")
#         return 0
#
#
# # PostgreSQL Monitoring Function
# def get_postgres_sessions(db_params):
#     try:
#         conn = psycopg2.connect(**db_params)
#         cursor = conn.cursor()
#         cursor.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';")
#         active_sessions = cursor.fetchone()[0]
#         cursor.close()
#         conn.close()
#         return active_sessions
#     except Exception as e:
#         print(f"Error with PostgreSQL: {e}")
#         return 0
#
#
# # SSH Monitoring Function
# def get_active_ssh_sessions():
#     ssh_sessions = 0
#     for proc in psutil.process_iter(['pid', 'name', 'username']):
#         if 'sshd' in proc.info['name']:
#             ssh_sessions += 1
#     return ssh_sessions
#
#
# # Nginx Active Connections Monitoring Function
# def get_nginx_active_connections(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             content = response.text
#             # Parse the response to extract the number of active connections
#             lines = content.splitlines()
#             for line in lines:
#                 if 'active connections' in line:
#                     active_connections = line.split()[2]  # Active connections count
#                     return int(active_connections)
#         return 0
#     except Exception as e:
#         print(f"Error with Nginx: {e}")
#         return 0
#
#
# # Main Function to Monitor All Data
# def monitor_server():
#     # Database Parameters (Change to your actual database parameters)
#     # mysql_db_params = {
#     #     'host': 'cybrosys',
#     #     'user': 'odoo16',
#     #     'password': 'cool',
#     #     'database': 'your_mysql_db'
#     # }
#
#     postgres_db_params = {
#         'dbname': 'monitoring_db',
#         'user': 'monitoring_user',
#         'password': 'cool',
#         'host': '',
#         'port': 5432
#     }
#
#     # MySQL Sessions
#     # mysql_sessions = get_mysql_sessions(mysql_db_params)
#     # print(f"Active MySQL Sessions: {mysql_sessions}")
#
#     # PostgreSQL Sessions
#     postgres_sessions = get_postgres_sessions(postgres_db_params)
#     print(f"Active PostgreSQL Sessions: {postgres_sessions}")
#
#     # SSH Sessions
#     # ssh_sessions = get_active_ssh_sessions()
#     # print(f"Active SSH Sessions: {ssh_sessions}")
#
#     # Nginx Active Connections
#     nginx_url = "http://localhost/nginx_status"  # URL for Nginx status page
#     nginx_sessions = get_nginx_active_connections(nginx_url)
#     print(f"Active Nginx Connections: {nginx_sessions}")
#
#
# # Main Execution Block
# if __name__ == "__main__":
#     monitor_server()
#
