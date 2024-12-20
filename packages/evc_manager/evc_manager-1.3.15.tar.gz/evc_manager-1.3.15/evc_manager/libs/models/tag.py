""" Class Tag part of EthernetVirtualCircuit"""

from typing import Union, List


class Tag(object):
    """Class Tag part of EthernetVirtualCircuit"""

    def __init__(self):
        self._type: str = "vlan"  # it has to be a str. 'vlan' is the default.
        self._value: Union[int, str, List[List[int]]] = (
            0  # It can be an integer, "untagged", or range of integers
        )

    # Variables

    @property
    def type(self) -> str:
        """Tag Type property

        :return: self._type
        """
        return self._type

    @type.setter
    def type(self, uni_type) -> None:
        """Tag type setter

        :param uni_type: tag type. Must be or 'vlan' or 'mpls'
        """
        uni_type = self._format_uni_type(uni_type)

        if self._assert_valid_type(uni_type):
            self._type = uni_type

    @property
    def value(self) -> Union[int, str, List[List[int]]]:
        """Tag Value property

        :return: self._value
        """
        return self._value

    @value.setter
    def value(self, uni_value: Union[int, str, List[List[int]]]) -> None:
        """Tag Value setter

        :param uni_value: tag value. Must be int from [-1,1-4095], "untagged", or a List of ranges
        :return:
        """
        final_value: Union[str, int, None] = None

        if self._assert_valid_str(uni_value):
            final_value = uni_value

        elif self._assert_valid_range(uni_value):
            final_value = uni_value

        elif self._assert_valid_int(uni_value):
            final_value = int(uni_value)

        if final_value:
            self._value = final_value

    # Public methods

    def contains_value(self, tag_value: Union[int, str, List[int]]) -> bool:
        """A public method to check if the current EVC contains the tag value"""
        currentEVCValue = self.value

        if isinstance(currentEVCValue, (str, int)):
            if isinstance(tag_value, (int, str)):
                return currentEVCValue == tag_value
            if isinstance(currentEVCValue, int) and isinstance(tag_value, list):
                return tag_value[0] <= currentEVCValue <= tag_value[1]
            return False

        for vlan_range in currentEVCValue:
            if isinstance(tag_value, int) and vlan_range[0] <= tag_value <= vlan_range[1]:
                return True

            # A range can be compared to another range in the following conditions:
            # 1: Range 1 has a lower and/or upper boundary within range 2
            # 2: Range 1 does not have a lower or upper boundary within range 2
            # 3: Range 1 is equal to range 2
            # 4: Range 1 encompasses range 2

            elif isinstance(tag_value, list) and (
                vlan_range[0] <= tag_value[0] <= vlan_range[1]
                or vlan_range[0] <= tag_value[1] <= vlan_range[1]
                or vlan_range[0] >= tag_value[0]
                and tag_value[1] >= vlan_range[1]
            ):
                return True

        return False

    # Private methods

    def _equals_evc(self, other_tag_value: Union[int, str, List[List[int]]]):
        """
        A private method to check if the current EVC contains tag values found in the
        other EVC
        """
        currentEVCValue = self.value

        # Conditionals where both are str/int

        if isinstance(currentEVCValue, int) and isinstance(other_tag_value, int):
            return currentEVCValue == other_tag_value

        elif isinstance(currentEVCValue, str) or isinstance(other_tag_value, str):
            return all(
                [
                    isinstance(currentEVCValue, str),
                    isinstance(other_tag_value, str),
                    currentEVCValue == other_tag_value == "untagged",
                ]
            )

        # Conditionals where one is a list and the other is an int

        elif isinstance(currentEVCValue, int) and isinstance(other_tag_value, list):
            for tag_range in other_tag_value:
                if len(tag_range) == 1:
                    if tag_range == currentEVCValue:
                        return True
                elif tag_range[0] <= currentEVCValue <= tag_range[1]:
                    return True
            return False

        elif isinstance(currentEVCValue, list) and isinstance(other_tag_value, int):
            for vlan_range in currentEVCValue:
                if len(vlan_range) == 1:
                    if vlan_range == other_tag_value:
                        return True
                elif vlan_range[0] <= other_tag_value <= vlan_range[1]:
                    return True
            return False

        # Loop over both ranges

        # A range can be compared to another range in the following conditions:
        # 1: Range 1 has a lower and/or upper boundary within range 2
        # 2: Range 1 does not have a lower or upper boundary within range 2
        # 3: Range 1 is equal to range 2
        # 4: Range 1 encompasses range 2

        for vlan_range in currentEVCValue:
            for tag_range in other_tag_value:
                if (
                    vlan_range[0] <= tag_range[0] <= vlan_range[1]
                    or vlan_range[0] <= tag_range[1] <= vlan_range[1]
                    or vlan_range[0] >= tag_range[0]
                    and tag_range[1] >= vlan_range[1]
                ):
                    return True

        return False

    def _assert_valid_range(self, uni_value: Union[int, List[List[int]]]) -> bool:
        """Assert that the provided value is a valid range"""
        if not isinstance(uni_value, list):
            return False

        for tag_range in uni_value:
            if not isinstance(tag_range, list) or len(tag_range) <= 0 or len(tag_range) >= 3:
                msg = (
                    "Error: VLAN IDs must be a list of ranges in"
                    + " the format [[x, y], [z], ...], where x, y, and z are integers."
                )
                raise ValueError(msg)

            if len(tag_range) < 2:
                tag_range.append(tag_range[0])

            self._assert_valid_int(tag_range[0])
            self._assert_valid_int(tag_range[1])

        return True

    def _assert_valid_int(self, uni_value: int) -> bool:
        """Assert that the provided value is a valid int value"""
        if not isinstance(uni_value, int):
            try:
                uni_value = int(uni_value)
            except TypeError as exc:
                msg = "Error: Tag Value must be integer"
                raise ValueError(msg) from exc

        if self._is_vlan() and not (uni_value == -1 or 1 <= uni_value <= 4095):
            msg = "Error: VLAN IDs must be int and be -1 or between 1 and 4095"
            raise ValueError(msg)

        if not self._is_vlan() and not 1 <= uni_value <= 1048576:
            msg = "Error: MPLS labels must be integer and between 1-1048576"
            raise ValueError(msg)

        return True

    def _assert_valid_str(self, uni_value: Union[int, str, List[List[int]]]) -> bool:
        """
        Assert that the provided value is a valid string value
        """
        if not isinstance(uni_value, str) or uni_value.isdigit():
            return False

        if uni_value not in {"untagged"}:
            msg = "Error: VLAN ID must be untagged if it is a string"
            raise ValueError(msg)

        return True

    def _assert_valid_type(self, uni_type: str) -> bool:
        """
        Assert that the provided uni_type value is a valid string
        """
        if uni_type not in {"vlan", "mpls"}:
            msg = "Error: Tag value must be or 'vlan' or 'mpls'"
            raise ValueError(msg)
        return True

    def _format_uni_type(self, uni_type: str) -> str:
        """
        Checks if the provided uni_type value is a string, then formats it to lowercase
        """
        if not isinstance(uni_type, str):
            msg = "Error: Tag value must be of type str"
            raise ValueError(msg)
        return uni_type.lower()

    def _is_vlan(self):
        """
        :return:
        """
        return self.type in {"vlan"}

    # Override methods

    def __eq__(self, other: object) -> bool:
        """Compare Tags"""
        return other and all(
            [
                self.type == other.type,
                self._equals_evc(other.value),
            ]
        )

    def __repr__(self) -> str:
        """Convert the tag into a string"""
        return f"Type: {self.type}\nValue: {self.value}l\n"
