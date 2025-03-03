class TestScheduleNotFoundException(Exception):
    def __init__(self, message="No test schedules available for the request"):
        super().__init__(message)