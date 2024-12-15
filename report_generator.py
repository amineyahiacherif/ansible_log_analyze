#!/usr/bin/env python3

def format_duration(seconds):
    """Format duration in a human-readable format"""
    if seconds < 60:
        return f"{seconds:.2f} secondes"
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes} min {remaining_seconds:.2f} sec"

def generate_report(host_tasks):
    print("\nRapport d'exécution des tâches Ansible par hôte:")
    print("=" * 50)
    
    for host, tasks in host_tasks.items():
        print(f"\nHôte: {host}")
        print("-" * (len(host) + 6))
        
        total_time = 0
        skipped_tasks = 0
        executed_tasks = 0
        
        for task in tasks:
            status_symbol = "⏭️ " if task['status'] == 'skipped' else "✅ "
            print(f"\n{status_symbol}Tâche: {task['task']}")
            print(f"  Durée: {format_duration(task['duration'])}")
            print(f"  Début: {task['start_time'].strftime('%H:%M:%S')}")
            print(f"  Fin: {task['end_time'].strftime('%H:%M:%S')}")
            
            if task['status'] == 'skipped':
                skipped_tasks += 1
            else:
                executed_tasks += 1
                total_time += task['duration']
        
        print(f"\nRésumé pour {host}:")
        print(f"  Tâches exécutées: {executed_tasks}")
        print(f"  Tâches ignorées: {skipped_tasks}")
        print(f"  Temps total d'exécution: {format_duration(total_time)}")
        print("=" * 50)
