# import librosa
# import numpy as np

# def load_audio(file_path, sr=None):
#     """Load an audio file.

#     Args:
#         file_path (str): Path to the audio file.
#         sr (int, optional): Sample rate. If None, uses the original sample rate.

#     Returns:
#         Tuple[np.ndarray, int]: The audio time series and the sample rate.
#     """
#     audio, sample_rate = librosa.load(file_path, sr=sr)
#     return audio, sample_rate

# def extract_spectrogram(audio, sample_rate):
#     """Extract the spectrogram from an audio signal.

#     Args:
#         audio (np.ndarray): The audio time series.
#         sample_rate (int): The sample rate of the audio.

#     Returns:
#         np.ndarray: The spectrogram of the audio signal.
#     """
#     spectrogram = librosa.stft(audio)
#     spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram))
#     return spectrogram_db

# def noise_reduction(audio, noise_factor=0.05):
#     """Reduce noise from the audio signal.

#     Args:
#         audio (np.ndarray): The audio time series.
#         noise_factor (float): The factor by which to reduce noise.

#     Returns:
#         np.ndarray: The noise-reduced audio signal.
#     """
#     noise = np.random.randn(len(audio))
#     audio_noisy = audio + noise_factor * noise
#     return audio_noisy
