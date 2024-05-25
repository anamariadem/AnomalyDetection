import csv
import datetime

from models.PatientVitalsTuple import PatientVitalsTuple


def save_to_csv(file_name: str, data: list[list]):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def filter_and_map_data(data: list[PatientVitalsTuple], field: str):
    filtered_data = filter(lambda x: len(x[field]) > 0, data)

    ids = []
    field_data = []

    for item in filtered_data:
        ids.append(item['id'])
        field_data.append(item[field])

    heading = ['id'] + list(field_data[0].keys())
    # values = [x.values() for x in field_data]
    values = []

    for id, x in zip(ids,field_data):
        values.append([id] + list(x.values()))

    return [heading] + values


def save_metrics_to_csv(data: list[PatientVitalsTuple], approach: str, window_size: int, threshold: float):
    print('Saving metrics to CSV...')
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    directory = f'plots/{current_datetime}'

    # write information about the approach
    with open(f'{directory}/info.txt', 'w') as file:
        file.write(f'Approach: {approach}\n')
        file.write(f'Window size: {window_size}\n')
        file.write(f'Threshold: {threshold}\n')

    data_to_save = filter_and_map_data(data, 'anomaly_scores')
    file_name = f'{directory}/anomaly_scores.csv'
    save_to_csv(file_name, data_to_save)

    data_to_save = filter_and_map_data(data, 'auc_scores')
    file_name = f'{directory}/auc_scores.csv'
    save_to_csv(file_name, data_to_save)

    data_to_save = filter_and_map_data(data, 'precision_scores')
    file_name = f'{directory}/precision_scores.csv'
    save_to_csv(file_name, data_to_save)

    data_to_save = filter_and_map_data(data, 'recall_scores')
    file_name = f'{directory}/recall_scores.csv'
    save_to_csv(file_name, data_to_save)

    tuples = [('id', 'memory_percentage', 'cpu_percentage')]
    for item in data:
        id = item['id']
        memory = item['memory_percentage']
        cpu = item['cpu_percentage']

        if memory > 0 and cpu > 0:
            tuples.append([id, memory, cpu])

    file_name = f'{directory}/memory_cpu.csv'
    save_to_csv(file_name, tuples)
    print('Metrics saved to CSV.')