# Copyright 2016 Streamlio, Inc. All rights reserved.
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

import sys
import pulsar

# A simple function to categorize an incoming message
def extract_category(msg_data):
    return ' '.join(msg_data.split(' ')[1:])

# A simple function to extract neighborhood from an incoming message
def extract_neighborhood(msg_data):
    return msg_data.split(' ')[0]

# A map from toy category to a destination pulsar topic
categories_to_topics = {}

def republish(client, category, neighborhood):
    # If the producer for that toy category has not been created yet, create it.
    if not category in categories_to_topics:
      # Create a producer on the topic. If the topic doesn't exist
      # it will be automatically created
      producer = client.create_producer(
          'persistent://sample/standalone/ns1/categorized-emails-%s' % category)
      categories_to_topics[category] = producer

    # Actually publish the 
    categories_to_topics[category].send(neighborhood)

def main():
    # Create a Pulsar client instance. The instance can be shared across multiple
    # producers and consumers
    client = pulsar.Client('pulsar://localhost:6650',
                           log_conf_file_path='./log4j.cxx')

    # Subscribe to the emails topic. Note that we are subscribing in
    # a shared mode, which means I can easily run multiple distributors
    # to parallely consume all the emails
    consumer = client.subscribe('persistent://sample/standalone/ns1/allemails',
                                'postmaster',
                                consumer_type=pulsar.ConsumerType.Shared)

    while True:
        # try and receive messages with a timeout of 10 seconds
        msg = consumer.receive()

        # Extract the category of the toy desired from the message by parsing it
        category = extract_category(msg.data())

        # Extract the neighboor hood of the kid who sent the email
        neighborhood = extract_neighborhood(msg.data())

        print('Received message for ' + category +\
              ' from neighborhood ' + neighborhood)

        # republish
        republish(client, category, neighborhood)

        # Acknowledge processing of message so that it can be deleted
        consumer.acknowledge(msg)

    # Close the client connection
    client.close()

if __name__ == '__main__':
    main()
