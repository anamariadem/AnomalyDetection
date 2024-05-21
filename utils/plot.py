import matplotlib.pyplot as plt
import datetime
import os


def plot_detection_results(processed_tuples):
    print(len(processed_tuples))
    heart_rate_scores = []
    systolic_blood_pressure_scores = []
    diastolic_blood_pressure_scores = []
    temperature_scores = []
    respiratory_rate_scores = []
    glucose_scores = []
    oxygen_saturation_scores = []

    for processing_tuple in processed_tuples:
        if not processing_tuple.anomaly_scores:
            continue

        heart_rate_scores.append(processing_tuple.anomaly_scores['heart_rate'])
        systolic_blood_pressure_scores.append(processing_tuple.anomaly_scores['systolic_blood_pressure'])
        diastolic_blood_pressure_scores.append(processing_tuple.anomaly_scores['diastolic_blood_pressure'])
        temperature_scores.append(processing_tuple.anomaly_scores['temperature'])
        respiratory_rate_scores.append(processing_tuple.anomaly_scores['respiratory_rate'])
        glucose_scores.append(processing_tuple.anomaly_scores['glucose'])
        oxygen_saturation_scores.append(processing_tuple.anomaly_scores['oxygen_saturation'])

    print(heart_rate_scores)

    plot_anomaly_scores(heart_rate_scores, label='heart_rate')
    plot_anomaly_scores(systolic_blood_pressure_scores, label='systolic_blood_pressure')
    plot_anomaly_scores(diastolic_blood_pressure_scores, label='diastolic_blood_pressure')
    plot_anomaly_scores(temperature_scores, label='temperature')
    plot_anomaly_scores(respiratory_rate_scores, label='respiratory_rate')
    plot_anomaly_scores(glucose_scores, label='glucose')
    plot_anomaly_scores(oxygen_saturation_scores, label='oxygen_saturation')


def plot_anomaly_scores(ano_scores, label):
    plt.plot(ano_scores, label=label)
    plt.axhline(y=0.9, color='r', linestyle='--', label='Threshold 0.9')
    plt.legend()

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    directory = f'plots/{current_datetime}'
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory,  f'{label}.png')
    plt.savefig(file_path)

    plt.show()
