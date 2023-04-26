import logging

from .utils.util import validate_level_name, validate_lot_size

log = logging.getLogger(__name__)


class ParkingSpot:
    """
        Class representing single spot in a Parking Lot Level
    """
    def __init__(self, level, spot_number, vehicle_id=None):
        self.level = level
        self.spot_number = spot_number
        self.vehicle_id = vehicle_id

    def __str__(self):
        return f'{self.level}-{self.spot_number}'

    @property
    def is_free(self):
        return self.vehicle_id is None

    @staticmethod
    def get_parking_spot(parking_spot_map, level, spot_number):
        if (level, spot_number) in parking_spot_map:
            parking_spot = parking_spot_map[(level, spot_number)]
        else:
            log.debug(f'Creating new ParkingSpot instance for level with name {level} and '
                      f'{spot_number} as spot number')
            parking_spot = ParkingSpot(level, spot_number)
            parking_spot_map[(level, spot_number)] = parking_spot

        return parking_spot

    def allocate_parking_spot_to_vehicle(self, vehicle_id_to_allocated_spot_map, vehicle_id):
        log.info(f'Allocating Parking Spot {self} to Vehicle ID: {vehicle_id}')
        self.vehicle_id = vehicle_id
        vehicle_id_to_allocated_spot_map[vehicle_id] = self

    def deallocate_parking_spot(self, vehicle_id_to_allocated_spot_map):
        log.info(f'De-allocating Parking Spot {self} from Vehicle ID: {self.vehicle_id}')
        vehicle_id_to_allocated_spot_map[self.vehicle_id] = None
        self.vehicle_id = None


class ParkingLotLevel:
    """
        class represents Level in Parking Lot
    """
    parking_spot_map = {}
    vehicle_id_to_allocated_spot_map = {}

    def __init__(self, level, level_size):
        validate_level_name(level)
        validate_lot_size(level_size)
        self.name = level
        self.size = level_size
        self._available_parking_spots = None
        self.parking_lot_data = {}

    @property
    def available_parking_spots(self):
        if self._available_parking_spots is None:
            self._available_parking_spots = self.get_available_parking_spots()

        return self._available_parking_spots

    def get_parking_number(self, vehicle_id):
        return self.parking_lot_data.get(vehicle_id)

    def get_parking_spot(self):
        return self.available_parking_spots.pop()

    def allocate_parking_spot(self, vehicle_id):
        parking_spot = self.get_parking_spot()
        if parking_spot:
            level, spot_number = parking_spot
            spot = ParkingSpot.get_parking_spot(self.parking_spot_map, level, spot_number)
            spot.allocate_parking_spot_to_vehicle(self.vehicle_id_to_allocated_spot_map, vehicle_id)
            return spot

    def deallocate_parking_spot(self, vehicle_id):
        parking_spot = self.vehicle_id_to_allocated_spot_map.get(vehicle_id)
        if parking_spot:
            parking_spot.deallocate_parking_spot()

    def get_available_parking_spots(self):
        return [
            (self.name, str(i))
            for i in range(1, self.size + 1)
        ]

    def get_allocated_spot_for_vehicle(self, vehicle_id):
        return self.vehicle_id_to_allocated_spot_map.get(vehicle_id)

    def get_parking_spot_details(self, spot_number):
        try:
            spot_number = int(spot_number)
        except ValueError:
            print('Please Enter Valid Spot Number')
            return

        return self.parking_spot_map.get((self.name, spot_number))

    def display(self):
        for level_name, spot_number in self.get_available_parking_spots():
            parking_spot = self.get_parking_spot_details(spot_number)
            text = 'Is Open for Parking'
            if parking_spot and parking_spot.is_free is False:
                text = f'Is occupied by Vehicle with ID, {parking_spot.vehicle_id}'
            print(f'{level_name}-{spot_number}: {text}')
