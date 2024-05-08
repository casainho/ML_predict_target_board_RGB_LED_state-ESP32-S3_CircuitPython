from ulab import numpy as np

# FIR filter designed with
# http://t-filter.appspot.com

# sampling frequency: 100 Hz

# * 0 Hz - 10 Hz
#   gain = 1
#   desired ripple = 0.001 dB
#   actual ripple = 0.0005032249393132639 dB

# * 30 Hz - 50 Hz
#   gain = 0
#   desired attenuation = -200 dB ()
#   actual attenuation = -203.29965109480193 dB

#define FILTER_TAP_NUM 45

filter_taps = np.array([
  6.320404326560145e-7,
  0.0000058397832746043805,
  0.00002306676607224123,
  0.00004241710368398302,
  -0.000005121423654635227,
  -0.00021592857491835733,
  -0.00048206393638285105,
  -0.0002598209582533281,
  0.0009789706655159837,
  0.0024198578468301885,
  0.0014330439666907675,
  -0.0035676224108471743,
  -0.008454484931413993,
  -0.004308362841950119,
  0.011398975609101742,
  0.023652710927404178,
  0.008848795837500015,
  -0.03385212353681059,
  -0.06132884794086225,
  -0.013366215773437874,
  0.12326611130762029,
  0.27944200642793704,
  0.34862736013685025,
  0.27944200642793704,
  0.12326611130762029,
  -0.013366215773437874,
  -0.06132884794086225,
  -0.03385212353681059,
  0.008848795837500015,
  0.023652710927404178,
  0.011398975609101742,
  -0.004308362841950119,
  -0.008454484931413993,
  -0.0035676224108471743,
  0.0014330439666907675,
  0.0024198578468301885,
  0.0009789706655159837,
  -0.0002598209582533281,
  -0.00048206393638285105,
  -0.00021592857491835733,
  -0.000005121423654635227,
  0.00004241710368398302,
  0.00002306676607224123,
  0.0000058397832746043805,
  6.320404326560145e-7
])

class Filter:
  def __init__(self):
    self.len_filter_taps = len(filter_taps)
    self.history = np.zeros(self.len_filter_taps)  # Initialize history with zeros
    self.last_index = 0
    self.samples = np.array([])
    
  def add_new_sample(self, new_sample):
    filtered_value = self.put(new_sample)  # Call put and store the result
    self.samples = np.concatenate((self.samples, np.array([filtered_value])))

  def put(self, input):
    self.history[self.last_index] = input  # Update history with new input
    self.last_index = (self.last_index + 1) % self.len_filter_taps  # Circular indexing
    
    acc = 0
    index = self.last_index
    for i in range(self.len_filter_taps):
      # Circular indexing for filter taps
      index = (index - 1) % self.len_filter_taps if index != 0 else self.len_filter_taps - 1
      acc += self.history[index] * filter_taps[i]
    return acc

  def get(self):
    # This function might be useful if you need the filtered value 
    # elsewhere in your code without calling put first. 
    acc = 0
    index = self.last_index
    for i in range(self.len_filter_taps):
        index = (index - 1) % self.len_filter_taps if index != 0 else self.len_filter_taps - 1
        acc += self.history[index] * filter_taps[i]
    return acc

  def get_end_stats(self):
    mean = np.mean(self.samples)
    median = np.median(self.samples)
    std = np.std(self.samples)
    self.samples = np.array([])
    return mean, median, std