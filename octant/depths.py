def zatr(ncfile, time=None):
    """
    ZATR finds z at rho points (positive up, zero at rest surface) 
    If zeta = True for all times with the calculated value of zeta, 
    otherwise, for one time calculated with zeta = 0 (default)
    
    ncfile - NetCDF file to use (a ROMS history file or netcdf object).
    """
    warnings.warn('Deprecated -- use Depths class instead.')
    nc = Dataset(ncfile)
    h = nc.variables['h'][:]
    h = atleast_2d(h)
    hc = nc.variables['hc'][:]
    Cs_r = nc.variables['Cs_r'][:]
    try:
        sc_r = nc.variables['sc_r'][:]  # roms-2.x format
    except:
        sc_r = nc.variables['s_rho'][:]  # roms-3.x format
    
    if time is None:
        zeta = zeros(h.shape, 'd')
    else:
        zeta = nc.variables['zeta'][time]
    
    if ndim(zeta) == 2:
        zeta = zeta[newaxis, :]
    
    N = len(nc.dimensions['N'])
    ti = zeta.shape[0]
    z = empty((ti, N) + h.shape, 'd')
    for n in arange(ti):
        for  k in arange(N):
            z0=(sc_r[k]-Cs_r[k])*hc + Cs_r[k]*h
            z[n,k,:] = z0 + zeta[n,:]*(1.0 + z0/h)
    
    return(squeeze(z))

def zatw(ncfile, time=None):
    """
    ZATW finds z at w-points (positive up, zero at rest surface) 
    If zeta = True for all times with the calculated value of zeta, 
    otherwise, for one time calculated with zeta = 0 (default)
    
    ncfile - NetCDF file to use (a ROMS history file or netcdf object).
    """
    warnings.warn('Deprecated -- use Depths class instead.')
    nc = Dataset(ncfile)
    h = nc.variables['h'][:]
    hc = nc.variables['hc'][:]
    Cs_w = nc.variables['Cs_w'][:]
    try:
        sc_w = nc.variables['sc_w'][:]  # roms-2.x format
    except:
        sc_w = nc.variables['s_w'][:]  # roms-3.x format
    
    if time is None:
        zeta = zeros(h.shape, 'd')
    else:
        zeta = nc.variables['zeta'][time]
    
    if ndim(zeta) == 2:
        zeta = zeta[newaxis, :]
    
    N = len(nc.dimensions['N']) + 1
    ti = zeta.shape[0]
    z = empty((ti, N) + h.shape, 'd')
    for n in arange(ti):
        for  k in arange(N):
            z0=(sc_w[k]-Cs_w[k])*hc + Cs_w[k]*h
            z[n,k,:] = z0 + zeta[n,:]*(1.0 + z0/h)
    
    return(squeeze(z))

def scoordr(h,hc,theta_b,theta_s,N):
    """
    z=scoordr(h,hc,theta_b,theta_s,N)
    SCOORDR finds z at rho points (positive up, zero at rest surface) 
     h = array of depths (e.g., from grd file)
     hc = critical depth
     theta_b = surface/bottom focusing parameter
     theta_s = strength of focusing parameter
     N number of vertical rho-points
    """
    warnings.warn('Deprecated -- use Depths class instead.')
    sc_w = arange(-1, 1./N, 1./N, dtype='d')
    sc_r = 0.5*(sc_w[1:]+sc_w[:-1])
    Cs_r = (1-theta_b)*sinh(theta_s*sc_r)/sinh(theta_s)\
          +0.5*theta_b\
          *(tanh(theta_s*(sc_r+0.5))-tanh(0.5*theta_s))/tanh(0.5*theta_s)
    z_r = empty((N,) + h.shape, dtype='d')
    for  k in arange(N):
        z_r[k,:]=(sc_r[k]-Cs_r[k])*hc + Cs_r[k]*h
    return(squeeze(z_r))

def scoordw(h,hc,theta_b,theta_s,N):
    """
    z=scoordr(h,hc,theta_b,theta_s,N)
    SCOORDW finds z at rho points (positive up, zero at rest surface) 
     h = array of depths (e.g., from grd file)
     hc = critical depth
     theta_b = surface/bottom focusing parameter
     theta_s = strength of focusing parameter
     N number of vertical w-points (one more than rho-points)
    """
    warnings.warn('Deprecated -- use Depths class instead.')
    sc_w = arange(-1, 1./N, 1./N, dtype='d')
    Cs_w = (1-theta_b)*sinh(theta_s*sc_w)/sinh(theta_s)\
          +0.5*theta_b\
          *(tanh(theta_s*(sc_w+0.5))-tanh(0.5*theta_s))/tanh(0.5*theta_s)
    z_w = empty((N,) + h.shape, dtype='d')
    for  k in arange(N):
        z_w[k,:]=(sc_w[k]-Cs_w[k])*hc + Cs_w[k]*h
    return(squeeze(z_w))
