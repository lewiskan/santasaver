# Copyright 2017 Streamlio, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/bin/env python

from itertools import cycle
import pulsar
import sys
import time

# Simple function to load a file containing category
# name line by line into a list
def load_csv(filename):
    items = []
    with open(filename, "r") as ins:
        for line in ins.read().splitlines():
            if line.strip().rstrip('\n'):
                items.append(line)
    return items

def main(argv):
    # Load the categories and the neighborhood
    categories = load_csv(argv[1])
    neighborhoods = load_csv(argv[2])
    category_pool = cycle(categories)
    neighborhood_pool = cycle(neighborhoods)

    # Create a Pulsar client instance.
    client = pulsar.Client('pulsar://localhost:6650')

    # Create a producer on the topic. If the topic doesn't exist
    # it will be automatically created
    producer = client.create_producer(
              'persistent://sample/standalone/ns1/allemails')
    message_count = 0

    # Keep publishing the messages forever
    while True:
        # For simulation purposes, we are just joining a random neighborhood
        # with the toy category type
        generated_email = ' '.join([next(neighborhood_pool), next(category_pool)])
        producer.send(generated_email)

        message_count += 1
        if message_count % 100 == 0:
          # For the sake of demo, sleep 1 second
          print('Produced %d messages' % message_count)
          time.sleep(1)

    # Close the client connection
    client.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Supply categories and neighborhood files"
        sys.exit(1)
    main(sys.argv)
