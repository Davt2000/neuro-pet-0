class Pool:
    def __init__(self, width, length, number_of_gates, resistance):
        self.w = width
        self.l = length
        self.n = number_of_gates
        self.spawn_space = (4*width/5, 4*length/5)
        self.r = resistance

    def __str__(self):
        out = "Pool sides: {}x{};\n" \
              "Gate spawn space: {}x{}\n" \
              "Number of gates {}" \
              "Water ".format(self.l, self.w, self.spawn_space[0], self.spawn_space[1], self.n)
        return out

