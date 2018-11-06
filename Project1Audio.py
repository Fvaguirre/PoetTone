import pygame;
import win32com.client as wincl;
from time import sleep; 

globalPause = False;

def playStanza(stanza, tone, cont, end): 
    speak = wincl.Dispatch("SAPI.SpVoice");
    if (cont == False):
        if (pygame.mixer_music.get_busy()):
            pygame.mixer_music.fadeout(2000);
            sleep(2);
        pygame.mixer_music.load(tone);
        pygame.mixer_music.set_volume(.5);
        pygame.mixer_music.play();
        sleep(3);
    else: 
        if (False == pygame.mixer_music.get_busy()):
            pygame.mixer_music.rewind();

    if (globalPause == False):
        speakLine(stanza, speak);
    else: 
        pygame.mixer_music.pause();

    if (end):
        pygame.mixer_music.fadeout(2000);
        sleep(2);

def speakLine(line, speak):
    speak.Speak(line);

tones = {"Sad": "StillAlive.mp3", "Anger": "StillAlive.mp3"};

poem = [(\
"Nature's first green is gold, \
Her hardest hue to hold.", "Sad"),("\
Her early leaf's a flower; \
But only so an hour.", "Sad"),("\
Then leaf subsides to leaf,", "Anger"),(" \
So Eden sank to grief, \
So dawn goes down to day, \
Nothing gold can stay.", "Sad")];

def playPoem(poem): #expected that poem is an array in the form [(stanza, id), (stanza id), ...]. 
    for i in range(len(poem)):
         stanza = poem[i][0];
         tone = poem[i][1];
         if (i == 0):
             playStanza(stanza, tones[tone], False, False);
         elif (i == (len(poem)-1)):
               playStanza(stanza, tones[tone], (poem[i-1][1] == poem[i][1]), True);
         elif (poem[i][1] == poem[i-1][1]):
             playStanza(stanza, tones[tone], True, False);
         else:
             playStanza(stanza, tones[tone], False, False);

def run(poem):
    pygame.mixer.init();
    playPoem(poem);

run(poem);