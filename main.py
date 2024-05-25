from runs.RunDetection import RunDetection

if __name__ == '__main__':
    run_detection = RunDetection('inputData/new_dataset_with_labels.csv', 'inputData/labels/anomaly_labels.csv',
                                 approach='local_outlier_factor')

    try:
        run_detection.run()
    except KeyboardInterrupt:
        run_detection.stop()
        print('Exiting...')
