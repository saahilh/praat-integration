import io
import base64
import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt

def draw_amplitude_for_sound(snd):
  fig = plt.figure()

  plt.plot(snd.xs(), snd.values.T)
  plt.xlim([snd.xmin, snd.xmax])
  plt.xlabel("time [s]")
  plt.ylabel("amplitude")

  return fig

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_intensity_for_sound(snd, spectogram=False):
  fig = plt.figure()
  if spectogram:
    spectrogram = snd.to_spectrogram()
    draw_spectogram(spectogram)
    plt.twinx()

  intensity = snd.to_intensity()

  plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
  plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
  plt.grid(False)
  plt.ylim(0)
  plt.ylabel("intensity [dB]")

  plt.xlim([snd.xmin, snd.xmax])

  return fig

def draw_pitch_for_sound(snd, spectogram=False):
  (PITCH_FLOOR, PITCH_CEIL) = (50, 200)
  pitch = snd.to_pitch()
  fig = plt.figure()
  
  if spectogram:
    # If desired, pre-emphasize the sound fragment before calculating the spectrogram
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)

    draw_spectrogram(spectrogram)
    plt.twinx()

  # Extract selected pitch contour, and replace unvoiced samples by NaN to not plot
  pitch_values = pitch.selected_array['frequency']
  pitch_values[pitch_values==0] = np.nan
  plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
  plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
  plt.grid(False)
  plt.ylim(PITCH_FLOOR, PITCH_CEIL)
  plt.ylabel("fundamental frequency [Hz]")
  plt.xlim([snd.xmin, snd.xmax])

  return fig

def create_encoded_image_for_figure(fig):
  png_image = io.BytesIO()
  FigureCanvas(fig).print_png(png_image)

  encoded_image_uri = "data:image/png;base64," + base64.b64encode(png_image.getvalue()).decode('utf8')

  return encoded_image_uri
