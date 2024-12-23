import numpy as np
import importlib.resources as pkg_resources
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import stft, istft
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from skimage import io, color, transform
import os

def read_audio_file(file_path):
    # Use pydub to read the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Convert to mono if the audio has multiple channels
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    # Convert to 16-bit PCM format
    audio = audio.set_sample_width(2)
    
    # Get the sample rate and samples
    sample_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())
    
    return sample_rate, samples, audio

def text_to_image(text, font_paths=["NotoSerifCJK.ttc","NotoSans-Regular.ttf"], font_size=20, image_path='message_image.png'):
    """
    Render text with fallback font support for multiple languages.

    :param text: The text to render.
    :param font_paths: A list of font paths to try in order (fallback mechanism).
    :param font_size: Size of the font.
    :param image_path: Path to save the generated image.
    """
    # Create a drawing object
    font_objects = []
    for font_name in font_paths:
        with pkg_resources.open_binary('spectoconvo.fonts', font_name) as font_file:
            font_objects.append(ImageFont.truetype(font_file, font_size))
    
    # Measure text size using the first font
    text_bbox = font_objects[0].getbbox(text)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Create a new image
    image = Image.new('RGB', (text_width + 20, text_height + 20), 'white')
    draw = ImageDraw.Draw(image)

    # Draw text with fallback support
    x, y = 10, 10
    for char in text:
        for font in font_objects:
            try:
                # Try rendering the character with the current font
                draw.text((x, y), char, font=font, fill='black')
                # Measure the size of the character
                char_bbox = draw.textbbox((x, y), char, font=font)
                char_width = char_bbox[2] - char_bbox[0]
                x += char_width
                break  # Exit font loop if the character was rendered successfully
            except OSError:
                continue

    # Save the image
    image.save(image_path)

def plot_inverted_image(image_path='output_image.png'):
    # Load the image
    image = io.imread(image_path)
    gray_image = color.rgb2gray(image)

    # Flip the image vertically
    gray_image = np.flipud(gray_image)

    # Invert the grayscale image
    grey_image = np.abs(-1 * (gray_image - 1))

    return grey_image

def add_message_to_spectrogram(sound_file, message, inital_spectrum_image, output_sound_file, output_spectrogram_file,start_freq=20*10**3,scale_freq=0,scale_time=0,intensity=1e-5,bitrate="320k"):
    # Read the sound file
    text_to_image(message)
    sample_rate, samples,original_audio = read_audio_file(sound_file)
    
    # Convert to mono if the audio has multiple channels
    if samples.ndim > 1:
        # Process each channel separately
        channels = [samples[:, i] for i in range(samples.shape[1])]
    else:
        # Single channel audio
        channels = [samples]

    # Initialize lists to store results for each channel
    all_modified_samples = []

    for channel in channels:
        # Generate the STFT for the channel
        nperseg = 4096
        noverlap = nperseg // 2
        frequencies, times, Zxx = stft(channel, sample_rate, nperseg=nperseg, noverlap=noverlap)

        # Convert the complex STFT result to magnitude
        Sxx = np.abs(Zxx)
        # Avoid log of zero by adding a small constant
        Sxx += 1e-10
    


    
        # Plot the original spectrogram
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud', cmap='inferno')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        
        # Add the message to the spectrogram

        # Save the original spectrogram image
        plt.savefig(inital_spectrum_image)
        plt.close()
    
        # Encode the message into the spectrogram
        message_encoded = np.array([ord(char) for char in message])
        message_encoded = np.pad(message_encoded, (0, Sxx.shape[1] - len(message_encoded)), 'constant')
        
        # Find the index corresponding to 20kHz
        freq_index = np.argmin(np.abs(frequencies - start_freq))
        
        # Load and process the image
        grey_image = plot_inverted_image('message_image.png')

        
        # Resize the grey_image to match the desired range in Sxx
        if scale_freq==0:
            scale_freq= Sxx.shape[0] - freq_index
        if scale_time==0:
            scale_time= Sxx.shape[1]
        freq_range =  scale_freq # Number of frequency bins to use
        time_range = scale_time# Number of time bins to use
        grey_image_resized = transform.resize(grey_image, (freq_range, time_range))
        
        # Embed the grey_image into the spectrogram
        Sxx[freq_index:freq_index + freq_range, :time_range] += grey_image_resized * np.max(Sxx) * intensity  # Adjust the intensity

        # Convert the modified spectrogram back to time domain
        _, modified_samples = istft(Sxx * np.exp(1j * np.angle(Zxx)), sample_rate, nperseg=nperseg, noverlap=noverlap)

        # Normalize the modified samples to avoid clipping
        modified_samples = np.int16(modified_samples / np.max(np.abs(modified_samples)) * 32767)

        # Store the modified samples
        all_modified_samples.append(modified_samples)

    # Combine the modified samples for all channels
    if len(all_modified_samples) > 1:
        modified_samples = np.stack(all_modified_samples, axis=-1)
    else:
        modified_samples = np.array(all_modified_samples[0], ndmin=2).T  # Ensure 2D array

    # Save the modified sound file as WAV
    wavfile.write('temp_output.wav', sample_rate, modified_samples)

    # Determine the output file format
    output_format = os.path.splitext(output_sound_file)[1][1:]

    # Convert the modified WAV file to the desired output format
    modified_audio = AudioSegment.from_wav('temp_output.wav')
    if output_format == 'mp3':
        modified_audio.export(output_sound_file, format=output_format, bitrate=bitrate)
    else:
        modified_audio.export(output_sound_file, format=output_format)

    # Remove the temporary WAV file
    os.remove('temp_output.wav')
    # Generate the spectrogram of the modified audio for the first channel (you can modify this to plot all channels if needed)
    frequencies, times, Zxx = stft(modified_samples[:, 0], sample_rate, nperseg=nperseg, noverlap=noverlap)
    Sxx = np.abs(Zxx)

    # Avoid log of zero by adding a small constant
    Sxx += 1e-10

    # Plot the spectrogram of the modified audio
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud', cmap='inferno')
    plt.colorbar(label='Intensity [dB]')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    
    # Save the spectrogram image of the modified audio
    plt.savefig(output_spectrogram_file)
    plt.close()

    return scale_freq, scale_time
def decode(sound_file, image_path):
    # Read the sound file
    sample_rate, samples,original_audio = read_audio_file(sound_file)

    # Convert to mono if the audio has multiple channels
    if samples.ndim > 1:
        samples = np.mean(samples, axis=1)

    # Generate the STFT
    nperseg = 4096
    noverlap = nperseg // 2
    frequencies, times, Zxx = stft(samples, sample_rate, nperseg=nperseg, noverlap=noverlap)

    # Convert the complex STFT result to magnitude
    Sxx = np.abs(Zxx)

    # Avoid log of zero by adding a small constant
    Sxx += 1e-10

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud', cmap='inferno')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar(label='Intensity [dB]')
    plt.savefig(image_path)
    plt.close()
    print(f'{image_path} saved')
