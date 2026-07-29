from cloudwatch_metrics import *

print("CPU:", get_cpu_usage(), "%")
print("Network In:", get_network_in(), "KB")
print("Network Out:", get_network_out(), "KB")
print("Status Check:", get_status_check())