import csv
import datetime

from models.PatientVitalsTuple import PatientVitalsTuple


def save_anomaly_score_to_csv(data: list[PatientVitalsTuple]):
    filtered_data = filter(lambda x: len(x.anomaly_scores) > 0, data)
    anomaly_scores = [x.anomaly_scores for x in filtered_data]
    heading = anomaly_scores[0].keys()
    data = [x.values() for x in anomaly_scores]

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    directory = f'plots/{current_datetime}'
    file_name = f'{directory}/anomaly_scores.csv'

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(heading)
        writer.writerows(data)

