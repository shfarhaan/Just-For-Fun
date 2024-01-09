import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pywt

def fft_analysis(signal):
    fft_result = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal))
    return freq, np.abs(fft_result)

def cwt_analysis(signal):
    cwt_result, frequencies = pywt.cwt(signal, scales=np.arange(1, 128), wavelet='cmor')
    return cwt_result, frequencies

def main():
    st.title("Fourier Analysis App")

    # Sidebar
    st.sidebar.header("Settings")
    signal_type = st.sidebar.radio("Select Signal Type", ("Sinusoidal", "Custom"))
    
    time = np.linspace(0, 1, 1000)
    
    num_components = st.sidebar.slider("Number of Signal Components", 1, 5, 1)
    signal_components = []

    for i in range(num_components):
        freq = st.sidebar.slider(f"Frequency of Component {i + 1}", 1, 10, 5)
        amplitude = st.sidebar.slider(f"Amplitude of Component {i + 1}", 1.0, 5.0, 1.0)
        phase = st.sidebar.slider(f"Phase of Component {i + 1}", 0.0, 2 * np.pi, 0.0)

        component = amplitude * np.sin(2 * np.pi * freq * time + phase)
        signal_components.append(component)

    signal = np.sum(signal_components, axis=0)
    

    # Main content
    st.header("Time-Domain Signal")

    if signal_type == "Sinusoidal":
        frequency = st.slider("Select Sinusoidal Frequency", 1, 10, 5)
        time = np.linspace(0, 1, 1000)
        signal = np.sin(2 * np.pi * frequency * time)
    else:
        st.info("Enter your custom time-domain signal below.")
        custom_signal = st.text_area("Custom Signal (comma-separated values)", "1, 2, 3, 2, 1")
        signal = np.array([float(val) for val in custom_signal.split(",")])

    st.line_chart(signal)

    # Fourier Analysis
    st.header("Fourier Analysis")

    fft_freq, fft_magnitude = fft_analysis(signal)
    st.line_chart(pd.DataFrame({"Frequency": fft_freq, "Magnitude": fft_magnitude}))

    # Continuous Wavelet Transform (CWT) Analysis
    st.header("Continuous Wavelet Transform (CWT) Analysis")

    cwt_result, cwt_freq = cwt_analysis(signal)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(np.abs(cwt_result), aspect='auto', extent=[0, len(signal), cwt_freq[-1], cwt_freq[0]])
    ax.set_title('Continuous Wavelet Transform Analysis')
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
