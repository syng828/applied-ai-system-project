## Original project
The project was originally a music recommender system. Based on their preferences such as with the genre, mood, and energy, the system recommends some songs that match those categories the closest.

## Title and Introduction
Music Recommender with Stats
The project does continue to recommend music, however it also gives the confidence and margin between songs as a result. This will allow users to see how close the song is to their preferences while also getting diverse songs.

## Architecture
The architecture of the project is displayed below:
![New project architecture](/assets/images/updated_architecture.png)

The user taste profile is used as the input, then the retriever gets songs from songs.csv, the scorer creates a ranking and the automated tester runs. Both of these go into the reliability layer where it will output the top k recommendations, an explanation, and a reliability report. What was added to this project is the reliability report and there is also a human review component where they can review low confidence songs. 

## Setup
Create a virtual environment (optional but recommended):

```
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```

Install dependencies
```
pip install -r requirements.txt
```

Run the app:
```
python -m src.main
```
Running Tests
Run the starter tests with:
```
pytest
```
You can add more tests in tests/test_recommender.py.

## Sample Interactions
1. User Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

#1  Sunrise City by Neon Echo
    Score : 2.98
    Why   : genre match (+1.0); mood match (+1.0); energy closeness (+0.98); reliability: confidence=0.99; margin=1.02; fallback=off

#2  Rooftop Lights by Indigo Parade
    Score : 1.96
    Why   : mood match (+1.0); energy closeness (+0.96); reliability: confidence=0.65; margin=0.09; fallback=off

#3  Gym Hero by Max Pulse
    Score : 1.87
    Why   : genre match (+1.0); energy closeness (+0.87); reliability: confidence=0.62; margin=0.88; fallback=off

#4  Sunset Groove by Velvet Frame
    Score : 0.99
    Why   : energy closeness (+0.99); reliability: confidence=0.33; margin=0.07; fallback=off

#5  Glass Horizon by North Circuit
    Score : 0.92
    Why   : energy closeness (+0.92); reliability: confidence=0.31; margin=0.92; fallback=off


2. User Preferences: {'genre': 'rock', 'mood': 'sad', 'energy': 0.3} 

#1  Storm Runner by Voltline
    Score : 1.39
    Why   : genre match (+1.0); energy closeness (+0.39); reliability: confidence=0.46; margin=0.41; fallback=on

#2  Spacewalk Thoughts by Orbit Bloom
    Score : 0.98
    Why   : energy closeness (+0.98); reliability: confidence=0.33; margin=0.03; fallback=on

#3  Library Rain by Paper Lanterns
    Score : 0.95
    Why   : energy closeness (+0.95); reliability: confidence=0.32; margin=0.02; fallback=on

#4  Coffee Shop Stories by Slow Stereo
    Score : 0.93
    Why   : energy closeness (+0.93); reliability: confidence=0.31; margin=0.01; fallback=on

#5  Winter Canvas by Aria Vale
    Score : 0.92
    Why   : energy closeness (+0.92); reliability: confidence=0.31; margin=0.92; fallback=on


3. User Preferences: {'genre': 'jazz', 'mood': 'relaxed', 'energy': 0.5}

#1  Coffee Shop Stories by Slow Stereo
    Score : 2.87
    Why   : genre match (+1.0); mood match (+1.0); energy closeness (+0.87); reliability: confidence=0.96; margin=1.91; fallback=off

#2  Old Pine Road by Maple Transit
    Score : 0.96
    Why   : energy closeness (+0.96); reliability: confidence=0.32; margin=0.04; fallback=off

#3  Midnight Coding by LoRoom
    Score : 0.92
    Why   : energy closeness (+0.92); reliability: confidence=0.31; margin=0.03; fallback=off

#4  Late Train Home by Velvet Frame
    Score : 0.89
    Why   : energy closeness (+0.89); reliability: confidence=0.30; margin=0.04; fallback=off

#5  Library Rain by Paper Lanterns
    Score : 0.85
    Why   : energy closeness (+0.85); reliability: confidence=0.28; margin=0.85; fallback=off

## Design Decisions
As stated in the previous project, the genre, mood, and energy are of equal weights to ensure that non conventional songs would show up regardless of their genre. I decided to add the confidence and margin to truly see how close the song is to a user preferences. For instance, the first and last example have fairly high confidence because of how close it is to their preferences while the second example has low confidence because of how different the genre, mood, and energy are together. The tradeoff with this is that it may add complexity for a user who does not know what confidence is, but this can be offset by creating a UI and a percentage that shows how close it matches their preferences. Additionally, the margin is between songs and when low it recommends other genres to give more varied songs, especially when the model is not very confident.

## Testing
There are 8 tests as described below:
1. Verifies ranking quality for pop/happy/high-energy songs
2. Calls explain_recommendation for a song and asserts that it is not blank
3. Verifies artists diversity, that it will return 2 different artists when both are high scoring
4. Tests that the confidence and margin are returned
5. Verifies margin are computer per selected song (For this one, it originally computed it globally)
6. Added an empty input test
7. Added tie/fallback behavior (this test failed intially, but the desired output is the 1st and 3rd song, because the fallback should trigger from low margin and so returns the more diverse genre)
8. Added wrong input type for numeric field, expected to return ValueError

## Reflection
I learned a lot about how effective AI can be used to generate code and also explain it. I wanted the song results to be more descriptive so it generated the confidence/margin/fallback system. I think overall it made me realize how many ways there are to create unique solutions.

8 out of 8 tests passed, and confidence was high around 0.8 for conventional songs, but turned on fallback for similar songs

The limitations of this system is that it is not very good at generating songs that are not typical. I think that the AI could be misused if someone intentionally generates incorrect song statistics which would mess with the result. I think what surprised me is that the AI is not always right like it had to change its own test but Im also surprised with how well everything works. So an instance where the AI generated something correct is its suggestion to have confidence and margin and it did the calculation quite well, but it did incorrectly made a test result.

## Demo
https://www.loom.com/share/3d7ee61e9993497cb24abfe08f2800b0
