COUNT_VALUES = 12
SEPARATOR = ";"


class ParseError(BaseException):
    pass


def parse_radio(data: str) -> dict:
    input_values = [i.strip() for i in data.split(SEPARATOR) if i != " "]

    match input_values:
        case [
            time,
            lenses_voltage,
            lenses_amperage,
            standard_voltage,
            standard_amperage,
            # x,
            # y,
            top_left,
            bottom_left,
            top_right,
            bottom_right,
            temp1,
            temp2,
        ]:
            result = {
                "time": time,
                "lenses_panels": {
                    "voltage": lenses_voltage,
                    "amperage": lenses_amperage,
                    "x": 1,
                    "y": 2,
                    "temperature": temp1,
                },
                "standard_panels": {
                    "voltage": standard_voltage,
                    "amperage": standard_amperage,
                    "temperature": temp2,
                },
                "light_intensity": {
                    "top_left": top_left,
                    "bottom_left": bottom_left,
                    "top_right": top_right,
                    "bottom_right": bottom_right,
                },
            }
        case _:
            raise ParseError()

    return result
