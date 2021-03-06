# -*- coding: utf-8 -*-
#
# forms_input.py - Input Flask Forms
#
import logging

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import DecimalField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from wtforms import widgets
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import NumberInput

from mycodo.config_translations import TRANSLATIONS
from mycodo.mycodo_flask.utils.utils_general import generate_form_input_list
from mycodo.utils.inputs import parse_input_information

logger = logging.getLogger("mycodo.forms_input")


class DataBase(FlaskForm):
    reorder_type = StringField('Reorder Type', widget=widgets.HiddenInput())
    list_visible_elements = SelectMultipleField('New Order')
    reorder = SubmitField(TRANSLATIONS['save_order']['title'])


class InputAdd(FlaskForm):
    choices_inputs = []
    dict_inputs = parse_input_information()
    list_inputs_sorted = generate_form_input_list(dict_inputs)

    for each_input in list_inputs_sorted:
        if 'interfaces' not in dict_inputs[each_input]:
            choices_inputs.append(
                ('{inp},'.format(inp=each_input),
                 '{manuf}: {name}: {meas}'.format(
                     manuf=dict_inputs[each_input]['input_manufacturer'],
                     name=dict_inputs[each_input]['input_name'],
                     meas=dict_inputs[each_input]['measurements_name'])))
        else:
            for each_interface in dict_inputs[each_input]['interfaces']:
                choices_inputs.append(
                    ('{inp},{int}'.format(inp=each_input, int=each_interface),
                     '{manuf}: {name}: {meas} ({int})'.format(
                         manuf=dict_inputs[each_input]['input_manufacturer'],
                         name=dict_inputs[each_input]['input_name'],
                         meas=dict_inputs[each_input]['measurements_name'],
                         int=each_interface)))

    input_type = SelectField(
        choices=choices_inputs,
        validators=[DataRequired()]
    )
    input_add = SubmitField(TRANSLATIONS['add']['title'])


