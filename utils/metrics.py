import os
import psutil

from models.PatientVitalsTuple import PatientVitalsTuple


def set_metrics(processing_tuple: PatientVitalsTuple):
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15 / os.cpu_count()) * 100

    processing_tuple.set_cpu_percentage(cpu_usage)
    processing_tuple.set_memory_percentage(psutil.virtual_memory().percent)