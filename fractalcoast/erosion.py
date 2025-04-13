import numpy as np

class Roll4:
    def __init__(self):
        self.lengths = np.ones(4)
        self.directions = ['N', 'E', 'S', 'W']

    def __len__(self):
        return len(self.directions)

    def reverse_direction(self, direction):
        if isinstance(direction, int):
            return (direction + len(self.directions)//2) % len(self.directions)
        return self.directions[self.reverse_direction(self.directions.index(direction))]

    def __call__(self, array: np.ndarray, direction: int|str, fill_value:float=0) -> np.ndarray:
        if isinstance(direction, int):
            direction = self.directions[direction]

        if direction == 'N':
            a = np.roll(array, 1, axis=1)
            a[:,0] = fill_value
        elif direction == 'E':
            a = np.roll(array, 1, axis=0)
            a[0,:] = fill_value
        elif direction == 'S':
            a = np.roll(array, -1, axis=1)
            a[:,-1] = fill_value
        elif direction == 'W':
            a = np.roll(array, -1, axis=0)
            a[-1,:] = fill_value
        else:
            raise ValueError(f'Invalid direction: {direction}')

        return a
    

class Roll8(Roll4):
    def __init__(self):
        self.lengths = np.array([1,np.sqrt(2)]*4)
        self.directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def __call__(self, array: np.ndarray, direction: int|str, fill_value:float=0) -> np.ndarray:
        if isinstance(direction, int):
            direction = self.directions[direction]

        if direction in super().directions:
            return super().__call__(array, direction, fill_value)
        
        if direction == 'NE':
            return super().__call__(super().__call__(array, 'N', fill_value), 'E', fill_value)
        elif direction == 'SE':
            return super().__call__(super().__call__(array, 'S', fill_value), 'E', fill_value)
        elif direction == 'SW':
            return super().__call__(super().__call__(array, 'S', fill_value), 'W', fill_value)
        elif direction == 'NW':
            return super().__call__(super().__call__(array, 'N', fill_value), 'W', fill_value)
        
        else:
            raise ValueError(f'Invalid direction: {direction}')