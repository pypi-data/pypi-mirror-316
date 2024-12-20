class BitsError(Exception):
    message = "Bits error"

    def __str__(self):
        return self.message

class NotEnoughBits(BitsError):
    def __init__(self, obj, length):
        self.message = f"{obj} cannot fit into {length} bits."

class IntegersRequireLength(BitsError):
    message = "Binary representations of integers require that a length be provided."

class IntegerAdditionRequiresSameLength(BitsError):
    message = "Can only add integers of the same length."
