
def is_bit_string(value):
    bit_chars = {'1', '0', ' '}
    return not (set(value) - bit_chars)

