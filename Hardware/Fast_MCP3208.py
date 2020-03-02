from mcp3208 import MCP3208
import time
from statistics import mean, pvariance

SAMPLES = 10000

adc = MCP3208()

data_photo = [None]*SAMPLES
data_diode = [None]*SAMPLES
start = time.monotonic()

# Read the same channel over and over
for i in range(SAMPLES):
    data_photo[i] = adc.read(0)
    data_diode[i] = adc.read(1)
end = time.monotonic()
total_time = end - start
# for i in range (0, len(data_photo)):
    # print('{}, {}\n'.format(data_photo[i], data_diode[i]))
print("mean: {}, var: {}.", mean(data_photo), pvariance(data_photo))
print("Time of capture: {}s".format(total_time))
print("Actual sample rate={}".format(2*SAMPLES / total_time))