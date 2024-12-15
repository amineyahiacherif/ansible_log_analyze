#!/usr/bin/env python3

import re
import json
from datetime import datetime
from collections import defaultdict

def parse_ansible_log(log_file):
    # Dictionary to store execution times per host
    host_tasks = defaultdict(list)
    
    try:
        with open(log_file, 'r') as f:
            current_task = None
            start_time = None
            
            for line in f:
                # Try to parse the line as JSON
                try:
                    data = json.loads(line)
                    
                    # Get timestamp
                    timestamp_str = data.get('timestamp', '')
                    if timestamp_str:
                        current_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    
                    # Task started
                    if data.get('event') == 'playbook_on_task_start':
                        current_task = data.get('name', 'Unknown task')
                        start_time = current_time
                    
                    # Task completed
                    elif data.get('event') == 'runner_on_ok' and current_task and start_time:
                        host = data.get('host', 'Unknown host')
                        duration = (current_time - start_time).total_seconds()
                        
                        host_tasks[host].append({
                            'task': current_task,
                            'duration': duration
                        })
                        
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"Error processing line: {e}")
                    continue
                    
        return host_tasks
    
    except FileNotFoundError:
        print(f"Error: File {log_file} not found")
        return None

def display_results(host_tasks):
    print("\nAnsible Task Execution Times by Host:")
    print("=====================================")
    
    for host, tasks in host_tasks.items():
        print(f"\nHost: {host}")
        print("-" * (len(host) + 6))
        
        total_time = 0
        for task in tasks:
            print(f"Task: {task['task']}")
            print(f"Duration: {task['duration']:.2f} seconds\n")
            total_time += task['duration']
        
        print(f"Total execution time for {host}: {total_time:.2f} seconds")
        print("=" * 50)

def main():
    log_file = input("Enter the path to your Ansible log file: ")
    host_tasks = parse_ansible_log(log_file)
    
    if host_tasks:
        display_results(host_tasks)

if __name__ == "__main__":
    main()
