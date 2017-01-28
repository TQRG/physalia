import csv


class Measurement:
    """Class for with energy measurement information

    Attributes:
        timestamp               When the execution started.
        use_case                Key identifier of the use case.
        device_model            Device where the measurements were performed.
        duration                Time it takes to execute the use case.
        energy_consumption_mean Mean of the measurements.
        energy_consumption_std  Standard deviation of the measurements.
        energy_consumption_n    Sample size of measurements.
    """

    csv_storage = "./db.csv"

    def __init__(
        self,
        timestamp,
        use_case,
        device_model,
        duration,
        energy_consumption_mean,
        energy_consumption_std,
        energy_consumption_n
    ):
        self.persisted = False
        self.timestamp = timestamp
        self.use_case = use_case
        self.device_model = device_model
        self.duration = duration
        self.energy_consumption_mean = energy_consumption_mean
        self.energy_consumption_std = energy_consumption_std
        self.energy_consumption_n = energy_consumption_n

    def persist(self):
        """ Store measurement in the database."""
        if self.persisted:
            return False
        else:
            with open(self.csv_storage, 'wb') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([
                    self.timestamp,
                    self.use_case,
                    self.device_model,
                    self.duration,
                    self.energy_consumption_mean,
                    self.energy_consumption_std,
                    self.energy_consumption_n,
                ])
            return True
