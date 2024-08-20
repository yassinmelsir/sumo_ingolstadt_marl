import random


class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.buffer = []
        self.buffer_size = buffer_size
        self.batch_size = batch_size

    def add(self, experience):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append(experience)

    def sample(self):
        return random.sample(self.buffer, self.batch_size)

    def __len__(self):
        return len(self.buffer)