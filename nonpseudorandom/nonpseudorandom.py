import numpy as np
import hashlib
from ._sensors import SensorReader

sensor_reader = SensorReader()

def seed(a=None):
    if a is not None:
        np.random.seed(a)
    else:
        sensor_data = sensor_reader.read_sensors()
        random_seed = hash(sensor_data)
        np.random.seed(random_seed)

def random():
    seed()
    return np.random.random()

def randint(a, b):
    seed()
    return np.random.randint(a, b)

def choice(seq):
    seed()
    return np.random.choice(seq)

def shuffle(seq):
    seed()
    np.random.shuffle(seq)
    return seq

def sample(population, k):
    seed()
    return np.random.choice(population, k, replace=False).tolist()

def uniform(a, b):
    seed()
    return np.random.uniform(a, b)

def hash(obj):
    array_bytes = np.array(obj).tobytes()
    hash_object = hashlib.sha256(array_bytes)
    hash_digest = hash_object.hexdigest()
    hash_int = int(hash_digest, 16) % (2**32)
    return hash_int