class ReservationNotFoundException(Exception):
    def __init__(self, message="Reservation does not exists."):
        super().__init__(message)