import csv


def calculate_memory_cpu_average(file_path: str):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')

        average_memory = 0
        average_cpu = 0
        count = 0

        for row in csv_reader:
            if row[0] == 'id':
                continue
            average_memory += float(row[1])
            average_cpu += float(row[2])
            count += 1

        average_memory /= count
        average_cpu /= count

    return average_memory, average_cpu


def calculate_memory_cpu_averages(file_paths: [str]):
    memory_cpu_averages = []
    for file_path in file_paths:
        memory, cpu = calculate_memory_cpu_average(file_path)
        memory_cpu_averages.append((memory, cpu))

    with open('memory_cpu_averages_gs.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(memory_cpu_averages)


file_paths = [
    '../plots/2024-05-23_00-19-hsf-100/memory_cpu.csv',
    '../plots/2024-05-23_01-30-hsf-500/memory_cpu.csv',
    '../plots/2024-05-23_13-26-hsf-1000/memory_cpu.csv',
    '../plots/2024-05-23_16-51-hsf-100/memory_cpu.csv',
    '../plots/2024-05-23_20-01-hsf-500/memory_cpu.csv',
    '../plots/2024-05-23_20-28-hsf-1000/memory_cpu.csv',
    '../plots/2024-05-23_22-14-hsf-100/memory_cpu.csv',
    '../plots/2024-05-23_22-40-hsf-500/memory_cpu.csv',
    '../plots/2024-05-23_23-06-hsf-1000/memory_cpu.csv',
]

file_paths2=[
    '../plots/2024-05-23_14-31-gs-100/memory_cpu.csv',
    '../plots/2024-05-23_14-58-gs-500/memory_cpu.csv',
    '../plots/2024-05-23_16-22-gs-1000/memory_cpu.csv',
    '../plots/2024-05-23_20-54-gs-100/memory_cpu.csv',
    '../plots/2024-05-23_21-21-gs-500/memory_cpu.csv',
    '../plots/2024-05-23_21-47-gs-1000/memory_cpu.csv',
    '../plots/2024-05-23_23-32-gs-100/memory_cpu.csv',
    '../plots/2024-05-23_23-58-gs-500/memory_cpu.csv',
    '../plots/2024-05-24_00-23-gs-1000/memory_cpu.csv',

]

calculate_memory_cpu_averages(file_paths2)
