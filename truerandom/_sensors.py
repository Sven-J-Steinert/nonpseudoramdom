import psutil
import numpy as np
import cv2
import sounddevice as sd

class SensorReader:
    def __init__(self):
        self.available_sensors = self.detect_sensors()

    def detect_sensors(self):
        sensors = {}
        if hasattr(psutil, "sensors_temperatures") and psutil.sensors_temperatures():
            sensors['cpu_temp'] = self.read_cpu_temp
        if sd.query_devices():
            sensors['mic_noise'] = self.read_microphone_noise
        if self.is_webcam_available():
            sensors['webcam_noise'] = self.read_webcam_noise
        return sensors

    def read_cpu_temp(self):
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                return entry.current
        return None

    def read_microphone_noise(self, duration=1):
        sample_rate = 44100
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        noise = np.std(recording)
        return noise

    def is_webcam_available(self):
        cap = cv2.VideoCapture(0)
        available = cap.isOpened()
        cap.release()
        return available

    def read_webcam_noise(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        noise = np.std(gray_frame)
        return noise

    def read_sensors(self):
        sensor_data = []
        for sensor_name, sensor_func in self.available_sensors.items():
            data = sensor_func()
            if data is not None:
                sensor_data.append(data)
        return sensor_data
