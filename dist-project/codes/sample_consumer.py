from __future__ import division

import math
import itertools
from pykafka import KafkaClient
from pykafka.common import OffsetType

client = KafkaClient(hosts="acorn:9092")
topic = client.topics['GOT']
consumer = topic.get_simple_consumer(
    auto_offset_reset=OffsetType.LATEST,
    reset_offset_on_start=True)
LAST_N_MESSAGES = 5
# # how many messages should we get from the end of each partition?
# MAX_PARTITION_REWIND = int(math.ceil(LAST_N_MESSAGES / len(consumer._partitions)))
# # find the beginning of the range we care about for each partition
# offsets = [(p, op.last_offset_consumed - MAX_PARTITION_REWIND)
#            for p, op in consumer._partitions.iteritems()]
# # if we want to rewind before the beginning of the partition, limit to beginning
# offsets = [(p, (o if o > -1 else -2)) for p, o in offsets]
# # reset the consumer's offsets
# consumer.reset_offsets(offsets)
for message in islice(consumer, LAST_N_MESSAGES):
    print(message.offset, message.value)