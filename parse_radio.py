COUNT_VALUES = 12
SEPARATOR = ";"


class ParseError(BaseException):
    pass


def parse_radio(data: str) -> dict:
    input_values = [i.strip() for i in data.split(SEPARATOR) if i != " "]

    match input_values:
        case [
            time,
            action,
            lenses_voltage,
            lenses_amperage,
            standard_voltage,
            standard_amperage,
            x,
            y,
            li_top,
            li_bottom,
            li_left,
            li_right,
        ]:
            result = {
                "time": time,
                "currect_action": action,
                "lenses_panels": {
                    "voltage": lenses_voltage,
                    "amperage": lenses_amperage,
                    "x": x,
                    "y": y,
                },
                "standard_panels": {
                    "voltage": standard_voltage,
                    "amperage": standard_amperage,
                },
                "light_intensity": {
                    "top": li_top,
                    "bottom": li_bottom,
                    "left": li_left,
                    "right": li_right,
                },
            }
        case _:
            raise ParseError()

    return result
