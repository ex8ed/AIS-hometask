# -*- coding: UTF-8 -*-
"""Contains widgets for main GUI file"""

from random import randint
from PySide6.QtWidgets import (QLabel,
                               QComboBox,
                               QLineEdit,
                               QWidget,
                               QGridLayout)

from config.style_settings import (DEC_9_WIDGET_COMBO_BOX_WIDTH,
                                   DEC_9_WIDGET_LINE_EDIT_WIDTH)

from app.app_core import Simulator
from app.messages import *


def isfloat(float_num_str):
    try:
        float(float_num_str)
    except ValueError:
        return False
    else:
        return True


def show_msg_success_box(title='MessageBox', text='Info'):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.show()
    r = msg_box.exec()


class GnSystem(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.layout = QGridLayout(self)

        self.layout.addWidget(QLabel(f'<h3> Specify parameters for {self.name}:</h3>', self),
                         0, 0, 1, 2)


class Uocns(GnSystem):
    def __init__(self):
        super().__init__("uocns")
        row = 1
        self.layout.addWidget(QLabel('Topology', self), row, 0)
        self.topology = QComboBox(self)
        self.topology.addItems(['Mesh', 'Circulant', 'Torus', 'CirculantOpt'])
        self.topology.setCurrentIndex(0)
        self.layout.addWidget(self.topology)

        row += 1
        self.layout.addWidget(QLabel('FIFO size, flits', self), row, 0)
        self.fifo_size = QLineEdit(self)
        self.layout.addWidget(self.fifo_size, row, 1)

        row += 1
        self.layout.addWidget(QLabel('FIFO count', self), row, 0)
        self.fifo_count = QLineEdit(self)
        self.layout.addWidget(self.fifo_count)

        row += 1
        self.layout.addWidget(QLabel('Flit size, bits', self), row, 0)
        self.flit_size = QLineEdit(self)
        self.layout.addWidget(self.flit_size)

        row += 1
        self.layout.addWidget(QLabel('Topology args', self), row, 0)
        self.topology_args = QLineEdit(self)
        self.layout.addWidget(self.topology_args)

        row += 1
        self.layout.addWidget(QLabel('Algorithm args', self), row, 0)
        self.algorithm_args = QLineEdit(self)
        self.layout.addWidget(self.algorithm_args)

        row += 1
        self.layout.addWidget(QLabel('Algorithm', self), row, 0)
        self.algorithm = QComboBox(self)
        self.algorithm.addItems(['Dijkstra', 'PO', 'POU'])
        self.algorithm.setCurrentIndex(0)
        self.layout.addWidget(self.algorithm)

        row = 1
        self.layout.addWidget(QLabel('Count run', self), row, 2)
        self.count_run = QLineEdit(self)
        self.layout.addWidget(self.count_run, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Count packet rx', self), row, 2)
        self.count_packet_rx = QLineEdit(self)
        self.layout.addWidget(self.count_packet_rx, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Packet size avg, flits', self), row, 2)
        self.packet_size_avg = QLineEdit(self)
        self.layout.addWidget(self.packet_size_avg, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Packet size is fixed', self), row, 2)
        self.packet_size_is_fixed = QComboBox(self)
        self.packet_size_is_fixed.addItems(['True', 'False'])
        self.packet_size_is_fixed.setCurrentIndex(0)
        self.layout.addWidget(self.packet_size_is_fixed, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Is mode GALS', self), row, 2)
        self.is_mode_gals = QComboBox(self)
        self.is_mode_gals.addItems(['True', 'False'])
        self.is_mode_gals.setCurrentIndex(0)
        self.layout.addWidget(self.is_mode_gals, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Count packet rx warm up', self), row, 2)
        self.count_packet_rx_warm_up = QLineEdit(self)
        self.layout.addWidget(self.count_packet_rx_warm_up, row, 3)

    def check_fields(self) -> bool:
        fifo_size = self.fifo_size.text()
        fifo_count = self.fifo_count.text()
        flit_size = self.flit_size.text()
        topology_args = self.topology_args.text().split()
        count_run = self.count_run.text()
        count_packet_rx = self.count_packet_rx.text()
        packet_size_avg = self.packet_size_avg.text()
        count_packet_rx_warm_up = self.count_packet_rx_warm_up.text()

        if not fifo_size.isdigit():
            GnCritical("FIFO_DIGIT")
            return False
        elif int(fifo_size) < 1 or int(fifo_size) > 128:
            GnCritical("FIFO_SIZE")
            return False

        if not fifo_count.isdigit():
            GnCritical("FIFO_COUNT_DIGIT")
            return False
        elif int(fifo_count) < 1 or int(fifo_count) > 10:
            GnCritical("FIFO_COUNT_SIZE")
            return False

        if not flit_size.isdigit():
            GnCritical("FLIT_SIZE_DIGIT")
            return False
        elif int(flit_size) < 1 or int(flit_size) > 128:
            GnCritical("FLIT_SIZE_SIZE")
            return False

        for arg in topology_args:
            if not arg.isdigit():
                GnCritical("TOPOLOGY")
                return False

        if not count_run.isdigit():
            GnCritical("COUNT_RUN_DIGIT")
            return False
        elif int(count_run) != 1:
            GnCritical("COUNT_RUN")
            return False

        if not count_packet_rx.isdigit():
            GnCritical("COUNT_PRX_DIGIT")
            return False
        elif int(count_packet_rx) < 100 or int(count_packet_rx) > 10000:
            GnCritical("COUNT_PRX_SIZE")
            return False

        if not packet_size_avg.isdigit():
            GnCritical("PACKET_SIZE_DIGIT")
            return False
        elif int(packet_size_avg) < 1 or int(packet_size_avg) > 100:
            GnCritical("PACKET_SIZE")
            return False

        if not count_packet_rx_warm_up.isdigit():
            GnCritical("COUNT_PACKET_RX_DIGIT")
            return False
        elif int(count_packet_rx_warm_up) < 0 or int(count_packet_rx_warm_up) > 1000:
            GnCritical("COUNT_PACKET_RX_SIZE")
            return False
        return True

    def read_fields(self):
        s = Simulator(self.name, 0)

        topology = self.topology.currentIndex()
        fifo_size = self.fifo_size.text()
        fifo_count = self.fifo_count.text()
        flit_size = self.flit_size.text()
        topology_args = self.topology_args.text().split()
        algorithm_args = self.algorithm_args.text().split()
        algorithm = self.algorithm.currentIndex()
        count_run = self.count_run.text()
        count_packet_rx = self.count_packet_rx.text()
        packet_size_avg = self.packet_size_avg.text()
        packet_size_is_fixed = self.packet_size_is_fixed.currentIndex()
        is_mode_gals = self.is_mode_gals.currentIndex()
        count_packet_rx_warm_up = self.count_packet_rx_warm_up.text()

        self.check_fields()

        s.set_parameter('Topology', topology)
        s.set_parameter('TopologyArguments', list(map(int, topology_args)))
        s.set_parameter('Algorithm', algorithm)
        s.set_parameter('AlgorithmArguments', algorithm_args)
        s.set_parameter('FifoSize', int(fifo_size))
        s.set_parameter('FifoCount', int(fifo_count))
        s.set_parameter('FlitSize', int(flit_size))
        s.set_parameter('PacketSizeAvg', int(packet_size_avg))
        s.set_parameter('PacketSizeIsFixed', packet_size_is_fixed == 0)
        s.set_parameter('PacketPeriodAvg', list(range(5, 100, 10)))  # default value that could be changed in UHLNoCS
        s.set_parameter('CountRun', int(count_run))
        s.set_parameter('CountPacketRx', int(count_packet_rx))
        s.set_parameter('CountPacketRxWarmUp', int(count_packet_rx_warm_up))
        s.set_parameter('IsModeGALS', is_mode_gals == 0)

        return s


class Booksim(GnSystem):
    def __init__(self):
        super().__init__("booksim")

        row = 1
        self.layout.addWidget(QLabel('Topology', self), row, 0)
        self.topology = QComboBox(self)
        self.topology.addItems(['Mesh', 'Torus'])
        self.topology.setCurrentIndex(0)
        self.layout.addWidget(self.topology, row, 1)

        row += 1
        self.layout.addWidget(QLabel('Virtual channels number', self), row, 0)
        self.virtual_channels_number = QLineEdit(self)
        self.layout.addWidget(self.virtual_channels_number)

        row += 1
        self.layout.addWidget(QLabel('Traffic distribution', self), row, 0)
        self.traffic_distribution = QComboBox(self)
        self.traffic_distribution.addItems(['Uniform',
                                            'BitComp',
                                            'BitRev',
                                            'Shuffle',
                                            'Transpose',
                                            'Tomado',
                                            'Neighbor'])
        self.traffic_distribution.setCurrentIndex(0)
        self.layout.addWidget(self.traffic_distribution)

        row += 1
        self.layout.addWidget(QLabel('Sample period, cycles', self), row, 0)
        self.sample_period = QLineEdit(self)
        self.layout.addWidget(self.sample_period)

        row += 1
        self.layout.addWidget(QLabel('Topology args', self), row, 0)
        self.topology_args = QLineEdit(self)
        self.layout.addWidget(self.topology_args)

        row += 1
        self.layout.addWidget(QLabel('Virtual channel buf size, flits', self), row, 0)
        self.virtual_channel_buffer = QLineEdit(self)
        self.layout.addWidget(self.virtual_channel_buffer)

        row = 1
        self.layout.addWidget(QLabel('Packet size, bits', self), row, 2)
        self.packet_size = QLineEdit(self)
        self.layout.addWidget(self.packet_size, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Warm up periods, cycles', self), row, 2)
        self.warm_up_periods = QLineEdit(self)
        self.layout.addWidget(self.warm_up_periods, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Routing function', self), row, 2)
        self.routing_function = QComboBox(self)
        self.routing_function.addItems(['DimOrder',
                                        'DOR',
                                        'DOR No Express',
                                        'Min',
                                        'RanMin'])
        self.routing_function.setCurrentIndex(0)
        self.layout.addWidget(self.routing_function, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Simulation type', self), row, 2)
        self.simulation_type = QComboBox(self)
        self.simulation_type.addItems(['Latency',
                                       'Throughput'])
        self.simulation_type.setCurrentIndex(0)
        self.layout.addWidget(self.simulation_type, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Max samples, cycles', self), row, 2)
        self.max_samples = QLineEdit(self)
        self.layout.addWidget(self.max_samples, row, 3)

    def check_fields(self) -> bool:
        topology = self.topology.currentIndex()
        virtual_channels_number = self.virtual_channels_number.text()
        traffic_distribution = self.traffic_distribution.currentIndex()
        sample_period = self.sample_period.text()
        topology_args = self.topology_args.text().split()
        virtual_channels_buffer = self.virtual_channel_buffer.text()
        packet_size = self.packet_size.text()
        warm_up_periods = self.warm_up_periods.text()
        routing_function = self.routing_function.currentIndex()
        simulation_type = self.simulation_type.currentIndex()
        max_samples = self.max_samples.text()

        if not virtual_channels_number.isdigit():
            GnCritical("VCN_DIGIT")
            return False
        elif int(virtual_channels_number) < 1 or int(virtual_channels_number) > 10:
            GnCritical("VCN_SIZE")
            return False

        if not sample_period.isdigit():
            GnCritical("SPC_DIGIT")
            return False
        elif int(sample_period) < 5000 or int(sample_period) > 100000:
            GnCritical("SPC_SIZE")
            return False

        for arg in topology_args:
            if not arg.isdigit():
                GnCritical("TOPOLOGY")
                return False

        if not virtual_channels_buffer.isdigit():
            GnCritical("VCNBF_DIGIT")
            return False
        elif int(virtual_channels_buffer) < 1 or int(virtual_channels_buffer) > 128:
            GnCritical("VCNBF_SIZE")
            return False

        if not packet_size.isdigit():
            GnCritical("PACKETF_DIGIT")
            return False
        elif int(packet_size) < 1 or int(packet_size) > 100:
            GnCritical("PACKETF_SIZE")
            return False

        if not warm_up_periods.isdigit():
            GnCritical("WARMUP_DIGIT")
            return False
        elif int(warm_up_periods) < 0 or int(warm_up_periods) > 10:
            GnCritical("WARMUP_SIZE")
            return False

        if not max_samples.isdigit():
            GnCritical("MAX_SAMPLES_DIGIT")
            return False
        elif int(max_samples) < 1 or int(max_samples) > 10:
            GnCritical("MAX_SAMPLES_SIZE")
            return False
        return True

    def read_fields(self):
        s = Simulator(self.name, 1)

        topology = self.topology.currentIndex()
        virtual_channels_number = self.virtual_channels_number.text()
        traffic_distribution = self.traffic_distribution.currentIndex()
        sample_period = self.sample_period.text()
        topology_args = self.topology_args.text().split()
        virtual_channels_buffer = self.virtual_channel_buffer.text()
        packet_size = self.packet_size.text()
        warm_up_periods = self.warm_up_periods.text()
        routing_function = self.routing_function.currentIndex()
        simulation_type = self.simulation_type.currentIndex()
        max_samples = self.max_samples.text()
        
        self.check_fields()

        s.set_parameter('Topology', topology)
        s.set_parameter('TopologyArgs', list(map(int, topology_args)))
        s.set_parameter('RoutingFunction', routing_function)
        s.set_parameter('VirtualChannelsNum', int(virtual_channels_number))
        s.set_parameter('VirtualChannelBufSize', int(virtual_channels_buffer))
        s.set_parameter('TrafficDistribution', traffic_distribution)
        s.set_parameter('PacketSize', int(packet_size))
        s.set_parameter('SimType', simulation_type)
        # default value that could be changed in UHLNoCS
        s.set_parameter('InjectionRate', [i / 100 for i in range(5, 100, 10)])
        s.set_parameter('SamplePeriod', int(sample_period))
        s.set_parameter('WarmUpPeriods', int(warm_up_periods))
        s.set_parameter('MaxSamples', int(max_samples))

        return s


class Newxim(GnSystem):
    def __init__(self):
        super().__init__('newxim')

        row = 1
        self.layout.addWidget(QLabel('Topology', self), row, 0)
        self.topology = QComboBox(self)
        self.topology.addItems(['Mesh',
                                'Torus',
                                'Tree',
                                'Circulant'])
        self.topology.setCurrentIndex(0)
        self.layout.addWidget(self.topology)

        row += 1
        self.layout.addWidget(QLabel('Topology channels', self), row, 0)
        self.topology_channels = QLineEdit(self)
        self.layout.addWidget(self.topology_channels)

        row += 1
        self.layout.addWidget(QLabel('Selection strategy', self), row, 0)
        self.selection_strategy = QComboBox(self)
        self.selection_strategy.addItems(['Random',
                                          'Buffer level',
                                          'Keep space',
                                          'Random keep space'])
        self.selection_strategy.setCurrentIndex(0)
        self.layout.addWidget(self.selection_strategy)

        row += 1
        self.layout.addWidget(QLabel('Simulation time, cycles', self), row, 0)
        self.simulation_time = QLineEdit(self)
        self.layout.addWidget(self.simulation_time)

        row += 1
        self.layout.addWidget(QLabel('Topology args', self), row, 0)
        self.topology_args = QLineEdit(self)
        self.layout.addWidget(self.topology_args)

        row += 1
        self.layout.addWidget(QLabel('Virtual channels', self), row, 0)
        self.virtual_channels = QLineEdit(self)
        self.layout.addWidget(self.virtual_channels)

        row = 1
        self.layout.addWidget(QLabel('Min packet size, bits', self), row, 2)
        self.min_packet_size = QLineEdit(self)
        self.layout.addWidget(self.min_packet_size, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Warm up time, cycles', self), row, 2)
        self.warm_up_time = QLineEdit(self)
        self.layout.addWidget(self.warm_up_time, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Routing algorithm', self), row, 2)
        self.routing_algorithm = QComboBox(self)
        self.routing_algorithm.addItems(['Dijkstra',
                                         'Up Down',
                                         'Mesh XY',
                                         'Circulant Pair Exchange',
                                         'Greedy Promotion',
                                         'Circulant Multiplicative',
                                         'Circulant Clockwise',
                                         'Circulant Adaptive'])
        self.routing_algorithm.setCurrentIndex(0)
        self.layout.addWidget(self.routing_algorithm, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Buffer depth', self), row, 2)
        self.buffer_depth = QLineEdit(self)
        self.layout.addWidget(self.buffer_depth, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Max packet size, flits', self), row, 2)
        self.max_packet_size = QLineEdit(self)
        self.layout.addWidget(self.max_packet_size, row, 3)

    def check_fields(self) -> bool:
        topology = self.topology.currentIndex()
        topology_channels = self.topology_channels.text()
        selection_strategy = self.selection_strategy.currentIndex()
        simulation_time = self.simulation_time.text()
        topology_args = self.topology_args.text().split()
        virtual_channels = self.virtual_channels.text()
        min_packet_size = self.min_packet_size.text()
        warm_up_time = self.warm_up_time.text()
        routing_algorithm = self.routing_algorithm.currentIndex()
        buffer_depth = self.buffer_depth.text()
        max_packet_size = self.max_packet_size.text()

        if not topology_channels.isdigit():
            GnCritical("TOPOLOGY_CHANELS")
            return False
        elif int(topology_channels) != 1:
            GnCritical("TOPOLOGY_CHANELS_1")
            return False

        if not simulation_time.isdigit():
            GnCritical("SIMULATION_TYPE_DIGIT")
            return False
        elif int(simulation_time) < 5000 or int(simulation_time) > 100000:
            GnCritical("SIMULATION_TYPE_SIZE")
            return False

        for arg in topology_args:
            if not arg.isdigit():
                GnCritical("TOPOLOGY")
                return False

        if not virtual_channels.isdigit():
            GnCritical("VCN_DIGIT")
            return False
        elif int(virtual_channels) < 1 or int(virtual_channels) > 10:
            GnCritical("VCN_SIZE")
            return False

        if not min_packet_size.isdigit():
            GnCritical("MIN_PACKET_DIGIT")
            return False
        elif int(min_packet_size) < 1 or int(min_packet_size) > 100:
            GnCritical("MIN_PACKET_SIZE")
            return False

        if not warm_up_time.isdigit():
            GnCritical("WARMUP_CYCLES_DIGIT")
            return False
        elif int(warm_up_time) < 0 or int(warm_up_time) > 10:
            GnCritical("WARMUP_CYCLES_SIZE")
            return False

        if not buffer_depth.isdigit():
            GnCritical("BUFFER_DEPTH_DIGIT")
            return False
        elif int(buffer_depth) < 1 or int(buffer_depth) > 128:
            GnCritical("BUFFER_DEPTH_SIZE")
            return False

        if not max_packet_size.isdigit():
            GnCritical("MAX_PACKET_DIGIT")
            return False
        elif int(max_packet_size) < 1 or int(max_packet_size) > 100:
            GnCritical("MAX_PACKET_SIZE")
            return False
        return True

    def read_fields(self):
        s = Simulator(self.name, 2)

        topology = self.topology.currentIndex()
        topology_channels = self.topology_channels.text()
        selection_strategy = self.selection_strategy.currentIndex()
        simulation_time = self.simulation_time.text()
        topology_args = self.topology_args.text().split()
        virtual_channels = self.virtual_channels.text()
        min_packet_size = self.min_packet_size.text()
        warm_up_time = self.warm_up_time.text()
        routing_algorithm = self.routing_algorithm.currentIndex()
        buffer_depth = self.buffer_depth.text()
        max_packet_size = self.max_packet_size.text()

        self.check_fields()

        s.set_parameter('Topology', topology)
        s.set_parameter('TopologyArgs', list(map(int, topology_args)))
        s.set_parameter('RoutingAlgorithm', routing_algorithm)
        s.set_parameter('SelectionStrategy', int(selection_strategy))
        s.set_parameter('TopologyChannels', int(topology_channels))
        s.set_parameter('VirtualChannels', int(virtual_channels))
        s.set_parameter('BufferDepth', int(buffer_depth))
        s.set_parameter('MinPacketSize', int(min_packet_size))
        s.set_parameter('MaxPacketSize', int(max_packet_size))
        # default value that could be changed in UHLNoCS
        s.set_parameter('PacketInjectionRate', [i / 100 for i in range(5, 100, 10)])
        s.set_parameter('SimulationTime', int(simulation_time))
        s.set_parameter('WarmUpTime', int(warm_up_time))

        return s


class Topaz(GnSystem):
    def __init__(self):
        super().__init__('topaz')

        row = 1
        self.layout.addWidget(QLabel('Router', self), row, 0)
        self.router = QComboBox(self)
        self.router.addItems(['Ligero',
                              'Ligero MCAST',
                              'Mesh CT NOC',
                              'Mesh WH NOC',
                              'Mesh DAMQ NOC',
                              'Mesh CT FAST NOC',
                              'Torus CT NOC',
                              'Torus Bless'])
        self.router.setCurrentIndex(0)
        self.layout.addWidget(self.router)

        row += 1
        self.layout.addWidget(QLabel('Traffic pattern', self), row, 0)
        self.traffic_pattern = QComboBox(self)
        self.traffic_pattern.addItems(['Modal', 'Reactive'])
        self.traffic_pattern.setCurrentIndex(0)
        self.layout.addWidget(self.traffic_pattern)

        row += 1
        self.layout.addWidget(QLabel('Message length, packets', self), row, 0)
        self.message_length = QLineEdit(self)
        self.layout.addWidget(self.message_length)

        row += 1
        self.layout.addWidget(QLabel('Flit size, bits', self), row, 0)
        self.flit_size = QLineEdit(self)
        self.layout.addWidget(self.flit_size)

        row += 1
        self.layout.addWidget(QLabel('Network Arguments'), row, 0)
        self.network_arguments = QLineEdit(self)
        self.layout.addWidget(self.network_arguments)

        row += 1
        self.layout.addWidget(QLabel('Traffic pattern type', self), row, 0)
        self.traffic_pattern_type = QComboBox(self)
        self.traffic_pattern_type.addItems(['Random',
                                            'Bit reversal',
                                            'Perfect shuffle',
                                            'Permutation',
                                            'Tornado',
                                            'Local'])
        self.traffic_pattern_type.setCurrentIndex(0)
        self.layout.addWidget(self.traffic_pattern_type)

        row = 1
        self.layout.addWidget((QLabel('Packet length, flits', self)), row, 2)
        self.packet_length = QLineEdit(self)
        self.layout.addWidget(self.packet_length, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Simulation cycles', self), row, 2)
        self.simulation_cycles = QLineEdit(self)
        self.layout.addWidget(self.simulation_cycles, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Model name', self), row, 2)
        self.model_name = QLineEdit(self)
        self.layout.addWidget(self.model_name, row, 3)

    def check_fields(self) -> bool:
        router = self.router.currentIndex()
        traffic_pattern = self.traffic_pattern.currentIndex()
        message_length = self.message_length.text()
        flit_size = self.flit_size.text()
        network_arguments = self.network_arguments.text().split()
        traffic_pattern_type = self.traffic_pattern_type.currentIndex()
        packet_length = self.packet_length.text()
        simulation_cycles = self.simulation_cycles.text()
        model_name = self.model_name.text()  # must be a str

        if not message_length.isdigit():
            GnCritical("MESSAGE_LENGTH_DIGIT")
            return False
        elif int(message_length) != 1:
            GnCritical("MESSAGE_LENGTH_SIZE")
            return False

        if not flit_size.isdigit():
            GnCritical("FLIT_SIZE_BITS_DIGIT")
            return False
        elif int(flit_size) < 1 or int(flit_size) > 256:
            GnCritical("FLIT_SIZE_BITS_SIZE")
            return False

        for arg in network_arguments:
            if not arg.isdigit():
                GnCritical("NETWORK_ARG_DIGIT")
                return False

        if not packet_length.isdigit():
            GnCritical("PACKET_FLITS_DIGIT")
            return False
        elif int(packet_length) < 1 or int(packet_length) > 100:
            GnCritical("PACKET_FLITS_SIZE")
            return False

        if not simulation_cycles.isdigit():
            GnCritical("SIMULATION_CYCLES_DIGIT")
            return False
        elif int(simulation_cycles) < 5000 or int(simulation_cycles) > 100000:
            GnCritical("SIMULATION_CYCLES_SIZE")
            return False
        return True

    def read_fields(self):
        s = Simulator(self.name, 3)

        router = self.router.currentIndex()
        traffic_pattern = self.traffic_pattern.currentIndex()
        message_length = self.message_length.text()
        flit_size = self.flit_size.text()
        network_arguments = self.network_arguments.text().split()
        traffic_pattern_type = self.traffic_pattern_type.currentIndex()
        packet_length = self.packet_length.text()
        simulation_cycles = self.simulation_cycles.text()
        model_name = self.model_name.text()  # must be a str

        self.check_fields()

        s.set_parameter('Simulation', model_name)  # must be a str
        s.set_parameter('TopologyArgs', list(map(int, network_arguments)))
        s.set_parameter('SimulationCycles', int(simulation_cycles))
        s.set_parameter('Router', router)
        s.set_parameter('TrafficPatternId', traffic_pattern)
        s.set_parameter('TopazTrafficPatternTypes', traffic_pattern_type)
        s.set_parameter('Seed', randint(1000, 9999))
        s.set_parameter('Load', [i / 10 for i in range(1, 11)])
        s.set_parameter('MessageLength', int(message_length))
        s.set_parameter('PacketLength', int(packet_length))
        s.set_parameter('FlitSize', int(flit_size))

        return s


class Dec9(GnSystem):
    def __init__(self):
        super().__init__('dec9')

        row = 1
        self.layout.addWidget(QLabel('Topology', self), row, 0)
        self.topology = QComboBox(self)
        self.topology.addItems(['Mesh', 'Circulant'])
        self.topology.setCurrentIndex(0)
        self.topology.setFixedWidth(DEC_9_WIDGET_COMBO_BOX_WIDTH)
        self.layout.addWidget(self.topology)

        row += 1
        self.layout.addWidget(QLabel('Cycle count', self), row, 0)
        self.cycle_count = QLineEdit(self)
        self.cycle_count.setFixedWidth(DEC_9_WIDGET_LINE_EDIT_WIDTH)
        self.layout.addWidget(self.cycle_count)

        row += 1
        self.layout.addWidget(QLabel('Topology args', self), row, 0)
        self.topology_args = QLineEdit(self)
        self.topology_args.setFixedWidth(DEC_9_WIDGET_LINE_EDIT_WIDTH)
        self.layout.addWidget(self.topology_args)

        row += 1
        self.layout.addWidget(QLabel('Message length', self), row, 0)
        self.message_length = QLineEdit(self)
        self.message_length.setFixedWidth(DEC_9_WIDGET_LINE_EDIT_WIDTH)
        self.layout.addWidget(self.message_length)

    def check_fields(self) -> bool:
        topology = self.topology.currentIndex()
        topology_args = self.topology_args.text().split()
        cycle_count = self.cycle_count.text()
        message_length = self.message_length.text()

        for arg in topology_args:
            if not arg.isdigit():
                GnCritical("TOPOLOGY")
                return False

        if not cycle_count.isdigit():
            GnCritical("CYCLE_COUNT_DIGIT")
            return False
        elif int(cycle_count) < 500 or int(cycle_count) > 100000:
            GnCritical("CYCLE_COUNT_SIZE")
            return False

        if not message_length.isdigit():
            GnCritical("MESSAGE_LENGTH_B_DIGIT")
            return False
        elif int(message_length) < 1 or int(message_length) > 100:
            GnCritical("MESSAGE_LENGTH_B_SIZE")
            return False
        return True

    def read_fields(self):
        s = Simulator(self.name, 4)

        topology = self.topology.currentIndex()
        topology_args = self.topology_args.text().split()
        cycle_count = self.cycle_count.text()
        message_length = self.message_length.text()

        self.check_fields()

        s.set_parameter('Topology', topology)
        s.set_parameter('TopologyArgs', list(map(int, topology_args)))
        s.set_parameter('CycleCount', int(cycle_count))
        s.set_parameter('MessageLength', int(message_length))
        s.set_parameter('InjectionRate', [i / 100 for i in range(5, 100, 10)])

        return s


class GpNocSim(GnSystem):
    def __init__(self):
        super().__init__('gpNocSim')

        row = 1
        self.layout.addWidget(QLabel('Topology', self), row, 0)
        self.topology = QComboBox(self)
        self.topology.addItems(['Mesh',
                                'Torus',
                                'Tree',
                                'Circulant'])
        self.topology.setCurrentIndex(0)
        self.layout.addWidget(self.topology)

        row += 1
        self.layout.addWidget(QLabel('Average message length', self), row, 0)
        self.avg_message_length = QLineEdit(self)
        self.layout.addWidget(self.avg_message_length)

        row += 1
        self.layout.addWidget(QLabel('Flit length', self), row, 0)
        self.flit_length = QLineEdit(self)
        self.layout.addWidget(self.flit_length)

        row += 1
        self.layout.addWidget(QLabel('Number of nodes', self), row, 0)
        self.number_of_nodes = QLineEdit(self)
        self.layout.addWidget(self.number_of_nodes)

        row += 1
        self.layout.addWidget(QLabel('Virtual channels number', self), row, 0)
        self.virtual_channels_num = QLineEdit(self)
        self.layout.addWidget(self.virtual_channels_num)

        row += 1
        self.layout.addWidget(QLabel('Number of flits per buf', self), row, 0)
        self.number_of_flits = QLineEdit(self)
        self.layout.addWidget(self.number_of_flits)

        row = 1
        self.layout.addWidget(QLabel('Number of cycles', self), row, 2)
        self.number_of_cycles = QLineEdit(self)
        self.layout.addWidget(self.number_of_cycles, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Number of runs', self), row, 2)
        self.number_of_runs = QLineEdit(self)
        self.layout.addWidget(self.number_of_runs, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Warm up cycles', self), row, 2)
        self.warm_up_cycles = QLineEdit(self)
        self.layout.addWidget(self.warm_up_cycles, row, 3)

        row += 1
        self.layout.addWidget(QLabel('Traffic type', self), row, 2)
        self.traffic_type = QComboBox(self)
        self.traffic_type.addItems(['Uniform', 'Local'])
        self.traffic_type.setCurrentIndex(0)
        self.layout.addWidget(self.traffic_type, row, 3)

    def check_fields(self) -> bool:
        topology = self.topology.currentIndex()
        avg_message_len = self.avg_message_length.text()
        flit_length = self.flit_length.text()
        number_of_nodes = self.number_of_nodes.text()
        virtual_channels_count = self.virtual_channels_num.text()
        number_of_flits = self.number_of_flits.text()
        number_of_cycles = self.number_of_cycles.text()
        number_of_runs = self.number_of_runs.text()
        warm_up_cycle = self.warm_up_cycles.text()
        traffic_type = self.traffic_type.currentIndex()

        if not avg_message_len.isdigit():
            GnCritical("AVG_MESSAGE_DIGIT")
            return False
        elif int(avg_message_len) < -2147483648 or int(avg_message_len) > 2147483647:
            GnCritical("AVG_MESSAGE_SIZE")
            return False

        if not flit_length.isdigit():
            GnCritical("FLIT_LENGTH_DIGIT")
            return False
        elif int(flit_length) < -2147483648 or int(flit_length) > 2147483647:
            GnCritical("FLIT_LENGTH_SIZE")
            return False

        if not number_of_nodes.isdigit():
            GnCritical("NUMBER_NODES_DIGIT")
            return False
        elif int(number_of_nodes) < -2147483648 or int(number_of_nodes) > 2147483647:
            GnCritical("NUMBER_NODES_SIZE")
            return False

        if not virtual_channels_count.isdigit():
            GnCritical("VCNC_DIGIT")
            return False
        elif int(virtual_channels_count) < -2147483648 or int(virtual_channels_count) > 2147483647:
            GnCritical("VCNC_SIZE")
            return False

        if not number_of_flits.isdigit():
            GnCritical("NUMBER_FLITS_DIGIT")
            return False
        elif int(number_of_flits) < -2147483648 or int(number_of_flits) > 2147483647:
            GnCritical("NUMBER_FLITS_SIZE")
            return False

        if not number_of_cycles.isdigit():
            GnCritical("NUMBER_CYCLES_DIGIT")
            return False
        elif int(number_of_cycles) < -2147483648 or int(number_of_cycles) > 2147483647:
            GnCritical("NUMBER_CYCLES_SIZE")
            return False

        if not number_of_runs.isdigit():
            GnCritical("NUMBER_RUNS_DIGIT")
            return False
        elif int(number_of_runs) < -2147483648 or int(number_of_runs) > 2147483647:
            GnCritical("NUMBER_RUNS_SIZE")
            return False

        if not isfloat(warm_up_cycle):
            GnCritical("WARMUP_CYCLES_DIGIT")
            return False
        return True

    def read_fields(self):
        s = Simulator(self.name, 5)

        topology = self.topology.currentIndex()
        avg_message_len = self.avg_message_length.text()
        flit_length = self.flit_length.text()
        number_of_nodes = self.number_of_nodes.text()
        virtual_channels_count = self.virtual_channels_num.text()
        number_of_flits = self.number_of_flits.text()
        number_of_cycles = self.number_of_cycles.text()
        number_of_runs = self.number_of_runs.text()
        warm_up_cycle = self.warm_up_cycles.text()
        traffic_type = self.traffic_type.currentIndex()

        self.check_fields()

        s.set_parameter('CurrentNet', topology)
        s.set_parameter('AvgInterArrival', [i * 10 for i in range(5, 15)])
        s.set_parameter('AvgMessageLength', int(avg_message_len))
        s.set_parameter('FlitLength', int(flit_length))
        s.set_parameter('NumOfIpNode', int(number_of_nodes))
        s.set_parameter('CurrentVcCount', int(virtual_channels_count))
        s.set_parameter('NumFlitPerBuffer', int(number_of_flits))
        s.set_parameter('NumCycle', int(number_of_cycles))
        s.set_parameter('NumRun', int(number_of_runs))
        s.set_parameter('TrafficType', traffic_type)
        s.set_parameter('WarmUpCycle', float(warm_up_cycle))

        return s
