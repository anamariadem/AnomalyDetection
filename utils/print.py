from models.PatientVitalsTuple import PatientVitalsTuple


def print_anomaly_scores(processing_tuple: PatientVitalsTuple):
    print("{:<8} {:<15}".format('Key', 'Score'))
    for key, result in processing_tuple.anomaly_scores.items():
        print("{:<8} {:<15}".format(key, result))
    print('\n')
