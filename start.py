import click
import logging

from core.constants import MENU_CHOICES, AVAILABLE_LEVELS, LEVEL_SIZES
from core.utils.util import (register_new_parking_lot_level, get_parking_lot_level_object_for_level_name,
                             can_create_parking_lot_level)

log = logging.getLogger(__name__)


if __name__ == '__main__':
    choice = None
    parking_lot_levels = []

    for level_name, level_size in zip(AVAILABLE_LEVELS, LEVEL_SIZES):
        if can_create_parking_lot_level(level_name, parking_lot_levels):
            parking_lot_levels.append(register_new_parking_lot_level(level_name, level_size))

    while True:
        click.clear()
        print('Welcome to Parking Lot Traker')
        print(MENU_CHOICES)
        choice = input('Enter your Choice: ')
        click.clear()

        match choice:

            case '1':
                print('Displaying Parking Lot Levels')
                print('%-*s | %s' % (7, 'Level Name', 'Level Size'))
                for level in parking_lot_levels:
                    print('%-*s %s' % (17, level.name, level.size))

            case '2':
                level_name = input('Enter Parking Lot Level name: ')
                while True:
                    level_size = input('Enter Parking Lot Level size (int): ')
                    try:
                        level_size = int(level_size)
                        break
                    except ValueError:
                        print('Please Enter Valid Integer')
                if can_create_parking_lot_level(level_name, parking_lot_levels):
                    new_level = register_new_parking_lot_level(level_name, level_size)
                    print(f'Parking Lot Level with name {level_name} is created')
                    parking_lot_levels.append(new_level)
                else:
                    print(f'Parking Lot level with name {level_name} already exists please '
                          f'try again with different name')

            case '3':
                level_name = input('Please Enter Level Name: ')
                level = get_parking_lot_level_object_for_level_name(level_name, parking_lot_levels)
                if level:
                    parking_spot = level.display()
                    if parking_spot:
                        break
                else:
                    print(f"You may have entered wrong Level name, "
                          f"please choose from this {','.join(level.name for level in parking_lot_levels)} "
                          f"or You can create one")
            case '4':
                vehicle_id = input('Please enter Vehicle ID: ')
                parking_spot = None
                for level in parking_lot_levels:
                    parking_spot = level.allocate_parking_spot(vehicle_id)
                    if parking_spot:
                        print(f'Allocated Parking Spot is: {parking_spot}')
                        break

                if parking_spot is None:
                    print('There are no free space for parking, Sorry for inconvenience')
            case '5':
                vehicle_id = input('Please enter Vehicle ID: ')
                parking_spot = None
                for level in parking_lot_levels:
                    parking_spot = level.get_allocated_spot_for_vehicle(vehicle_id)
                    if parking_spot:
                        break

                if parking_spot:
                    print(f'Your vehicle is parked at {parking_spot}')
                else:
                    print('You may have entered wrong Vehicle ID or your vehicle is not parked here.')
            case '6':
                level_name = input('Enter Parking Lot Level name: ')
                spot_number = input('Enter Parking Lot Level number: ')
                parking_spot = None
                level = get_parking_lot_level_object_for_level_name(level_name, parking_lot_levels)
                if level:
                    parking_spot = level.get_parking_spot_details(spot_number)
                    if parking_spot and parking_spot.is_free is False:
                        print('Parking Spot is Occupied, please check another spot')
                    else:
                        print('Parking Spot is free for parking')
                else:
                    print(f"You may have entered wrong Level name, "
                          f"please choose from this {','.join(level.name for level in parking_lot_levels)} "
                          f"or You can create one")
            case _:
                print('\n Bye Bye... \n')
                break

        print()
        if input('Press Any Key to continue'):
            continue