class InputMod(FlaskForm):
    input_id = StringField('Input ID', widget=widgets.HiddenInput())
    input_measurement_id = StringField(widget=widgets.HiddenInput())
    name = StringField(
        TRANSLATIONS['name']['title'],
        validators=[DataRequired()]
    )
    period = DecimalField(
        TRANSLATIONS['period']['title'],
        validators=[DataRequired(),
                    validators.NumberRange(
                        min=5.0,
                        max=86400.0
        )],
        widget=NumberInput(step='any')
    )
    num_channels = IntegerField(lazy_gettext('Number of Measurements'), widget=NumberInput())
    location = StringField(lazy_gettext('Location'))
    ftdi_location = StringField(TRANSLATIONS['ftdi_location']['title'])
    uart_location = StringField(TRANSLATIONS['uart_location']['title'])
    gpio_location = IntegerField(TRANSLATIONS['gpio_location']['title'])
    i2c_location = StringField(TRANSLATIONS['i2c_location']['title'])
    i2c_bus = IntegerField(TRANSLATIONS['i2c_bus']['title'], widget=NumberInput())
    baud_rate = IntegerField(TRANSLATIONS['baud_rate']['title'], widget=NumberInput())
    power_output_id = StringField(lazy_gettext('Power Output'))  # For powering input
    calibrate_sensor_measure = StringField(lazy_gettext('Calibration Measurement'))
    resolution = IntegerField(TRANSLATIONS['resolution']['title'], widget=NumberInput())
    resolution_2 = IntegerField(TRANSLATIONS['resolution']['title'], widget=NumberInput())
    sensitivity = IntegerField( TRANSLATIONS['sensitivity']['title'], widget=NumberInput())
    measurements_enabled = SelectMultipleField(TRANSLATIONS['measurements_enabled']['title'])

    # Server options
    host = StringField(TRANSLATIONS['host']['title'])
    port = IntegerField(
        TRANSLATIONS['port']['title'], widget=NumberInput())
    times_check = IntegerField(
        TRANSLATIONS['times_check']['title'], widget=NumberInput())
    deadline = IntegerField(
        TRANSLATIONS['deadline']['title'], widget=NumberInput())

    # Linux Command
    cmd_command = StringField(TRANSLATIONS['cmd_command']['title'])

    # MAX chip options
    thermocouple_type = StringField(TRANSLATIONS['thermocouple_type']['title'])
    ref_ohm = IntegerField(
        TRANSLATIONS['ref_ohm']['title'], widget=NumberInput())

    # SPI Communication
    pin_clock = IntegerField(
        TRANSLATIONS['pin_clock']['title'], widget=NumberInput())
    pin_cs = IntegerField(
        TRANSLATIONS['pin_cs']['title'], widget=NumberInput())
    pin_mosi = IntegerField(
        TRANSLATIONS['pin_mosi']['title'], widget=NumberInput())
    pin_miso = IntegerField(
        TRANSLATIONS['pin_miso']['title'], widget=NumberInput())

    # Bluetooth Communication
    bt_adapter = StringField(lazy_gettext('BT Adapter (hci[X])'))

    # ADC
    adc_gain = IntegerField(
        TRANSLATIONS['adc_gain']['title'], widget=NumberInput())
    adc_resolution = IntegerField(
        TRANSLATIONS['adc_resolution']['title'], widget=NumberInput())
    adc_sample_speed = StringField(TRANSLATIONS['adc_sample_speed']['title'])

    switch_edge = StringField(lazy_gettext('Edge'))
    switch_bouncetime = IntegerField(
        lazy_gettext('Bounce Time (ms)'), widget=NumberInput())
    switch_reset_period = IntegerField(
        lazy_gettext('Reset Period'), widget=NumberInput())

    # Pre-Output
    pre_output_id = StringField(TRANSLATIONS['pre_output_id']['title'])
    pre_output_duration = DecimalField(
        TRANSLATIONS['pre_output_duration']['title'],
        validators=[validators.NumberRange(
            min=0,
            max=86400
        )],
        widget=NumberInput(step='any')
    )
    pre_output_during_measure = BooleanField(
        TRANSLATIONS['pre_output_during_measure']['title'])

    # RPM/Signal
    weighting = DecimalField(
        TRANSLATIONS['weighting']['title'],
        widget=NumberInput(step='any'))
    rpm_pulses_per_rev = DecimalField(
        TRANSLATIONS['rpm_pulses_per_rev']['title'],
        widget=NumberInput(step='any'))
    sample_time = DecimalField(
        TRANSLATIONS['sample_time']['title'],
        widget=NumberInput(step='any'))

    # SHT options
    sht_voltage = StringField(TRANSLATIONS['sht_voltage']['title'])

    input_mod = SubmitField(TRANSLATIONS['save']['title'])
    input_delete = SubmitField(TRANSLATIONS['delete']['title'])
    input_acquire_measurements = SubmitField(lazy_gettext('Acquire Measurements Now'))
    input_activate = SubmitField(TRANSLATIONS['activate']['title'])
    input_deactivate = SubmitField(TRANSLATIONS['deactivate']['title'])
    input_order_up = SubmitField(TRANSLATIONS['up']['title'])
    input_order_down = SubmitField(TRANSLATIONS['down']['title'])


class InputMeasurementMod(FlaskForm):
    input_id = StringField('Input ID', widget=widgets.HiddenInput())
    input_measurement_id = StringField(widget=widgets.HiddenInput())
    input_type = StringField(widget=widgets.HiddenInput())
    name = StringField(TRANSLATIONS['name']['title'])
    select_measurement_unit = StringField(TRANSLATIONS['select_measurement_unit']['title'])

    scale_from_min = DecimalField(
        TRANSLATIONS['scale_from_min']['title'],
        widget=NumberInput(step='any'))
    scale_from_max = DecimalField(
        TRANSLATIONS['scale_from_max']['title'],
        widget=NumberInput(step='any'))
    scale_to_min = DecimalField(
        TRANSLATIONS['scale_to_min']['title'],
        widget=NumberInput(step='any'))
    scale_to_max = DecimalField(
        TRANSLATIONS['scale_to_max']['title'],
        widget=NumberInput(step='any'))
    invert_scale = BooleanField(
        TRANSLATIONS['invert_scale']['title'])

    rescaled_measurement_unit = StringField(lazy_gettext('Rescaled Measurement'))
    convert_to_measurement_unit = StringField(TRANSLATIONS['convert_to_measurement_unit']['title'])

    input_measurement_mod = SubmitField(TRANSLATIONS['save']['title'])
