# -*- coding: UTF-8 -*-
import logging

from Coniferous.ttypes import InvalidSystemClock, InvalidTokenError


__author__ = 'yangtianhang'

from Coniferous.Coniferous import Iface
import time


class IdWorker(object, Iface):
    def __init__(self, worker_id, data_center_id):
        self.worker_id = worker_id
        self.data_center_id = data_center_id

        self.token = "a"
        self.logger = logging.getLogger("idworker")

        # stats
        self.ids_generated = 0

        # Tue, 21 Mar 2006 20:50:14.000 GMT
        self.twepoch = 1142974214000L

        self.sequence = 0L
        self.worker_id_bits = 5L
        self.data_center_id_bits = 5L
        self.max_worker_id = -1L ^ (-1L << self.worker_id_bits)
        self.max_data_center_id = -1L ^ (-1L << self.data_center_id_bits)
        self.sequence_bits = 12L

        self.worker_id_shift = self.sequence_bits
        self.data_center_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.data_center_id_bits
        self.sequence_mask = -1L ^ (-1L << self.sequence_bits)

        self.last_timestamp = -1L
        self.max_count = 255

        # Sanity check for worker_id
        if self.worker_id > self.max_worker_id or self.worker_id < 0:
            raise ValueError("worker id can't be greater than %i or less than 0" % self.max_worker_id)

        if self.data_center_id > self.max_data_center_id or self.data_center_id < 0:
            raise ValueError("data center id can't be greater than %i or less than 0" % self.max_data_center_id)

        self.logger.info("worker starting. timestamp left shift %d, data center id bits %d, worker id bits %d, sequence bits %d, worker id %d" %
                         (self.timestamp_left_shift, self.data_center_id_bits, self.worker_id_bits, self.sequence_bits, self.worker_id))

    def _time_gen(self):
        return long(int(time.time() * 1000))

    def _till_next_millis(self, last_timestamp):
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()

        return timestamp

    def _next_id(self):
        timestamp = self._time_gen()

        if self.last_timestamp > timestamp:
            self.logger.warning("clock is moving backwards. Rejecting request until %i" % self.last_timestamp)
            raise InvalidSystemClock("Clock moved backwards. Refusing to generate id for %i milliseocnds" % self.last_timestamp)

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - self.twepoch) << self.timestamp_left_shift) | (self.data_center_id << self.data_center_id_shift) | (self.worker_id << self.worker_id_shift) | self.sequence
        self.ids_generated += 1
        return new_id

    def get_worker_id(self):
        return self.worker_id

    def get_timestamp(self):
        return self._time_gen()

    def get_ids(self, token, count):
        if self.token != token:
            raise InvalidTokenError("Invalid token")
        if count > self.max_count:
            raise InvalidTokenError("Invalid count")

        return [self._next_id() for _x in range(count)]

    def get_data_center_id(self):
        return self.data_center_id
