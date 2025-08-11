# What Could Go Wrong - AI Edition

This repository hosts the files used for the What Could Go Wrong? digital card game. Nikolas Martelaro and Wendy Ju developed and presented the game at a Workshop at AutoUI 2020. The game was then modified by Nik and his team at CMU to be more generalized for AI-based systems.

The digital card game can be loaded into and played on PlayingCards.io. Custom cards can be added using the `csv` files for `prompts` and `responses`

## Abstract
While AI has the potential to greatly improve our daily lives, there are also challenges and potential downsides to these systems. This game aims to foster discussions about the potential negative aspects of AI in hopes of surfacing challenges that should be considered during the design process rather than after deployment.

## Game Setup Instructions For playingcards.io
1. Download this repository
2. Go to https://playingcards.io/game/standard-deck and choose "Start a Blank Room"
3. Enter the virtual card table
4. Click the `Edit Table` icon in the green toolbard
5. Select `Room Options`
6. Select  `Import From File`
7. Upload `what-could-go-worng-av.pcio`
8. Click `Edit Table` to exit editing mode and go into gameplay mode

## Gameplay Instructions

### Setup
1. Each player draws 5 white response cards from their stack
2. Click the spinner to randomly choose the first Card Czar

### Each Round
1. **The Card Czar** draws a black prompt card and reads it aloud to the group
2. **All other players** select 1 white response card from their hand and place it face down in their designated slot
3. **The Card Czar** flips and reads each white response card out loud
4. **The Card Czar** chooses the response card they think best answers the prompt
5. **+1 point** goes to the player whose card was chosen
6. **Group Discussion**: The group discusses what else could go wrong based on the chosen card
   - Players can award **+1 point** to anyone who makes a good point during discussion
   - Discussion should last a few minutes
7. **Next Round**: The next player becomes the Card Czar
   - Click the "Deal" button to give each player a new white card
   - All players should have 5 cards in their hand at the start of each round

### Game Flow
- The role of Card Czar rotates clockwise around the table
- Continue playing until you decide to stop or run out of cards
- The player with the most points at the end wins!

### Important Notes
- **Take notes** on ideas you haven't thought about before
- **Don't worry about card categories** - some cards are causes, others are effects. Go where the discussion leads
- **Content warning**: Some cards may contain upsetting content (e.g., abuse, harm)
- **Take your time** - meaningful discussion is encouraged


### Video Demonstration
[![What could go wrong card game demonstration](https://img.youtube.com/vi/DlqgWnhEqoc/0.jpg)](https://youtu.be/DlqgWnhEqoc)

## Adding new cards
Edit the `prompts.csv` and `responses.csv` to add new cards to the decks. Follow instrcutions for adding new cards here: https://playingcards.io/docs/custom-decks

## Suggested Citation
Nikolas Martelaro and Wendy Ju. 2020. What Could Go Wrong? Exploring the Downsides of Autonomous Vehicles. In *12th International Conference on Automotive User Interfaces and Interactive Vehicular Applications* (*AutomotiveUI '20*). Association for Computing Machinery, New York, NY, USA, 99–101. DOI:https://doi.org/10.1145/3409251.3411734

### Bibtex
```@inproceedings{10.1145/3409251.3411734,  
author = {Martelaro, Nikolas and Ju, Wendy},  
title = {What Could Go Wrong? Exploring the Downsides of Autonomous Vehicles},  
year = {2020},  
isbn = {9781450380669},  
publisher = {Association for Computing Machinery},  
address = {New York, NY, USA},  
url = {https://doi.org/10.1145/3409251.3411734},  
doi = {10.1145/3409251.3411734},  
abstract = { While autonomous vehicles have the potential to greatly improve our daily lives, there are also challenges and potential downsides to these systems. In this workshop, we intend to foster discussions about the potential negative aspects of autonomous cars in hopes of surfacing challenges that should be considered during the design process rather than after deployment. We will spur these conversations through a review of participant position statements and through group discussion facilitated by a card game called “What Could Go Wrong?” Our goal is to consider the autonomous vehicle’s benefits—improving safety, increasing mobility, reducing emissions—against potential drawbacks. By identifying potential harms and downsides, the workshop attendees, and the AutoUI community more broadly can design well-considered solutions.},  
booktitle = {12th International Conference on Automotive User Interfaces and Interactive Vehicular Applications},  
pages = {99–101},  
numpages = {3},  
keywords = {game with a purpose, failure modes, autonomous vehicles},  
location = {Virtual Event, DC, USA},  
series = {AutomotiveUI '20}. 
}
```

For some motivation on why we want to develop new hazard analysis games.

```@article{martelaro2022exploring,
  title={Exploring Opportunities in Usable Hazard Analysis Processes for AI Engineering},
  author={Martelaro, Nikolas and Smith, Carol J and Zilovic, Tamara},
  journal={arXiv preprint arXiv:2203.15628},
  year={2022}
}
```



