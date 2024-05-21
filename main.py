from runs.RunDetection import RunDetection

if __name__ == '__main__':
    run_detection = RunDetection('./inputData/smooth_dataset_with_anomalies_smooth.csv',
                                 approach='half_space_trees')

    try:
        run_detection.run()
    except KeyboardInterrupt:
        run_detection.stop()
        print('Exiting...')
