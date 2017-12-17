# Santasaver
How Pulsar helped Santa scale Christmas!

# Constituent modules
This example consists of three modules
1. Incoming email generator which is implemented by the incoming_emails.py file.
It simulates emails coming from all over the world by generating a random tuple
consisting of a neighborhood zipcode and desired toy
2. PostMaster which routes the incoming emails generated above into its appropriate
category of the toy. This is implemented by postmaster.py
3. Lego Elf is the elf that manufactures lego toys. It reads from the lego category
populated by the postmaster and after creating the lego, puts it into the
correct neighborhood.
The code for the modules is found in src directory. The resources consist of all
the resource files needed by the Incoming email generator. The conf file is a log4j
log config used by both the PostMaster and the Lego Elf.

# How to run
1. First setup a Pulsar cluster on your laptop in standalone mode.
2. Do a git clone of this repo.
3. cd into the repo.
4. python ./src/incoming_emails.py ./resources/SantaProductCatalog.csv ./resources/ZipcodeDatabase.csv
5. python ./src/postmaster.py
6. python ./src/lego_elf.py
