import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy import signal

noise_initial = np.random.normal(0, 0.1, size=len(np.linspace(0, 10, 1000)))

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise):
    if show_noise:
        return amplitude * np.sin(2 * np.pi * frequency * t + phase) + noise
    else:
        return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def update(val):
    amp = amp_slider.val
    freq = freq_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_cov = noise_cov_slider.val
    show_noise = check.get_status()[0]
    

    y = harmonic_with_noise(t, amp, freq, phase, noise_mean, noise_cov, show_noise, noise_initial)
    l.set_ydata(y)
    fig.canvas.draw_idle()

def reset_noise(val):
    amp = amp_slider.val
    freq = freq_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_cov = noise_cov_slider.val
    show_noise = check.get_status()[0]
    
    noise = np.random.normal(noise_mean, np.sqrt(noise_cov), size=len(t))
    global noise_initial
    noise_initial = noise
    y = harmonic_with_noise(t, amp, freq, phase, noise_mean, noise_cov, show_noise, noise)
    l.set_ydata(y)
    fig.canvas.draw_idle()


def reset(event):
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_cov_slider.reset()
    check.set_active(True)

# Generate time values
t = np.linspace(0, 10, 1000)
# Generate initial data
amp_initial = 1.0
freq_initial = 1.0
phase_initial = 0.0
noise_mean_initial = 0.0
noise_cov_initial = 0.1
y_initial = harmonic_with_noise(t, amp_initial, freq_initial, phase_initial, noise_mean_initial, noise_cov_initial, True, noise_initial)

# Create plot
fig, ax = plt.subplots()
l, = ax.plot(t, y_initial)

# Create sliders
amp_slider_ax = plt.axes([0.1, 0.02, 0.65, 0.03])
amp_slider = Slider(amp_slider_ax, 'Amplitude', 0.1, 2.0, valinit=amp_initial)
amp_slider.on_changed(update)

freq_slider_ax = plt.axes([0.1, 0.06, 0.65, 0.03])
freq_slider = Slider(freq_slider_ax, 'Frequency', 0.1, 2.0, valinit=freq_initial)
freq_slider.on_changed(update)

phase_slider_ax = plt.axes([0.1, 0.1, 0.65, 0.03])
phase_slider = Slider(phase_slider_ax, 'Phase', 0, 2*np.pi, valinit=phase_initial)
phase_slider.on_changed(update)

noise_mean_slider_ax = plt.axes([0.1, 0.14, 0.65, 0.03])
noise_mean_slider = Slider(noise_mean_slider_ax, 'Noise Mean', -1, 1, valinit=noise_mean_initial)
noise_mean_slider.on_changed(reset_noise)

noise_cov_slider_ax = plt.axes([0.1, 0.18, 0.65, 0.03])
noise_cov_slider = Slider(noise_cov_slider_ax, 'Noise Covariance', 0.01, 1, valinit=noise_cov_initial)
noise_cov_slider.on_changed(reset_noise)

# Create checkbox
check_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
check = CheckButtons(check_ax, ['Show Noise'], [True])
check.on_clicked(update)

# Create reset button
reset_ax = plt.axes([0.8, 0.1, 0.1, 0.04])
button = Button(reset_ax, 'Reset')
button.on_clicked(reset)

plt.show()