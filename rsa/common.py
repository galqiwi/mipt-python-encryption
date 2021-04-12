
# Быстрое возведение в степень
def power_mod(value, power, mod):
    value %= mod

    power_bin = []

    while power > 0:
        power_bin.append(power % 2)
        power //= 2
    power_bin.reverse()

    out = 1
    for bit in power_bin:
        out = (out * out) % mod
        if bit == 1:
            out = (out * value) % mod

    return out
