import Audio
import os
from watson_developer_cloud import ToneAnalyzerV3

def loadPoem():
    poem_name = input("Enter Poem name: ")
    cwd = os.getcwd()
    file_dir = cwd + "//Poems//" + poem_name + ".txt"
    try:
        f_open = open(file_dir)
        return f_open
    except IOError:
        print("Failed to load poem, please try again")
        exit()


def parsePoem(poem):
    count = 1
    stanza_num_to_text = dict()
    curr_stanza = ""
    for line in poem.splitlines(keepends=True):
        if line == "\n":
            stanza_num_to_text[count] = curr_stanza
            count += 1
            curr_stanza = ""
        else:
            curr_stanza += line
    if count not in stanza_num_to_text:
        stanza_num_to_text[count] = curr_stanza

    return stanza_num_to_text


def analyzeStanza(nums_to_response):
    nums_to_tone = dict()
    last_key = 0
    for key, val in nums_to_response.items():
        # Stanza_tones is a list of dictionaries where each internal dictionary represents a dominant tone within
        # the stanza and has the form {'score: float', 'tone_id' : str, 'tone_name' : str}
        # tone_id can be either: anger, fear, joy, and sadness (emotional tones); analytical, confident, and
        # tentative (language tones)
        stanza_tones = val.get('document_tone').get('tones')
        # Sentence_tones is a list of dictionaries where each internal dictionary represents a sentence(line)
        # within the given stanza and has the form: {'sentence_id' : int, 'text' : str, 'tones' : [{'score': float,
        # 'tone_id' : str, 'tone_name' : str} ... ]}
        sentence_tones = val.get('sentence_tones')

        if len(stanza_tones) == 0 or stanza_tones is None:
            nums_to_tone[key] = nums_to_tone.get(last_key)
            # TODO: gather stanza tone from internal sentences or simply skip this stanza's tone and apply previous
            # stanza's tone
        else:
            # for now only consider the most dominant tone
            nums_to_tone[key] = stanza_tones[0].get('tone_id')
            last_key = key
            # TODO: maybe consider more than the most dominant tone if more than one dominant tones in stanza
    return nums_to_tone

def analyzePoem(nums_to_stanzas):
    nums_to_response = dict()

    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        iam_apikey='YOUR API KEY_',
        url='YOUR URL'
    )
    # Loop through each stanza and query API for tone analysis response
    for key, val in nums_to_stanzas.items():
        response_code = 0
        tone_response = tone_analyzer.tone(
            {'text': val},
            'application/json'
        )

        # Wait until the API request returns an okay 200
        while response_code != 200:
            response_code = tone_response.get_status_code()

        tone_analysis = tone_response.get_result()
        # Map the response result to its corresponding stanza
        nums_to_response[key] = tone_analysis

    # Analyze the tone of each individual stanza
    results = analyzeStanza(nums_to_response)
    return results


def poemLoader(poem):
    # Maps stanza number to stanza text [1...n]
    nums_to_stanzas = parsePoem(poem)
    # Analyze the tones of the poem and map the dominant tone to stanza number
    num_to_tone = analyzePoem(nums_to_stanzas)
    # Combine nums_to_stanza and num_to_tone to a list of tuples:  [( string of stanza text,
    # string of dominant tone) ...]
    text_tone_list = []
    for key, val in nums_to_stanzas.items():
        text_tone_list.append((val, num_to_tone.get(key)))
    Audio.run(text_tone_list)

# a = """Do not go gentle into that good night,
# Old age should burn and rave at close of day;
# Rage, rage against the dying of the light.
#
# Though wise men at their end know dark is right,
# Because their words had forked no lightning they
# Do not go gentle into that good night.
#
# Good men, the last wave by, crying how bright
# Their frail deeds might have danced in a green bay,
# Rage, rage against the dying of the light.
#
# Wild men who caught and sang the sun in flight,
# And learn, too late, they grieved it on its way,
# Do not go gentle into that good night.
#
# Grave men, near death, who see with blinding sight
# Blind eyes could blaze like meteors and be gay,
# Rage, rage against the dying of the light.
#
# And you, my father, there on the sad height,
# Curse, bless, me now with your fierce tears, I pray.
# Do not go gentle into that good night.
# Rage, rage against the dying of the light."""
# poemLoader(a)