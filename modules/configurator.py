from typing import List, Union
from modules.cyclerConfig import CyclerConfig, ExperimentConfig, Sequence, Instruction, TerminationCondition
from modules.drivers.pymacnet import PyMacNet, PyMacNetConfig

class Configurator:
    def __init__(self, yaml_data: dict, driverName: str, additional_configs= None) -> None:
        self.yaml_data = yaml_data
        self.driverName = driverName
        self.additional_configs =additional_configs
        self.deserialized_data = self.deserialize_cycler_config()

    def get_driver_config(self) -> PyMacNetConfig:
        if self.driverName == "maccor":
            driver = PyMacNet(self.deserialized_data, self.additional_configs)

        return driver.convert(self.additional_configs)

    def deserialize_cycler_config(self) -> CyclerConfig:
        globals_data = self.yaml_data['globals']
        experiment_config = ExperimentConfig(
            V_unit=globals_data['V_unit'],
            C_unit=globals_data['C_unit'],
            T_unit=globals_data['T_unit'],
            duration_unit=globals_data['duration_unit'],
            V_min=globals_data['V_min'],
            V_max=globals_data['V_max'],
            T_ambient=globals_data['T_ambient'],
            T_max=globals_data['T_max'],
        )

        def deserialize_sequence(sequence_data: List[Union[dict, Sequence]]) -> List[Union[Instruction, Sequence]]:
            sequence = []
            for item in sequence_data:
                if 'type' in item:
                    termination_data = item.get('termination', [])
                    termination_conditions = [TerminationCondition(**t) for t in termination_data]
                    instruction = Instruction(
                        type=item['type'],
                        value=item.get('value', None),
                        time=item['time'],
                        termination=termination_conditions,
                        name=item.get('name'),
                        repeat=item.get('repeat', 1)
                    )
                    sequence.append(instruction)
                elif 'sequence' in item:
                    nested_sequence = deserialize_sequence(item['sequence'])
                    sequence.append(Sequence(
                        sequence=nested_sequence,
                        name=item.get('name'),
                        repeat=item.get('repeat', 1)
                    ))
            return sequence

        instructions_data = self.yaml_data['instructions']
        instructions = deserialize_sequence(instructions_data)

        return CyclerConfig(globals=experiment_config, instructions=instructions)