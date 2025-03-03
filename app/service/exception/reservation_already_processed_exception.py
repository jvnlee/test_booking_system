class ReservationAlreadyProcessedException(Exception):
    def __init__(self, message="Cannot perform update because this reservation has already been processed."):
        super().__init__(message)