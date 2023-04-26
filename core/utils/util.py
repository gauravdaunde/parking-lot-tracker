

def register_new_parking_lot_level(level_name, level_size):
    """
        Util function to create new ParkingLotLevel instance

        :param level_name: string contains level name
        :param level_size: integer denotes size of parking lot level
        :return: returns instance of ParkingLotLevel
    """
    from core.logic import ParkingLotLevel
    return ParkingLotLevel(level_name, level_size)


def get_parking_lot_level_object_for_level_name(level_name, available_levels):
    """
        Util function gives ParkingLotLevel instance for given level name
        it matches given name in ParkingLotLevel and return if found a match or returns nothing

        :param level_name: string contains level name
        :param available_levels: list containing instances of ParkingLotLevel
        :return: instance of ParkingLotLevel of matched else None
    """
    for level in available_levels:
        if level.name == level_name:
            return level


def can_create_parking_lot_level(level_name, available_levels):
    """
        Util function to validate whether new ParkingLotLevel can be created with given name
        it checks if any instance present for given name or not if present we can't create another instance
        with same name

        :param level_name: string contains level name
        :param available_levels: list containing instances of ParkingLotLevel
        :return: returns True if level can be created with given name else returns False
    """
    is_level_with_same_name_already_exists = bool(get_parking_lot_level_object_for_level_name(
        level_name, available_levels
    ))

    return not is_level_with_same_name_already_exists


def validate_level_name(level_name, raise_error=False):
    """
        Util function to validate level name, it should be valid string

        :param level_name: level name
        :param raise_error: boolean to control whether to raise error or not
        :return: None
    """
    try:
        str(level_name)
    except ValueError:
        error_msg = 'Please Enter valid name for level'
        if raise_error:
            raise ValueError(error_msg)
        else:
            print(error_msg)


def validate_lot_size(level_size, raise_error=False):
    """
        Util function to validate lot size, it should be an integer

        :param level_size: integer
        :param raise_error: boolean to control whether to raise error or not
        :return: None
    """

    try:
        str(level_size)
    except ValueError:
        error_msg = 'Please Enter valid size (integer) for level'
        if raise_error:
            raise ValueError(error_msg)
        else:
            print(error_msg)
