# OSRS AUTOBOT

## FUTURE FEATURES

### QUESTION HANDLER v2

- new question handler for random events (currently pause and screenshot)
- spell/grammar check on question detected
- if new push to LLM/answer-bot?

### HEALTH CHECK

- Log HP - constant check of hp
- when low - invoke reset of some kind.
    - reset involves teleporting by typing ::edge or some other teleport 
    - or clicking to a certain location like a fixed fountain
    - then clicking back into place on the stall
    - Other options: eat food, drink potion, halt & alarm, or dzone only fountain

### HARD RESET

- might involve the above but also logging out and back in
- might involve restarting the script or client if a serious error or process fault is detected
- might depend on the skill as to reset params/operations
- track xp - if no xp gained or no inventory action taken in X minutes
- perform hard reset (ie: we got teleported to lumby or died)
- use ::cg to start

## CLAN GUILD (CG) FUNCTIONS

### CG-RESET

- ::cg
- CAMERA
- COMPASS
- CG-BANK

### CG-BANK

- CLICK BANK TILE 1
- CLICK BANK - DEPOSIT ALL INVENTORY

### FISHING

- CG-RESET
- CG-BANK
- CLICK FISH SPACE 1
- WAIT 1MIN? CLICK?
- CG-BANK
- CLICK FISH SPACE 1

### OTHER SKILLS

- Woodcutting x3
- Mining x4
- Cooking
- Smithing
- Firemaking
- Crafting
- Fletching
- Herblore
- Runecrafting
- Agility
- etc.

### NEW ACCOUNT SETUP

- create a new account with a random name
- randomize the password
- randomize the email
- store in a db

### MULE DUMP

- when cash stack hits X
- dump to mule account via trade
- teleport to castle wars
- trade mule
- trade back
- teleport back using reset function
- trade screen setup and functionality or DROP trade and have bot spam pickup
- need uncommon location for mule to avoid detection (Castle Wars? needs to be same spot everytime)

### AUTO DEPLOYER

- Virtualize the bot
- Dockerize the bot
- Create a deployment script
- install the client
- clone the repo and install dependencies
- run the bot (login/logout needed)
