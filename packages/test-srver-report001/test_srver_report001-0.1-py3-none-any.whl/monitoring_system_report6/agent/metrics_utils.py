from lib2to3.fixes.fix_input import context

import psutil
import time
import os


def collect_metrics():
    """Collect system metrics."""
    cpu_usage = psutil.cpu_percent(interval=1)
    # cpu_current_freq = psutil.cpu_freq().min
    memory = psutil.virtual_memory()
    load_avg = psutil.getloadavg()
    cpu_count = psutil.cpu_count()
    cpu_times = psutil.cpu_times()
    thread_count = psutil.Process().num_threads()
    cpu_user_times = cpu_times.user
    cpu_idle_times = cpu_times.idle
    cpu_system_times = cpu_times.system
    cpu_io_wait = cpu_times.iowait
    cpu_nice = cpu_times.nice
    memory_usage = memory.percent

    # Resource consumption

    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    disk_usage = psutil.disk_usage('/')
    voluntary_context_switching = psutil.Process().num_ctx_switches().voluntary
    involuntary_context_switching = psutil.Process().num_ctx_switches().involuntary

    total_used_memory = ((virtual_memory.used + swap_memory.used) /
     (virtual_memory.total + swap_memory.total)) * 100
    total_used_disk =(disk_usage.used /disk_usage.total) * 100



    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        # "cpu_current_freq":cpu_current_freq,
        "1_min_load_avg":load_avg[0],
        "5_min_load_avg":load_avg[1],
        "15_min_load_avg":load_avg[2],
        "cpu_count":cpu_count,
        # "cpu_user_time":cpu_times.user,
        # "cpu_system_time":round(cpu_times.system,2),
        # "cpu_idle_time":round(cpu_times.idle,2),
        "cpu_user_times":cpu_user_times,
        "thread_count":thread_count,
        "virtual_memory":virtual_memory.used,
        "total_used_memory":round(total_used_memory, 2),
        "total_used_disk":round(total_used_disk, 2),
        "voluntary_context_switching":voluntary_context_switching,
        "involuntary_context_switching":involuntary_context_switching,
        "cpu_idle_times":cpu_idle_times,
        "cpu_system_times":cpu_system_times,
        "cpu_io_wait":cpu_io_wait,
        "cpu_nice":cpu_nice



    }


# print("-----------------resourse consumption-----------------")
    # print("disk usage",psutil.disk_usage('/'))
    # print("network usage",psutil.net_io_counters())
