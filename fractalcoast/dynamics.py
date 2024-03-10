import numpy as np

class Base():
    '''
    Base class for Stochastic ODE dynamics of the kind

    $$ \dot{x} = f(x,t) $$

    Subclasses must implement function `f`, which returns a 2-ple with drift and noise terms.
    '''
    def __init__(self, dt=0.01):
        self.dt = dt

    def f(self, x, t) -> tuple:
        raise NotImplementedError
    
    def update(self, t, x) -> tuple:
        '''
        (t,x) -> (t + dt, x + f(x,t))
        '''
        drift, noise = self.f(x,t)
        dx = drift*self.dt + noise*np.sqrt(self.dt)
        return t + self.dt, x + dx
    
    def traj(self, length=100, x0=0, t0=0):
        '''
        Starting from (t0, x0), generate a trajectory with `length` points using Euler's integration method
        '''
        t = t0
        x = x0
        seq = [x0]
        for i in range(length - 1):
            t, x = self.update(t, x)
            seq.append(x)
        return np.array(seq)


class OrnsteinUhlenbeck(Base):
    def __init__(self, mu=0, theta=1, sigma=1, dt=0.01):
        '''
        Ornstein-Uhlenbeck process:

        $$ \dot{x} = f(x,t) = \theta (\mu - x) + \sigma \epsilon $$
        '''
        super().__init__(dt=dt)
        self.mu = mu
        self.theta = theta
        self.sigma = sigma

    def f(self, x, t):
        return (self.mu - x)*self.theta, self.sigma*np.random.standard_normal()
        