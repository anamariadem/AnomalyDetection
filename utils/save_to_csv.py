import csv
import datetime

from models.PatientVitalsTuple import PatientVitalsTuple


def save_to_csv(file_name: str, data: list[list]):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def filter_and_map_data(data: list[PatientVitalsTuple], field: str):
    filtered_data = filter(lambda x: len(x[field]) > 0, data)
    field_data = [x[field] for x in filtered_data]
    heading = field_data[0].keys()
    values = [x.values() for x in field_data]

    return [heading] + values


def save_metrics_to_csv(data: list[PatientVitalsTuple]):
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    directory = f'plots/{current_datetime}'

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
