# Santasaver

How Pulsar helped Santa scale Christmas!

# Constituent modules

This example consists of three modules:

1. Incoming email generator which is implemented by the `incoming_emails.py` file.
It simulates emails coming from all over the world by generating a random tuple
consisting of a neighborhood zipcode and desired toy
2. A "postmaster" that routes the incoming emails generated above into the appropriate
toy category. This is implemented by the `postmaster.py` script.
3. Lego Elf is the elf that manufactures Lego toys. It reads from the `lego` category
populated by the postmaster and after creating the lego puts it into the
correct neighborhood.

The code for the modules is found in the `src` directory. The resources consist of all
the resource files needed by the Incoming email generator. The conf file is a log4j
log config used by both the postmaster and the Lego Elf.

# How to run the example

1. First, set up a Pulsar cluster on your laptop in standalone mode. Detailed instructions can be found [in the official Pulsar docs](http://pulsar.incubator.apache.org/docs/latest/getting-started/LocalCluster/). Simpler instructions here:

   ```bash
   $ wget http://archive.apache.org/dist/incubator/pulsar/pulsar-1.21.0-incubating/apache-pulsar-1.21.0-incubating-bin.tar.gz
   $ tar xvfz apache-pulsar-1.21.0-incubating-bin.tar.gz
   $ cd apache-pulsar-1.21.0-incubating
   $ bin/pulsar standalone
   ```
2. Clone this repo using Git and then `cd` into it:

   ```bash
   $ git clone https://github.com/streamlio/santasaver
   $ cd santasaver
   ```
4. Run the email generator script:

   ```bash
   $ python ./src/incoming_emails.py \
     ./resources/SantaProductCatalog.csv \
     ./resources/ZipcodeDatabase.csv
   ```
5. Start the postmaster Python script:

   ```bash
   $ ./src/postmaster.py
   ```
6. Start the Lego Elf script:

   ```bash
   $ python ./src/lego_elf.py
   ```
