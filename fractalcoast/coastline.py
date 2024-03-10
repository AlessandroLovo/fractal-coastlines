import numpy as np

def place_along_line(z:np.ndarray, start:tuple, end:tuple, touches_endpoints=False) -> np.ndarray:
    '''
    Place a set of equally spaced points with orthogonal coordinate `z` along a line between `start` and `end`.

    Parameters
    ----------
    z : np.ndarray
        array of orthogonal coordinate
    start : 2-ple
        coordinates of the beginning of the line
    end : 2-ple
        coordinates of the end of the line
    touches_endpoints : bool, optional
        If true, z is linearly detrended such that the first and last point are exactly `start` and `end`, by default False

    Returns
    -------
    np.ndarray with shape (len(z), 2)
        coordinates of the placed points
    '''
    x1, y1 = start
    x2, y2 = end
    if touches_endpoints:
        z = z - z[0]
        z = z - np.linspace(0,1,len(z))*z[-1]

    points = np.zeros((len(z),2), dtype=float) + np.array((x1,y1))
    vec_par = np.array((x2 - x1, y2 - y1))/(len(z) - 1)
    vec_perp = np.array((-vec_par[1], vec_par[0]))
    for i in range(len(z)):
        points[i] += z[i] * vec_perp + i*vec_par
    return points

def recursive_fractal_segment(start, end, generator, zs=10, iterations=None, regenerate=True, total_points=1000) -> np.ndarray:
    '''
    Recursively generate a segment of coastline

    Parameters
    ----------
    start : 2-ple
        coordinates of the start point
    end : 2-ple
        coordinates of the end point
    generator : subclass dynamics.Base
        Must implement function `traj`
    zs : int or np.ndarray, optional
        number or set of points that each segment will have, by default 10
    iterations : int or None, optional
        number of iterations to perform, if None it is determined automatically by parameter `total_points`, by default None
    regenerate : bool, optional
        Whether to regenarate the noise at each iteration. For a realistic coastline use True. If False, the coastline will exhibit self similarity, by default True
    total_points : int or None, optional
        Approximate total number of points to have in the stretch of coastline, by default 1000

    Returns
    -------
    np.ndarray with shape (N,2)
        coordinates of the generated points
    '''
    nz = zs if isinstance(zs, int) else len(zs)
    if iterations is None:
        iterations = int(np.log(total_points)/np.log(nz))
        print(f'{iterations = }')
    if isinstance(zs,int) or regenerate:
        zs = generator.traj(length=nz)
        # print(zs)
    points =  place_along_line(zs, start, end, touches_endpoints=True)
    
    if iterations == 1:
        return points
    else:
        ps = []
        for i in range(points.shape[0] - 1):
            _ps = recursive_fractal_segment(points[i], points[i+1], generator, zs=zs, iterations=iterations-1, regenerate=regenerate)
            ps.append(_ps[:-1])
        ps.append(_ps[-1:])
        return np.concatenate(ps, axis=0)