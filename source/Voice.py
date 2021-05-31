import random
import time
import speech_recognition as sr
from gtts import gTTS
import os

class Voice:
    def __init__(self):
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
    

    def recognize_speech_from_mic(self):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                successful
        "error":   `None` if no error occured, otherwise a string containing
                an error message if the API could not be reached or
                speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = self.recognizer.recognize_google(audio, language="fr-FR")
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response


    def speak_from_text(self, text):
        # Language in which you want to convert
        language = 'fr'
          
        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        # have a high speed
        myobj = gTTS(text=text, lang=language, slow=False)
          
        # Saving the converted audio in a mp3 file named
        # welcome 
        myobj.save("last_speech.mp3")
          
        # Playing the converted file
        os.system("mpg321 last_speech.mp3")


    def detect_room_in_text(self, text):
        for i in range(len(text)):
            if text[i].isdigit():
                i_begin = i
                for j in range(i+1, len(text)):
                    if not(text[j].isdigit()):
                        i_end = j
                    i_end = len(text)
                    return int(text[i_begin:i_end])
        return None


if __name__=="__main__":
    v = Voice()
    print("Speak !")
    guess=v.recognize_speech_from_mic()
    if guess["success"] and not guess["error"]:
        text = guess["transcription"]
        print(text)
        room = v.detect_room_in_text(text)
        if room:
            v.speak_from_text("C'est parti pour la salle F" + str(room))
        else:
            v.speak_from_text("Je n'ai pas compris, ou voulez-vous aller ?")
    else:
        v.speak_from_text("Je crois que je n'ai rien compris")
