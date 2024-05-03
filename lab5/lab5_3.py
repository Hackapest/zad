import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, CheckboxGroup, Select
from bokeh.plotting import figure
from scipy.signal import butter, lfilter

noise_initial = np.random.normal(0, 0.1, size=len(np.linspace(0, 10, 1000)))

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise=None):
    if show_noise:
        return amplitude * np.sin(2 * np.pi * frequency * t + phase) + noise
    else:
        return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def median_filter(signal, window_size):
    filtered_signal = []
    half_window = window_size // 2

    for i in range(len(signal)):
        window = sorted(signal[max(0, i - half_window): min(len(signal), i + half_window + 1)])
        median_value = window[len(window) // 2]
        filtered_signal.append(median_value)

    return filtered_signal

initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
initial_cutoff_frequency = 1.0
initial_window_size = 3

t = np.arange(0.0, 10.0, 0.01)
sampling_frequency = len(t) / (t[-1] - t[0])

signal = harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase,
                             initial_noise_mean, initial_noise_covariance, True, noise_initial)
filtered_signal = median_filter(signal, initial_window_size)

source = ColumnDataSource(data=dict(t=t, signal=signal, filtered_signal=filtered_signal))

plot = figure(title="Graph of harmonic with noise", height=300, width=600, y_range=(-3, 3))
line = plot.line('t', 'signal', source=source, line_width=3, line_alpha=0.6, color='red')
scatter = plot.scatter('t', 'signal', source=source, size=3, color='red', alpha=0.6, visible=False)

plot_filtered = figure(title="Filtered harmonic", height=300, width=600, y_range=(-3, 3))
line_filtered = plot_filtered.line('t', 'filtered_signal', source=source, line_width=3, line_alpha=0.6, color='blue')
scatter_filtered = plot_filtered.scatter('t', 'filtered_signal', source=source, size=3, color='blue', alpha=0.6, visible=False)

amplitude_slider = Slider(start=0.1, end=10.0, value=initial_amplitude, step=0.1, title="Amplitude")
frequency_slider = Slider(start=0.1, end=10.0, value=initial_frequency, step=0.1, title="Frequency")
phase_slider = Slider(start=0, end=2*np.pi, value=initial_phase, step=0.1, title="Phase")
noise_mean_slider = Slider(start=-1.0, end=1.0, value=initial_noise_mean, step=0.1, title="Noise Mean")
noise_covariance_slider = Slider(start=0.0, end=1.0, value=initial_noise_covariance, step=0.01, title="Noise Covariance")
cutoff_slider = Slider(start=0.1, end=5.0, value=initial_cutoff_frequency, step=0.1, title="Cutoff Frequency")
window_size_slider = Slider(start=3, end=21, value=initial_window_size, step=2, title="Window Size")

show_noise_checkbox = CheckboxGroup(labels=["Show Noise"], active=[0])

plot_type_select = Select(title="Plot Type:", value="Line", options=["Line", "Scatter"])

noise = noise_initial  # Initialize with the initial noise

def update_data(attrname, old, new):
    new_signal = harmonic_with_noise(t, amplitude_slider.value, frequency_slider.value, phase_slider.value,
                                     noise_mean_slider.value, noise_covariance_slider.value, 0 in show_noise_checkbox.active, noise)
    new_filtered_signal = median_filter(new_signal, window_size_slider.value)
    source.data = dict(t=t, signal=new_signal, filtered_signal=new_filtered_signal)
    
    if plot_type_select.value == "Line":
        line.visible = True
        scatter.visible = False
        line_filtered.visible = True
        scatter_filtered.visible = False
    elif plot_type_select.value == "Scatter":
        line.visible = False
        scatter.visible = True
        line_filtered.visible = False
        scatter_filtered.visible = True

for widget in [amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider, cutoff_slider, window_size_slider]:
    widget.on_change('value', update_data)

def show_noise_checkbox_changed(attrname, old, new):
    global noise
    if 0 in new:  # If "Show Noise" is selected
        noise = np.random.normal(0, 0.1, size=len(np.linspace(0, 10, 1000)))
    else:
        noise = np.zeros_like(t)  # Set noise to zeros
    update_data(None, None, None)

show_noise_checkbox.on_change('active', show_noise_checkbox_changed)

reset_button = Button(label="Reset", button_type="success")

def reset():
    amplitude_slider.value = initial_amplitude
    frequency_slider.value = initial_frequency
    phase_slider.value = initial_phase
    noise_mean_slider.value = initial_noise_mean
    noise_covariance_slider.value = initial_noise_covariance
    cutoff_slider.value = initial_cutoff_frequency
    update_data(None, None, None)

reset_button.on_click(reset)

adjust_noise_button = Button(label="Adjust Noise", button_type="primary")

def adjust_noise():
    global noise
    noise = np.random.normal(noise_mean_slider.value, noise_covariance_slider.value, size=len(np.linspace(0, 10, 1000)))
    if 0 not in show_noise_checkbox.active:  # If "Show Noise" is not selected
        noise = np.zeros_like(t)  # Set noise to zeros
    update_data(None, None, None)

adjust_noise_button.on_click(adjust_noise)

controls = column(amplitude_slider, frequency_slider, phase_slider, noise_mean_slider, noise_covariance_slider,
                  cutoff_slider, window_size_slider, show_noise_checkbox, reset_button, adjust_noise_button, plot_type_select)

curdoc().add_root(row(column(plot, plot_filtered), controls))
curdoc().title = "Lab5"
