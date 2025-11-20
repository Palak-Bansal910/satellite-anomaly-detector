"""This script implements the orbit determination filters in the following sequence:
    - Initialization of filter:
        Gauss initial orbit determination
        Batch least squares
    - Kalman filter - Cowell filter (EKF or UKF), Semianalytical filter (ESKF or USKF)
"""
import os

import numpy as np

from beyond.beyond.dates import Date, timedelta
from beyond.beyond.orbits import Orbit

from orbidet.propagators import ImportedProp
from orbidet.satellite import SatelliteSpecs
from orbidet.observers import GroundStation, get_obs
from orbidet.force import Force,TwoBody,AtmosphericDrag,GravityAcceleration,ExponentialDragDb

from orbidet.IOD.Gauss import Gauss
from orbidet.estimators import LeastSquares,CowellFilter,SemianalyticalFilter
from orbidet.errors import LSnotConverged
from orbidet.metrics.metrics import Metrics
from orbidet.observers.utils import matrix_RSW_to_ECI

def main():
    ################# defining initial conditions and simulation setup #################
    start = Date(2000,4,6,11,0,0)
    step = timedelta(seconds = 5)
    stop = start + timedelta(hours = 6)
    MonteCarlo = 1 #number of Monte Carlo runs to run the simulation

    # frames
    frameECI = "TOD"
    frameECEF = "PEF"

    # Control flags
    apply_noise = True              #Measurement Noise
    LOS = True                     #use LOS condition to validate measurements

    # reference trajectory
    filename = "./orbidet/data/trajectories/GMAT1.csv"
    prop = ImportedProp(start, filename=filename,frame="TOD")
    initialState = prop.orbit

    # setting up Ground Station (GS) observer
    sensors_GS = ["Range", "Azimuth","Elevation","Range Rate"]
    GS1_name = "Lisbon"
    GS1_latlonalt = (38,-10,0)

    # Noise figures
    std_range = (100) / 1000                 #range                              [km]
    std_angles = (0.02) * np.pi/180            #angle measurements                 [rad]
    std_rangerate = (10) / 100 / 1000       #range rate                         [km/s]
    dict_std = {"range":std_range,
                "angles":std_angles,
                "range rate":std_rangerate}

    observer = GroundStation(GS1_name,GS1_latlonalt,sensors_GS,dict_std,frameECEF)
    # print(repr(observer))

    # creating satellite & force model
    sat = SatelliteSpecs("SAT1", #name
                        2,       #CD
                        50,      #mass [kg]
                        2)      #area [m²]
    force = Force(integrationFrame = frameECI, gravityFrame = frameECEF)
    grav = GravityAcceleration(5,0)
    DragHandler = ExponentialDragDb()
    drag = AtmosphericDrag(sat,DragHandler)
    two_body = TwoBody()
    force.addForce(grav)
    # force.addForce(drag)
    force.addForce(two_body)
    # print(force)


    ################# Estimation Setup #################
    InitialOD_LEN = 10 # Number of observations to collect in initialization procedure
    filterName = "USKF" #possible filters: EKF, UKF, ESKF or USKF
    Q_cartesian = np.block([[10**-9*np.eye(3),np.zeros((3,3))],[np.zeros((3,3)),10**-12*np.eye(3)]]) #process noise cov
    Q_equinoctial = np.diag([1e-10,1e-14,1e-14,1e-14,1e-14,1e-12])
    metrics = Metrics(MonteCarlo,RMSE_errors = True,
                                              consistency_tests = True,abs_erros=True,frames = ("ECI","RSW"))


    ################# simulation #################
    run = 1
    while run <= MonteCarlo:
        print('Monte Carlo run %d'%run)

        gen = prop.iter(step=step,stop=stop,start=start)
        # The algorithm should only start when there is LOS (consume observations until LOS)
        if LOS:
            y = None
            while y is None:
                orbit = next(gen)
                y = get_obs(orbit.copy(),observer,dict_std,apply_noise,LOS)

        # setup Initial Orbit Determination (10 observations)
        IOD = []
        while len(IOD) < InitialOD_LEN:
            orbit = next(gen)
            y = get_obs(orbit,observer,dict_std,apply_noise,LOS)
            if y is not None:
                IOD.append([orbit.date,y])

        # run Gauss Initial Orbit Determination algorithm
        gauss = Gauss(IOD[0:3],observer,frameECI)

        # run batch least squares
        t = IOD[3][0]
        orbit = gauss.get_propagated_solution(t,force)
        try:
            LS = LeastSquares(IOD[3:],orbit,observer.R_default,0.1,observer.jacobian_h,observer.h,force)
        except LSnotConverged:
            print("this MC did not converge. Retrying this Monte Carlo run")
            continue
        orbit,P,t = LS.get_propagated_solution(frameECI)

        # create Kalman filter (uncomment desired filter: Cowell or Semianalytical)
        # filter = CowellFilter(filterName,orbit,t,P,Q_cartesian, observer,force,frameECI,"RK45")
        filter = SemianalyticalFilter(filterName,orbit,P,t,Q_equinoctial,
                          observer,force,frameECI,"RK45",timedelta(hours=1),
                          quadrature_order = 20,DFT_lmb_len = 16, DFT_sideral_len=16)

        # continue the simulation until the end of the generator
        for orbit in gen:
            ECI_to_RSW = matrix_RSW_to_ECI(np.array(orbit[0:3]),np.array(orbit[3:])).T
            t = (orbit.date - start).total_seconds()

            y = get_obs(orbit.copy(),observer,dict_std,apply_noise,LOS) #get reference observation and corrupt it with noise
            invS,v = filter.filtering_cycle(orbit.date,y,observer)
            metrics.append_estimation(t,np.array(orbit),filter.x_osc.copy(form="cartesian"),
                    R_ECI_to_RSW=ECI_to_RSW,P = filter.P_osc,Sinv = invS,obs_err = v)
            print(orbit.date)



        run += 1

    # process estimation metrics
    path = "./results/"
    save = False
    if save and not os.path.exists(path):
        os.makedirs(path)

    metrics.process_results(path+"_osc_"+filterName,save=save)
    metrics.plot_results(len(sensors_GS),6,n=-1,side_consistency="one-sided",prob_consistency=0.95,
                            filter_name = filterName)


