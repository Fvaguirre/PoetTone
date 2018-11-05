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


def parsePoem(file):
    count = 1
    stanza_num_to_text = dict()
    curr_stanza = ""
    for line in file:
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
    for key, val in nums_to_response.items():
        # Stanza_tones is a list of dictionaries where each internal dictionary represents a dominant tone within
        # the stanza and has the form {'score: float', 'tone_id' : str, 'tone_name' : str}
        stanza_tones = val.get('document_tone').get('tones')
        # Sentence_tones is a list of dictionaries where each internal dictionary represents a sentence(line)
        # within the given stanza and has the form: {'sentence_id' : int, 'text' : str, 'tones' : [{'score': float,
        # 'tone_id' : str, 'tone_name' : str} ... ]}
        sentence_tones = val.get('sentence_tones')

        if len(stanza_tones) == 0:
             count = len(sentence_tones)
            # TODO: gather stanza tone from internal sentences or simply skip this stanza's tone and apply previous
            # stanza's tone
        else:
            # for now only consider the most dominant tone
            nums_to_tone[key] = stanza_tones[0].get('tone_id')
            # TODO: maybe consider more than the most dominant tone if more than one dominant tones in stanza
    return nums_to_tone

def analyzePoem(nums_to_stanzas):
    nums_to_response = dict()

    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        iam_apikey='Your API key',
        url='Your URL'
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


if __name__ == '__main__':
    # Open the selected poem and load into file
    file = loadPoem()
    # Maps stanza number to stanza text [1...n]
    nums_to_stanzas = parsePoem(file)
    # Close the opened file
    file.close()
    # Analyze the tones of the poem and map the dominant tone to stanza number
    num_to_tone = analyzePoem(nums_to_stanzas)
    print(num_to_tone)


