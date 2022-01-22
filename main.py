import pandas.io.excel
import wget as wget
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.speech_to_text_v1 import SpeechToTextV1
from pandas import json_normalize
from ibm_watson import LanguageTranslatorV3


url_s2t = "{{Url_speech_to_text}}"
url_lt="{{Url_traslate}}"
apikey_lt='{{apiKey-Tl}}'
iam_apikey_s2t = "{{apiKey_ST}}"
version_lt='2018-05-01'
filename='path file audio'
model='{{language code example en-es/en-Fr}}'
model="en-es"
def speechToText():
    authenticator = IAMAuthenticator(iam_apikey_s2t)
    s2t = SpeechToTextV1(authenticator=authenticator)
    s2t.set_service_url(url_s2t)
    with open(filename, mode="rb") as wav:
        response = s2t.recognize(audio=wav, content_type='audio/mp3')
    response.result
    json_normalize(response.result['results'], "alternatives")
    recognized_text = response.result['results'][0]["alternatives"][0]["transcript"]
    return recognized_text

def traslate(recognized_text,model):
    authenticator = IAMAuthenticator(apikey_lt)
    language_translator = LanguageTranslatorV3(version=version_lt, authenticator=authenticator)
    language_translator.set_service_url(url_lt)
    json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")
    translation_response = language_translator.translate(text=recognized_text, model_id=model)
    translation = translation_response.get_result()
    spanish_translation = translation['translations'][0]['translation']
    print(spanish_translation )


traslate(speechToText(),model)