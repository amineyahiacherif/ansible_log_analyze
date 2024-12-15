#!/usr/bin/env python3

from log_parser import parse_ansible_log
from report_generator import generate_report

def main():
    log_file = input("Entrez le chemin du fichier de log Ansible: ")
    host_tasks = parse_ansible_log(log_file)
    
    if host_tasks:
        generate_report(host_tasks)

if __name__ == "__main__":
    main()
