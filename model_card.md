# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

I chose Vibify 2.0, combining Spotify and Vibe Coding and added the confidence and margin feature.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration   

The recommendations suggests 5 songs, based on genre, mood, and energy. It is for classroom exploration more as there are only 16 songs.IT assumes that the user wants to listen to a variety of songs because it will recommend other genres if the margin between two song recommendations are small.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

So it uses genre, energy, and mood, so it would only consider that. The weights are as follows: 
genre match: +1.0 points
mood match: +1.0 point
energy similarity: up to +1.0 point based on how close the song's energy is to the user's target

From the starter logic the genre had 2.0 points but it was too heavy so it switched to 1.0 points.

The added code is that it also measures the confidence of how well it fits the user preferences. 

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

There are 16 songs in the catalog, and genres include pop, lofi, rock, ambient, jazz, synthwave, indiepop, electronic, classical, funk, folk, metal, and soul. The moods are happy, chill, intense, relaxed, moody, focused, energized, complementative, groovy, wistful, aggressive, and warm. I added 6 new songs which was given by the AI and it has a larger range of genres and moods. There appears to be a wide range of music tastes in the dataset but there are too few for some of them, especially the later genres and moods that were added.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The user types it gives reasonable results is Happy Pop and Chill Lofi, which is because they go hand in hand. So songs like that would be captured correctly, and this is where it matched my intution. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Some limitations include that there are little songs with mid-range energy, with a 0.23 spread which makes it meaningless. Additionally, there are no songs with "sad" and negative valnece mood. There are no partial credit for adjacent genres such as indie pop vs pop. Lofi has the greatest amount of songs and lastly some of the fields are just completely ignored like valence and such. The scoring system would favor users that have more songs with a certain genre or mood or energy like Chill Lofi.
Another limitation is that it can give low confidence songs if the songs are not typical in terms of genre, mood, and energy.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

I tested 4 user profiles.
First is Happy Pop and from that I would have expected Sunrise City to appear first which it did.

Next is Sad Rock which I would have expected Storm Runner to go first because of its genre and it did. However, I did not expect Spacewalk Thoughts to appear since ambient songs are very different from rock, but based on the energy it does make sense. 

Next is Relaxed Jazz which I would have expected Coffee Shop Stories to appear first which it did because it had a lot of matches. Overall, this one matched the most because there are a lot of slow songs in the songs list.

Lastly is Intense Lofi which is interesting that it chose Storm Runner first since its a rock song. However, it does make sense based on the mood and energy match. It did change from before where genre had a 2.0 weight and now changed to 1.0 and it previously suggested Lofi songs more.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I think some additional features would include having partial genres, such as pop being considered for indie pop. I would also include the other categories like acousticness and valence. Another thing I would do is add recommendations based on what other users preferred which would imrpove the diversity. As for complex user tastes, I would have to include more songs which don't match the usual type of songs like the genre and mood not matching.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

In the recommender system I learned about the concept of weights. I think it was interesting seeing the results for unconventional preferences like lofi and intense, and it made me realize that music recommendation apps have to go through a lot of testing to make it good. The biggest learning moment in my project, is looking through the results and realizing that the AI would not always produce the best results. The AI tool helped me with writing down the code quickly, but I needed to double check stuff like how the weights work or the commit message which was very general. Its surprising that a simple weighting system can provide recommendations because I would have thought that it would require lots of calculations. To extend this project further, I would include recommendations from other users that popular music streaming apps use as well.
