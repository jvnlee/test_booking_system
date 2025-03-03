class NotEnoughParticipantCapacityException(Exception):
    def __init__(self, message="The requested number of participants exceeds the available capacity."):
        super().__init__(message)