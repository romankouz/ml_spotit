# "Spot It!" AI
A personal project that generates a Spot It environment for an AI to play against humans. The project has
3 objectives:
    1. Generate a "Spot It!" game of arbitrary size.
    2. Create a functioning UI on which the game can be played by both humans and an AI.
    3. Train an AI to play the game with a high degree of accuracy.

### December 23 - 26
- [ ] Place images on super pixels and calculate size ranges so that images appear within card boundaries.
- [ ] Add a lot of comments and cleanup to update_card() so that it's clear what code is doing.
- [ ] Write a backtracking algorithm to find the set of images that accurately creates a spot it game.

### Completed Column ✓
- [x] FIX AI's Side for Updating Middle Card (used + instead of - for x shift for AI) 
- [x] Add autoclicking modules to requirements.txt (using PyAutoGUI)
- [x] Add a lint that is applied before git commits. (using pylint)

### Bucket

- [ ] Insert a penalty if the model gets the guess wrong.
- [ ] Clean up np.where code and weird indexing. It makes it hard to read.
- [ ] Identify why player and AI buttons need to be destroyed but not common ones.
- [ ] Add docstrings for methods and classes.
- [ ] A lot of repeat arithmetic calculations should be saved in properly named variables.
- [ ] Find maximizing distance between k points with the constraint that they all must be within the circular boundary.