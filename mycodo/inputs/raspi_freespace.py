# coding=utf-8
import logging

import os

from mycodo.inputs.base_input import AbstractInput

# Measurements
measurements_dict = {
    0: {
        'measurement': 'disk_space',
        'unit': 'MB'
    }
}

# Input information
INPUT_INFORMATION = {
    'input_name_unique': 'RPiFreeSpace',
    'input_manufacturer': 'Mycodo',
    'input_name': 'Free Space',
    'measurements_name': 'Unallocated Disk Space',
    'measurements_dict': measurements_dict,

    'options_enabled': [
        'location',
        'period'
    ],
    'options_disabled': ['interface'],

    'interfaces': ['Mycodo'],
    'location': {
        'title': 'Path',
        'phrase': 'The path to monitor the free space of',
        'options': [('/', '')]
    }
}


class InputModule(AbstractInput):
    """ A sensor support class that monitors the free space of a path """

    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__()
        self.logger = logging.getLogger("mycodo.inputs.raspi_freespace")
        self._disk_space = None

        if not testing:
            self.logger = logging.getLogger(
                "mycodo.raspi_freespace_{id}".format(id=input_dev.unique_id.split('-')[0]))

            self.path = input_dev.location

    def get_measurement(self):
        """ Gets the free space """
        return_dict = measurements_dict.copy()

        f = os.statvfs(self.path)
        return_dict[0]['value'] = (f.f_bsize * f.f_bavail) / 1000000.0

        return return_dict