if __name__ == "__main__":
    main()

"""This script creates measurement records of ground station passes
"""

import numpy as np

from beyond.beyond.dates import Date, timedelta
from beyond.beyond.orbits import Orbit

from orbidet.propagators import ImportedProp
from orbidet.satellite import SatelliteSpecs
from orbidet.observers import GroundStation, get_obs



def main():
    # defining initial conditions and setting propagator
    start = Date(2010,3,1,18,00,0)
    filename = "./orbidet/data/trajectories/GMAT1.csv"
    prop = ImportedProp(start, filename=filename,frame="TOD")
    initialState = prop.orbit
    # print(repr(initialState))

    # getting generator
    step = timedelta(seconds = 60)
    stop = start + timedelta(hours = 24)
    gen = prop.iter(step=step,stop=stop,start=start)

    # setting up Ground Station (GS) observer
    sensors_GS = ["Range", "Azimuth","Elevation","Range Rate"]
    GS1_name = "Lisbon"
    GS1_latlonalt = (38,-10,0)

    # Noise figures
    std_range = (100) / 1000                 #range                              [km]
    std_angles = (0.02) * np.pi/180            #angle measurements                 [rad]
    std_rangerate = (10) / 100 / 1000       #range rate                         [km/s]
    dict_std = {"range":std_range,
                "angles":std_angles,
                "range rate":std_rangerate}

    ECEF_frame = "PEF" # the topocentric frame is defined with respect to ECEF_frame
    observer = GroundStation(GS1_name,GS1_latlonalt,sensors_GS,dict_std,ECEF_frame)
    # print(repr(observer))


    # generate orbit
    for orbit in gen:
        y = get_obs(orbit.copy(),observer,dict_std,apply_noise=True,do_LOS=True)
        if y is not None:
            print(orbit.date, y)











if __name__ == "__main__":
    main()
"""File demonstrating the use of propagators (examples)
"""
import numpy as np

from beyond.beyond.dates import Date, timedelta
from beyond.beyond.orbits import Orbit

from orbidet.propagators import ImportedProp, Cowell, Semianalytical
from orbidet.force import Force,TwoBody,AtmosphericDrag,GravityAcceleration,ExponentialDragDb
from orbidet.satellite import SatelliteSpecs
from orbidet.metrics.plot_utils import *


forms = {'cartesian':['x','y','z','vx','vy','vz'],
         'keplerian':["a", "e", "i", "RAAN", "w", "TA"],
         'keplerian_mean':["a", "e", "i", "RAAN", "w", "M"],
         "equinoctial_mean":["a","h","k","p","q","lmb"]
         }


def ImportedPropExample():
    # defining initial conditions and setting propagator
    start = Date(2010,3,1,18,00,0)
    filename = "./orbidet/data/trajectories/GMAT1.csv"
    prop = ImportedProp(start, filename=filename)
    initialState = prop.orbit
    # print(repr(initialState))

    # getting generator
    step = timedelta(seconds = 5)
    stop = start + timedelta(hours = 1)
    gen = prop.iter(step=step,stop=stop,start=start)

    # generate orbit
    for orbit in gen:
        print(orbit.date, orbit)


