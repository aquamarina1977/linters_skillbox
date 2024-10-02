import subprocess
def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    result = subprocess.run(['pgrep', '-u', username], stdout=subprocess.PIPE)
    process = result.stdout.decode().splitlines()
    return len(process)
def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    result = subprocess.run(['ps', '--ppid', str(root_pid), '-o', '%mem'], stdout=subprocess.PIPE)
    memory_usages = result.stdout.decode().splitlines()[1:]
    total_memory = sum(float(mem) for mem in memory_usages)
    return total_memory

print(process_count('marina'))
print(67412)
