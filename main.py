from runs.RunDetection import RunDetection
from config.config import FILE_PATH, LABELS_FILE_PATH

if __name__ == '__main__':
    run_detection = RunDetection(FILE_PATH, LABELS_FILE_PATH)

    try:
        run_detection.run()
    except KeyboardInterrupt:
        run_detection.stop()
        print('Exiting...')
