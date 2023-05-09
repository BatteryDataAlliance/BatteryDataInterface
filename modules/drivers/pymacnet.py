
from modules.cyclerConfig import CyclerConfig
from typing import List, Union, Optional, Dict, Any
import json
import pymacnet
import sys
class PyMacNetConfig:
    """
    The Config class represents the configuration object (Object 2) with default values.
    """
    channel: int
    test_name: str
    c_rate_ah: float
    v_max_v: float
    v_min_v: float
    v_max_safety_limit_v: float
    v_min_safety_limit_v: float
    i_max_safety_limit_a: float
    i_min_safety_limit_a: float
    data_record_time_s: float
    data_record_voltage_delta_vbys: float
    data_record_current_delta_abys: float
    test_procedure: str
    server_ip: str
    json_server_port: int
    tcp_server_port: int
    msg_buffer_size_bytes: int

    # TODO: create a default YAML file instead of setting defaults in code
    def __init__(
        self,
        channel: int = 75,
        test_name: str = "",
        c_rate_ah: float = 1,
        v_max_v: float = 5.0,
        v_min_v: float = 3.0,
        v_max_safety_limit_v: float = 4.25,
        v_min_safety_limit_v: float = 2.9,
        i_max_safety_limit_a: float = 3.0,
        i_min_safety_limit_a: float = 3.0,
        data_record_time_s: float = 0.05,
        data_record_voltage_delta_vbys: float = 0.0,
        data_record_current_delta_abys: float = 0.0,
        test_procedure: str = "test_procedure_1",
        server_ip: str = "3.3.31.83",
        json_server_port: int = 57570,
        tcp_server_port: int = 57560,
        msg_buffer_size_bytes: int = 1024,
    ) -> None:
        self.channel = channel
        self.test_name = test_name
        self.c_rate_ah = c_rate_ah
        self.v_max_v = v_max_v
        self.v_min_v = v_min_v
        self.v_max_safety_limit_v = v_max_safety_limit_v
        self.v_min_safety_limit_v = v_min_safety_limit_v
        self.i_max_safety_limit_a = i_max_safety_limit_a
        self.i_min_safety_limit_a = i_min_safety_limit_a
        self.data_record_time_s = data_record_time_s
        self.data_record_voltage_delta_vbys = data_record_voltage_delta_vbys
        self.data_record_current_delta_abys = data_record_current_delta_abys
        self.test_procedure = test_procedure
        self.server_ip = server_ip
        self.json_server_port = json_server_port
        self.tcp_server_port = tcp_server_port
        self.msg_buffer_size_bytes = msg_buffer_size_bytes

    def to_dict(self) -> Dict[str, Any]:
        return {
            'channel': self.channel,
            'test_name': self.test_name,
            'c_rate_ah': self.c_rate_ah,
            'v_max_v': self.v_max_v,
            'v_min_v': self.v_min_v,
            'v_max_safety_limit_v': self.v_max_safety_limit_v,
            'v_min_safety_limit_v': self.v_min_safety_limit_v,
            'i_max_safety_limit_a': self.i_max_safety_limit_a,
            'i_min_safety_limit_a': self.i_min_safety_limit_a,
            'data_record_time_s': self.data_record_time_s,
            'data_record_voltage_delta_vbys': self.data_record_voltage_delta_vbys,
            'data_record_current_delta_abys': self.data_record_current_delta_abys,
            'test_procedure': self.test_procedure,
            'server_ip': self.server_ip,
            'json_server_port': self.json_server_port,
            'tcp_server_port': self.tcp_server_port,
            'msg_buffer_size_bytes': self.msg_buffer_size_bytes,
        }


class PyMacNet:
    def __init__(self, expConfig: CyclerConfig, pyMacNetConfig: PyMacNetConfig) -> None:
        self.expConfig = expConfig
        self.pyMacNetConfig = pyMacNetConfig
        
    def convert(self, additional_properties: Optional[Dict[str, Any]] = None) -> PyMacNetConfig:
        # TODO: we need to be able to pass the IP, Port, test name (we shouldn't default here)
        config = PyMacNetConfig()

        # Map the global parameters from Object 1 to Object 2
        config.v_max_v = self.expConfig.globals.V_max
        config.v_min_v = self.expConfig.globals.V_min

        # Set additional properties from the user
        if additional_properties:
            for key, value in additional_properties.items():
                if hasattr(config, key):
                    setattr(config, key, value)

        return config


    def run_test(self, config: PyMacNetConfig):
        """One shot test
        """
        maccor_interface = pymacnet.MaccorInterface(config.to_dict())
        if not maccor_interface.start():
            sys.exit("failed to create connection!")

        if maccor_interface.start_test_with_procedure():
            print("Test started!")

    def direct_control(self):
        """Configure on the fly
        """

    def read_signals(self):
        """Read signals: Limitations: 1Hz
        """
        pass
