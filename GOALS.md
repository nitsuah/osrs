# RSPS AUTOBOT

## FUTURE FEATURES

### QUESTION HANDLER v2

- new question handler for random events (currently pause and screenshot)
- spell/grammar check on question detected
- if new push to LLM/answer-bot?

### AUTO CG
  
- increase the number of interactive targeted skills to the Clan Guild location
- fishing x4, woodcutting x3, cooking, smithing, firemaking, mining x4
- there is also a bank so bank and deposit instead of empty
- need to add a check for the bank and the bank booth
- use cg teleport to reset rhythm

### HEALTH CHECK

- constant check of hp
- when low, invoke reset of some kind.
- reset involves teleporting by typing ::edge or some other teleport or clicking to a certain location
- then clicking the fountain
- then clicking back into place on the stall
- might need to reset camera out and in strategically
- could also involve eating food if hp is low by clicking other inventory spaces besides 1st slot

### BANKING

- onyx protection - pausing + sound

### MULE DUMP

- when cash stack hits X, dump to mule account via trade
- teleport to castle wars, trade mule, trade back, teleport back using reset function
- trade screen setup and functionality or DROP trade and have bot spam pickup
- need uncommon location for mule to avoid detection (Castle Wars? needs to be same spot everytime)

### NEW ACCOUNT SETUP

- create a new account with a random name
- randomize the password
- randomize the email

### AUTO DEPLOYER

- Dockerize the bot
- Create a deployment script
- install the client
- clone the repo and install dependencies
- run the bot (login/logout needed)

### HARD RESET

- might involve the above but also logging out and back in
- might involve restarting the script or client if a serious error or process fault is detected
- might depend on the skill as to reset params/operations
- track xp - if no xp gained or no inventory action taken in X minutes, perform hard reset (ie: we got teleported to lumby or died)
