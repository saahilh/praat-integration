import parselmouth
import seaborn as sns

from flask import Flask
from flask import render_template


from helpers import create_encoded_image_for_figure
from helpers import draw_amplitude_for_sound
from helpers import draw_intensity_for_sound
from helpers import draw_pitch_for_sound

app = Flask(__name__)

@app.route("/")
def read_sound():
    snd = parselmouth.Sound("backend/sound/untitled.wav")
    # fig = draw_amplitude_for_sound(snd)
    # fig = draw_intensity_for_sound(snd)
    fig = draw_pitch_for_sound(snd)
    
    return render_template("image.html", image=create_encoded_image_for_figure(fig))
