# ![Logo.png](https://raw.githubusercontent.com/fvaguirre/PoetTone/master/icon.png)PoetTone 

PoetTone is an application that enhances poetry. With PoetTone poetry is given sound! PoetTone uses IBM Watson's [ToneAnalyzer](https://www.ibm.com/watson/services/tone-analyzer/) to analyze a poem's tone by stanza and then match a musical piece to each stanza. The selected poem is then read aloud using Microsoft Speech Engine [Text-to-Speech](https://www.microsoft.com/en-us/download/details.aspx?id=27224) while the application plays the musical piece that matched the poem's tone(s)!

## Architecture
![Architecture.png](https://raw.githubusercontent.com/fvaguirre/PoetTone/master/PoetToneArchitecture.png)

## Setting Up
1. Install Python 3
2. Install pip
3. Install dependencies using pip
4. Install the fonts (Double click the two font files in the Fonts folder)
5. Input your personal IBM Watson ToneAnalyzer API key and URL in loader.py
6. Run the PoetTone.sh shell script or "python PoetToneGui.py" after cd'ing to the folder in cmd

## Dependencies
1. Python 3
2. IBM Watson Developer Cloud
3. Pygame
4. PyWin32
5. Windows OS

## Using PoetTone
1. Click on the "Select a Poem!" dropdown menu to select a poem from the Poems folder.
2. Click on the "Change Poem" button to start reading the poem.
3. You can import a poem into the Poems folder and click on "Reset Poems" to read a custom poem.
4. When clicking on Change Poem during a current reading of a poem, please wait for the reading of the current stanza to finish, and the program will automatically begin playing the next poem afterwards.

## Music Credits
> Story by Meydän - http://freemusicarchive.org/music/Meydan/Havor/10-_Story_1090<br/>
> Arrival of the Ghosts by Dee Yan-Key - http://freemusicarchive.org/music/Dee_Yan-Key/just_a_dream/03--Dee_Yan-Key-Arrival_of_the_Ghosts <br/>
> Inexplicable Fear by Alex Mason - http://freemusicarchive.org/music/Alex_Mason/Red_Numbers/05_1625<br/>
> The Gray Forest - II The Trap by Aitua - http://freemusicarchive.org/music/Aitua/Elements/13_The_Gray_Forest_-_II_The_Trap<br/>
> Elements - III Blue Sky by Aitua - http://freemusicarchive.org/music/Aitua/Elements/08_Elements_-_III_Blue_Sky<br/>
> fastlife by Ketsa - http://freemusicarchive.org/music/Ketsa/1111_vol_1_1795/07fastlifebyKetsa<br/>
> Insomnia Pt. 2 by Meydän - http://freemusicarchive.org/music/Meydan/For_Creators/Insomnia_Pt_2<br/>
**All Music was unmodified from source**