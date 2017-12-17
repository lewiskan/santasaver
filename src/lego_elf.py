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

# Magically create lego
def create_lego():
    return "Magical Lego"

# A map from toy category to a destination pulsar topic
neighborhoods_to_topics = {}

# Publish the lego toy into the right neighborhood topic
def republish_toys(client, neighborhood, toy):
    # If the producer for that toy category has not been created yet, create it.
    if not neighborhood in neighborhoods_to_topics:
        # Create a producer on the topic. If the topic doesn't exist
        # it will be automatically created
        producer = client.create_producer(
              'persistent://sample/standalone/ns1/built-toys-%s' % neighborhood)
        neighborhoods_to_topics[neighborhood] = producer

    # Actually publish the toy
    neighborhoods_to_topics[neighborhood].send(toy)

def main():
    # Create a Pulsar client instance. The instance can be shared across multiple
    # producers and consumers
    client = pulsar.Client('pulsar://localhost:6650',
                           log_conf_file_path='./log4j.cxx')

    # Subscribe to the emails topic. Note that we are subscribing in
    # a Exclusive mode, which means that all of the lego requests
    # are handled by this super efficient lego elf
    consumer = client.subscribe(
               'persistent://sample/standalone/ns1/categorized-emails-Lego',
               'postmaster', consumer_type=pulsar.ConsumerType.Exclusive)

    while True:
        # try and receive messages with a timeout of 10 seconds
        msg = consumer.receive()
        print("Lego Elf received lego request from neighborhood " + msg.data())
   
        # Create the toy
        lego_toy = create_lego()

        # Route the toy to the right neighborhood
        republish_toys(client, msg.data(), lego_toy)

        # Acknowledge processing of message so that it can be deleted
        consumer.acknowledge(msg)

    # Close the client connection
    client.close()

if __name__ == '__main__':
    main()
