import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pywt

# Define time outside of the main function
time = np.linspace(0, 1, 1000)

def fft_analysis(signal):
    fft_result = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal))
    return freq, np.abs(fft_result)

def cwt_analysis(signal):
    cwt_result, frequencies = pywt.cwt(signal, scales=np.arange(1, 128), wavelet='cmor')
    return cwt_result, frequencies

def main():
    st.title("Explore Signals with Fourier Analysis")
    
    
    # Custom style for fixed sidebar
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            position: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Introduction", "Where do we use Fourier Analysis?", "Time-Domain Signal Analysis"])

    if page == "Introduction":
        st.markdown(
            """
            # **Introduction**
            
            Fourier Analysis is a powerful tool used to understand the different components
            that make up a signal. In simple terms, it helps us break down a signal into its
            individual frequencies.

            This app allows you to visualize and analyze signals, helping you understand how
            different frequencies contribute to the overall signal.
            
            ## **Why Fourier Analysis?**

            Fourier Analysis is crucial in understanding signals because it allows us to decompose
            complex signals into simpler frequency components. Here are some key reasons why Fourier
            Analysis is important:

            1. **Identifying Frequency Components:** Helps in identifying the individual frequencies
               present in a signal, which is essential in various fields such as signal processing,
               communication, and audio analysis.

            2. **Filtering and Noise Removal:** Enables the removal of unwanted frequency components
               through filtering, helping to isolate and enhance specific aspects of the signal.

            3. **Transforming between Time and Frequency Domains:** Facilitates the transformation
               between time and frequency domains, providing valuable insights into the characteristics
               of a signal.

            This Streamlit application empowers you to interactively explore and visualize the effects
            of different frequency components on time-domain signals.
            
            
            """
        )

    elif page == "Where do we use Fourier Analysis?":
        st.markdown(
            """
            Fourier analysis is used in various fields to understand and analyze complex signals or functions. Here are some key reasons why and where Fourier analysis is employed:

            1. **Frequency Decomposition:**
            
            **Signal Decomposition:** Fourier analysis helps break down a complex signal into its individual frequency components. This is crucial in understanding the different harmonic contributions that make up a signal.

            2. **Frequency Spectrum Representation:**
            
            **Frequency Spectrum Visualization:** It provides a clear representation of the frequency spectrum of a signal, showing the amplitude and phase information associated with each frequency component.

            3. **Filtering and Signal Processing:**
            
            **Filter Design:** Fourier analysis is used to design filters that can isolate or remove specific frequency components from a signal.
            
            **Signal Enhancement:** By filtering out unwanted frequencies, it can enhance the relevant components of a signal.

            4. **Data Compression:**
            
            **Data Compression Techniques:** In data compression, Fourier analysis is used to transform time-domain data into the frequency domain. This transformation often leads to more efficient compression techniques.

            5. **Communication Systems:**
            
            **Modulation and Demodulation:** In communication systems, Fourier analysis is crucial for understanding modulation and demodulation processes. It helps analyze the frequency content of modulated signals.

            6. **Physics and Engineering:**
            
            **Vibration Analysis:** In physics and engineering, Fourier analysis is used to analyze vibrations and study the resonant frequencies of structures.
            
            **Spectral Analysis:** It is applied in fields such as acoustics, electromagnetics, and optics to analyze spectral characteristics.

            7. **Medical Imaging:**
            
            **Magnetic Resonance Imaging (MRI):** Fourier analysis is fundamental in medical imaging techniques like MRI, where signals are transformed between the spatial and frequency domains.

            8. **Audio and Music Processing:**
            
            **Audio Signal Processing:** Fourier analysis is extensively used in audio processing, helping in tasks like equalization, filtering, and spectral analysis of sound signals.

            9. **Control Systems:**
            
            **Control System Analysis:** Fourier analysis is employed in control system analysis to study the frequency response of systems.

            10. **Quantum Mechanics:**
            
            **Quantum Mechanics:** In quantum mechanics, Fourier transforms are used to switch between position and momentum representations of wave functions.

            In summary, Fourier analysis provides a valuable tool for understanding the frequency content of signals and has applications in a wide range of scientific, engineering, and technological fields. It allows researchers and practitioners to gain insights into the behavior of complex systems and signals in both time and frequency domains.
                            
            """
        )

    elif page == "Time-Domain Signal Analysis":
        st.header("Time-Domain Signal Analysis")

        # Sidebar
        st.sidebar.header("Settings")
        signal_type = st.sidebar.radio("Select Signal Type", ("Sinusoidal", "Custom"))

        # Reset button
        if st.sidebar.button("Reset"):
            st.experimental_rerun()

        # Main content
        st.header("Time-Domain Signal")

        if signal_type == "Sinusoidal":
            frequency = st.sidebar.slider("Select Sinusoidal Frequency", 1, 10, 5)
            signal = np.sin(2 * np.pi * frequency * time)
        else:
            st.info("Adjust your custom time-domain signal from the side bar.")
            st.markdown(
                """
                ### Customizing the Time-Domain Signal in the Sidebar

                The sidebar customization allows you to interactively choose or customize the time-domain signal that you want to analyze. Here's a breakdown of the customization options:

                #### Sinusoidal Signal

                If you select "Sinusoidal" as the signal type, the app generates a simple sinusoidal signal. You can customize the frequency of this sinusoidal signal using a slider in the sidebar. Adjust the "Select Sinusoidal Frequency" slider to set the frequency of the sine wave. The resulting sinusoidal signal is displayed in the chart.

                #### Custom Signal

                If you choose "Custom" as the signal type, the app provides more flexibility. You can adjust a custom time-domain signal by specifying its components in the sidebar. Here are the customization options:

                1. **Number of Signal Components:** Use the "Number of Signal Components" slider to specify how many frequency components you want to include in your custom signal.

                2. **Frequency, Amplitude, and Phase of Each Component:** For each component, sliders are available to set the frequency, amplitude, and phase. Adjust the sliders for "Frequency of Component," "Amplitude of Component," and "Phase of Component" to define the characteristics of each frequency component.

                3. **Generated Custom Signal:** The app dynamically generates a custom signal based on the specified components. The resulting time-domain signal, composed of the sum of these components, is displayed in the chart.

                Feel free to experiment with these settings to observe how changes in frequency, amplitude, and phase affect the appearance of the time-domain signal.

                """
            )
            num_components = st.sidebar.slider("Number of Signal Components", 1, 5, 1)
            signal_components = []

            for i in range(num_components):
                freq = st.sidebar.slider(f"Frequency of Component {i + 1}", 1, 10, 5)
                amplitude = st.sidebar.slider(f"Amplitude of Component {i + 1}", 1.0, 5.0, 1.0)
                phase = st.sidebar.slider(f"Phase of Component {i + 1}", 0.0, 2 * np.pi, 0.0)

                component = amplitude * np.sin(2 * np.pi * freq * time + phase)
                signal_components.append(component)

            signal = np.sum(signal_components, axis=0)

        st.line_chart(pd.DataFrame({"Signal": signal}))

        st.markdown(
            """
            The chart above represents the time-domain signal you've provided. If you selected a
            sinusoidal signal, it shows a smooth wave. If you entered a custom signal, it displays
            the values you specified over time.
            """
        )

        # Fourier Analysis
        st.header("Fourier Analysis")

        fft_freq, fft_magnitude = fft_analysis(signal)
        st.line_chart(pd.DataFrame({"Frequency": fft_freq, "Magnitude": fft_magnitude}))

        st.markdown(
            """
            The chart above shows how much of each frequency is present in your signal. 
            Higher peaks indicate stronger contributions from specific frequencies.
            """
        )

        # Continuous Wavelet Transform (CWT) Analysis
        st.header("Continuous Wavelet Transform (CWT) Analysis")

        cwt_result, cwt_freq = cwt_analysis(signal)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(np.abs(cwt_result), aspect='auto', extent=[0, len(signal), cwt_freq[-1], cwt_freq[0]])
        ax.set_title('Continuous Wavelet Transform Analysis')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

        st.markdown(
            """
            The image above represents how different frequencies change over time in your signal. 
            Brighter areas indicate higher energy in those frequency components at specific times.
            """
        )

if __name__ == "__main__":
    main()