def CowellExample():
    # defining initial conditions & frames
    start = Date(2010,3,1,18,00,0)
    step = timedelta(seconds = 5)
    stop = start + timedelta(hours = 1)
    integrationFrame = "TOD"
    gravityFrame = "PEF"
    initialOrbit = Orbit(np.array([6542.76,2381.36,-0.000102,0.3928,-1.0793,7.592]),
                        start,"cartesian",integrationFrame,None)

    # creating satellite
    sat = SatelliteSpecs("SAT1", #name
                        2,       #CD
                        50,      #mass [kg]
                        2)      #area [m²]

    # creating force model
    force = Force(integrationFrame = integrationFrame, gravityFrame = gravityFrame)
    grav = GravityAcceleration(5,5)
    DragHandler = ExponentialDragDb()
    drag = AtmosphericDrag(sat,DragHandler)
    two_body = TwoBody()
    force.addForce(grav)
    force.addForce(drag)
    force.addForce(two_body)
    # print(force)

    # creating propagator & generator
    prop = Cowell(step,force,method="RK45",frame=initialOrbit.frame)
    initialOrbit.propagator = prop
    gen = initialOrbit.iter(stop=stop,step=step)

    # generate orbit
    for orbit in gen:
        print(orbit.date,orbit)




def SemianalyticalExample():
    # defining initial conditions & frames
    start = Date(2010,3,1,18,00,0)
    output_step = timedelta(seconds = 60)
    propagation_step = timedelta(hours = 1)
    stop = start + timedelta(hours = 5)
    integrationFrame = "TOD"
    gravityFrame = "PEF"
    initialOrbit = Orbit(np.array([6542.76,2381.36,-0.000102,0.3928,-1.0793,7.592]),
                        start,"cartesian",integrationFrame,None)

    # creating satellite
    sat = SatelliteSpecs("SAT1", #name
                        2,       #CD
                        50,      #mass [kg]
                        2)      #area [m²]

    # creating force model
    force = Force(integrationFrame = integrationFrame, gravityFrame = gravityFrame)
    grav = GravityAcceleration(5,5)
    DragHandler = ExponentialDragDb()
    drag = AtmosphericDrag(sat,DragHandler)
    two_body = TwoBody()
    force.addForce(grav)
    # force.addForce(drag)
    force.addForce(two_body)
    # print(force)

    # creating propagator & generator
    prop = Semianalytical(propagation_step,force,method="RK45",frame=initialOrbit.frame,
                        quadrature_order = 20, DFT_lmb_len = 32, DFT_sideral_len=32,
                        outputs=("mean","osculating"))
    initialOrbit.propagator = prop
    initialOrbit.state = "mean"
    gen = initialOrbit.iter(stop=stop,step=output_step)


    ephm_osc = []
    ephm_mean = []
    output_form = "equinoctial_mean"
    # generate orbit
    for mean,osc in gen:
        ephm_osc.append(osc.copy(form=output_form))
        ephm_mean.append(mean.copy(form=output_form))

        print(mean.date)


    # Time array
    dt = (ephm_osc[1].date - ephm_osc[0].date).total_seconds()
    delta_t = (ephm_osc[-1].date - ephm_osc[0].date).total_seconds()
    t = [t_i for t_i in range(0,round(delta_t+dt),round(dt))]
    xlabel = 'Time [s]'


    for ephm,label in zip([ephm_osc,ephm_mean],["osc","mean"]):
        x0 = [x[0] for x in ephm]
        x1 = [x[1] for x in ephm]
        x2 = [x[2] for x in ephm]
        x3 = [x[3] for x in ephm]
        x4 = [x[4] for x in ephm]
        x5 = [x[5] for x in ephm]
        plot_graphs(x0,t,forms[output_form][0],"",xlabel,i=0,label=label,show_label=True)
        plot_graphs(x1,t,forms[output_form][1],"",xlabel,i=1,label=label,show_label=True)
        plot_graphs(x2,t,forms[output_form][2],"",xlabel,i=2,label=label,show_label=True)
        plot_graphs(x3,t,forms[output_form][3],"",xlabel,i=3,label=label,show_label=True)
        plot_graphs(x4,t,forms[output_form][4],"",xlabel,i=4,label=label,show_label=True)
        plot_graphs(x5,t,forms[output_form][5],"",xlabel,i=5,label=label,show_label=True)
    show_plots(True)




def main():
    SemianalyticalExample()

if __name__ == "__main__":
    main()
