from gtts import gTTS
import os

def text_to_speech(text, filename='output.mp3', lang='en'):
    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)

        # Save the audio file
        tts.save(filename)
        
        # Optionally, play the generated speech
        # os.system(f'start {filename}')  # Uncomment this line if you want to play the speech immediately

        return True
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        return False

# Example usage:
text_to_speech("Face not recognized", filename='face_not_recognize.mp3', lang='en')
