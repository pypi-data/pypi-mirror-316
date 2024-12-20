from bitarray import bitarray
from bitarray.util import (
    zeros, 
    ones, 
    int2ba,
    ba2int,
)
from easybits.util import is_bit_string
from easybits.errors import (
    NotEnoughBits, 
    IntegersRequireLength, 
    IntegerAdditionRequiresSameLength,
)

class Bits(bitarray):
    """A wrapper around bitarray with a more idiomatic interface for beginners.
    - Integers are always signed.
    """

    @classmethod
    def zeros(cls, length):
        return Bits(zeros(length))

    @classmethod
    def ones(cls, length):
        return Bits(ones(length))

    def __new__(cls, value, length=None, encoding='ascii'):
        if isinstance(value, bytes):
            bits = bitarray()
            bits.frombytes(value)
        elif isinstance(value, bool):
            bits = bitarray([value])
        elif isinstance(value, int):
            if not length:
                raise IntegersRequireLength()
            bits = int2ba(value, length=length, signed=True)
        elif isinstance(value, str):
            if is_bit_string(value):
                bits = bitarray(value)
            else:
                bits = bitarray()
                bits.frombytes(value.encode(encoding))
        elif isinstance(value, list):
            bits = bitarray(value)
        elif isinstance(value, bitarray):
            bits = value
        else:
            raise ValueError(f"Can't create bits from {value}")
        if length:
            if length < len(bits):
                raise NotEnoughBits(value, length)
            else:
                sized_bits = bitarray(length)
                sized_bits[-len(bits):] = bits
        else:
            sized_bits = bits
        return super().__new__(cls, sized_bits)

    def __str__(self):
        bits = self.to01()

    def __repr__(self):
        return self.to01()

    @property
    def bool(self):
        return [bool(b) for b in  self.tolist()]

    @property
    def int(self):
        return ba2int(self, signed=True)

    @property
    def bytes(self):
        return self.tobytes()

    @property
    def ascii(self):
        return self.bytes.decode("ascii")

    def __add__(self, other):
        """Performs bitwise addition on `self` and `other`. Does not
        check for overflow.
        """
        a, b = self, Bits(other)
        if not len(a) == len(b):
            raise IntegerAdditionRequiresSameLength()
        result = Bits.zeros(len(a))
        carry = 0
        for i in reversed(range(len(a))):
            result[i] = a[i] ^ b[i] ^ carry
            carry = (a[i] & b[i]) | (a[i] & carry) | (b[i] & carry)
        return result

    def __sub__(self, other):
        """Performs bitwise addition on `self` and `other`. Does not
        check for overflow.
        """
        a, b = self, Bits(other)
        if not len(a) == len(b):
            raise IntegerAdditionRequiresSameLength()
        return a + (-b)

    def __neg__(self):
        """Treats `self` as an integer, and flips its sign.
        """
        if self[0]:
            return ~self + Bits(1, length=len(self))
        else:
            return ~(self + Bits(-1, length=len(self)))
