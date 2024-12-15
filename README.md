# MusicToasts 🎶

**Discover interesting facts about the song you're listening to with a simple toast notification!**

Did you know that _"Bohemian Rhapsody"_ by _Queen_ was initially called "The Cowboy Song"?  
Or that _"Rolling in the Deep"_ by _Adele_ was inspired by a dream where her house burned down?  
Or that the guitar solo in _"Hotel California"_ by _Eagles_ was recorded in a bathroom for its reverb effect?   
<small>(at least that's what the AI says...)</small>

**Curious to learn more about the song currently playing?**  
_**MusicToasts**_ displays a toast notification with song details (title and artist) and album art (if available) when a
new track starts playing on your computer.
It also offers a fun fact about the song, generated by AI, and an "ask me anything about this song" button for
further information!

## Demo

Initial toast:  
<img src="demo/Cover%20Art%20-%20The%20Line.png" width="250"></img>

Fun fact:  
<img src="demo/Fun%20Fact%20-%20The%20Line.png" width="250"></img>

Ask a question:  
<img src="demo/Ask%20-%20The%20Line%20(1).png" width="250"></img>
<img src="demo/Ask%20-%20The%20Line%20(2).png" width="250"></img>

Lyrics:  
<img src="demo/Lyrics%20-%20Macarena.png" width="250"></img>  
You can view the full lyrics by hovering with the mouse over the toast:
<img src="demo/Lyrics%20-%20Forever%20Young.png" width="450"></img>  

Error toast:  
<img src="demo/Error%20-%20AI%20Configuration.png" width="250"></img>

## Features

- [x] Display a toast with song details (title and artist) as it starts playing.
- [x] Show the album art (if available).
- [x] Provide a fun fact about the song, generated by AI.
- [x] Include an "ask me anything about this song" button, powered by AI.
- [x] Show a dedicated error toast for issues (e.g., missing/invalid API key).

## Installation

### Requirements

- Windows >= 10
- Python >= 3.8
- Only works with apps that support the Windows 10 Media Session API (e.g., Windows Media Player, Spotify, Browser +
  Spotify Web, etc.)

### Setup

1. Clone the repository.
    ``` bash
    git clone https://github.com/Adioffer/MusicToasts
    ```

1. Install the dependencies.
    ``` bash
    pip install -r requirements.txt
    ```

### Configuration

1. Configure environment variables (example below).
    ``` bash
    set MT_AI_ENDPOINT_URL=https://api.deepseek.com/chat/completions
    set MT_AI_API_KEY=sk-xxx
    set MT_AI_MODEL=deepseek-chat
    ```
   (use setx for permanent changes).

   I recommend using DeepSeek model, as it is (almost) state-of-the-art, and 2 bucks can get you about 50K requests.

## Usage

1. Run the application.
    ``` bash
    python src\main.py
    ```

## Misc

### License

MIT. Just please don't sue me.

### Acknowledgements

[windows-toasts](https://github.com/DatGuy1/Windows-Toasts),
[winsdk](https://pypi.org/project/winsdk/),
[MusicBrainz](https://musicbrainz.org/),
[CoverArtArchive](https://coverartarchive.org/),
[LyricsOvh](https://lyricsovh.docs.apiary.io/).

### Contributing

This project was a fun POC for me, and I do not plan to continue working on it.  
Your contributions are welcomed! Please check the Backlog section for missing features.  

### Support

Consider buying me a coffee (latte, 1 tsp sugar) if you like my work.

### Backlog

- [ ] General - use async networking (aiohttp instead of requests) when possible
- [ ] General - destroy toast objects when no longer needed
- [ ] Lyrics toast - find a better way to display long texts
- [ ] Lyrics toast - switch to a more reliable data source
- [ ] Validate the operating system at startup
- [ ] Support additional operating systems
- [ ] Create a [custom AUMID](https://windows-toasts.readthedocs.io/en/latest/custom_aumid.html) to allow customized
  toast titles and icons
- [ ] Add instructions for running the app as a service.
- [ ] Add --configure option
- [ ] Generate a wheel package and upload it to PyPI
- [ ] Add GitHub actions for CI/CD
