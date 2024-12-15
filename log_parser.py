#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from collections import defaultdict

def parse_timestamp(line):
    """Extract and parse timestamp from log line without using strptime"""
    timestamp_match = re.match(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}),(\d{3})', line)
    if timestamp_match:
        year, month, day, hour, minute, second, msec = map(int, timestamp_match.groups())
        return datetime(year, month, day, hour, minute, second) + timedelta(milliseconds=msec)
    return None

def parse_host(line):
    """Extract host from log line"""
    host_match = re.search(r'\[([\w.-]+)\]', line)
    if host_match:
        return host_match.group(1)
    return None

def parse_task_name(line):
    """Extract task name from log line"""
    task_match = re.search(r'TASK \[(.*?)\]', line)
    if task_match:
        return task_match.group(1)
    return None

def parse_ansible_log(log_file):
    host_tasks = defaultdict(list)
    current_task = None
    start_time = None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                timestamp = parse_timestamp(line)
                if not timestamp:
                    continue

                # Détection du début d'une tâche
                task_name = parse_task_name(line)
                if task_name:
                    current_task = task_name
                    start_time = timestamp
                    continue

                # Détection de la fin d'une tâche
                host = parse_host(line)
                if host and current_task and start_time:
                    if 'ok:' in line or 'changed:' in line or 'skipping:' in line:
                        duration = (timestamp - start_time).total_seconds()
                        status = 'skipped' if 'skipping:' in line else 'ok'
                        
                        host_tasks[host].append({
                            'task': current_task,
                            'duration': duration,
                            'status': status,
                            'start_time': timestamp,
                            'end_time': timestamp
                        })

        return host_tasks
    except FileNotFoundError:
        print(f"Erreur: Fichier {log_file} non trouvé")
        return None
