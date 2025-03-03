class ReservationDeadlineExceededException(Exception):
    def __init__(self, message="Reservations must be made at least 3 days prior to the test date"):
        super().__init__(message)