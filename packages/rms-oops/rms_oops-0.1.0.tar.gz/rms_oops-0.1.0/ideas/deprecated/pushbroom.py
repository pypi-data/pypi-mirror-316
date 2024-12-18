################################################################################
# oops/observation/pushbroom.py: Subclass Pushbroom of class Observation
################################################################################

import numpy as np
from polymath import Scalar, Pair, Vector

from oops.observation          import Observation
from oops.observation.snapshot import Snapshot
from oops.cadence              import Cadence
from oops.cadence.metronome    import Metronome
from oops.frame                import Frame
from oops.path                 import Path

from oops.observation.timedimage import TimedImage

class Pushbroom(TimedImage):
    """A subclass of Observation consisting of a 2-D image generated by sweeping
    a 1-D strip of sensors across a field of view.

    The FOV object is assumed to define the entire 2-D field of view, even if
    the reality is that a 1-D array was swept in a (roughly) perpendicular
    direction. The virtual array of data is assumed to have a t-dimension of 1,
    while the number of time steps is equal to the number of samples in the u
    or v direction, depending on the direction of sweep. In effect, then, the
    virtual array samples a diagonal ramp through the (u,v,t) cube.
    """

    pass

#     INVENTORY_IMPLEMENTED = True
#
#     # Relates these axes to Snapshot axes
#     AXIS_REPLACEMENTS = {
#         'ut':  'u',
#         'vt':  'v',
#     }
#
#     #===========================================================================
#     def __init__(self, axes, cadence, fov, path, frame, **subfields):
#         """Constructor for a Pushbroom observation.
#
#         Input:
#             axes        a list or tuple of strings, with one value for each axis
#                         in the associated data array. A value of 'u' or 'ut'
#                         should appear at the location of the array's u-axis;
#                         'vt' or 'v' should appear at the location of the array's
#                         v-axis. The 't' suffix is used for the one of these axes
#                         that is emulated by time-sampling the slit.
#
#             cadence     a 1-D Cadence object defining the start time and
#                         duration of each consecutive position in the sweep of
#                         the pushbroom. Alternatively, a tuple or dictionary
#                         providing input arguments to the constructor
#                         Metronome.for_array1d() (excluding the number of
#                         lines, which is defined by the FOV)
#                             (tstart, texp, interstep_delay)
#
#             fov         a FOV (field-of-view) object, which describes the field
#                         of view including any spatial distortion. It maps
#                         between spatial coordinates (u,v) and instrument
#                         coordinates (x,y).
#
#             path        the path waypoint co-located with the instrument.
#
#             frame       the wayframe of a coordinate frame fixed to the optics
#                         of the instrument. This frame should have its Z-axis
#                         pointing outward near the center of the line of sight,
#                         with the X-axis pointing rightward and the y-axis
#                         pointing downward.
#
#             subfields   a dictionary containing all of the optional attributes.
#                         Additional subfields may be included as needed.
#         """
#
#         # Basic properties
#         self.path = Path.as_waypoint(path)
#         self.frame = Frame.as_wayframe(frame)
#
#         # FOV
#         self.fov = fov
#         self.uv_shape = tuple(self.fov.uv_shape.vals)
#
#         # Axes
#         self.axes = list(axes)
#         assert (('u' in self.axes and 'vt' in self.axes) or
#                 ('v' in self.axes and 'ut' in self.axes))
#
#         if 'ut' in self.axes:
#             self.u_axis = self.axes.index('ut')
#             self.v_axis = self.axes.index('v')
#             self.t_axis = self.u_axis
#             self._cross_slit_uv_index = 0
#             self._along_slit_uv_index = 1
#         else:
#             self.u_axis = self.axes.index('u')
#             self.v_axis = self.axes.index('vt')
#             self.t_axis = self.v_axis
#             self._cross_slit_uv_index = 1
#             self._along_slit_uv_index = 0
#
#         self.swap_uv = (self.u_axis > self.v_axis)
#
#         # Shape / Size
#         self.shape = len(axes) * [0]
#         self.shape[self.u_axis] = self.uv_shape[0]
#         self.shape[self.v_axis] = self.uv_shape[1]
#
#         lines = self.uv_shape[self._cross_slit_uv_index]
#         samples = self.uv_shape[self._along_slit_uv_index]
#         self._cross_slit_len = lines
#         self._along_slit_len = samples
#
#         slit_uv_shape = [1,1]
#         slit_uv_shape[self._along_slit_uv_index] = samples
#         self._slit_uv_shape = Pair(slit_uv_shape)
#
#         # Cadence
#         if isinstance(cadence, (tuple,list)):
#             self.cadence = Metronome.for_array1d(lines, *cadence)
#         elif isinstance(cadence, dict):
#             self.cadence = Metronome.for_array1d(lines, **cadence)
#         elif isinstance(cadence, Cadence):
#             self.cadence = cadence
#             assert self.cadence.shape == (lines,)
#         else:
#             raise TypeError('Invalid cadence class: ' + type(cadence).__name__)
#
#         # Timing
#         self.time = self.cadence.time
#         self.midtime = self.cadence.midtime
#
#         # Optional subfields
#         self.subfields = {}
#         for key in subfields.keys():
#             self.insert_subfield(key, subfields[key])
#
#         # Snapshot class proxy
#         snapshot_axes = [Pushbroom.AXIS_REPLACEMENTS.get(axis, axis)
#                          for axis in axes]
#         snapshot_tstart = self.cadence.time[0]
#         snapshot_texp = self.cadence.time[1] - self.cadence.time[0]
#
#         self.snapshot = Snapshot(snapshot_axes, snapshot_tstart, snapshot_texp,
#                                  self.fov, self.path, self.frame, **subfields)
#
#     def __getstate__(self):
#         return (self.axes, self.cadence, self.fov, self.path, self.frame,
#                 self.subfields)
#
#     def __setstate__(self, state):
#         self.__init__(*state[:-1], **state[-1])
#
#     #===========================================================================
#     def uvt(self, indices, remask=False, derivs=True):
#         """Coordinates (u,v) and time t for indices into the data array.
#
#         This method supports non-integer index values.
#
#         Input:
#             indices     a Scalar or Vector of array indices.
#             remask      True to mask values outside the field of view.
#             derivs      True to include derivatives in the returned values.
#
#         Return:         (uv, time)
#             uv          a Pair defining the values of (u,v) within the FOV that
#                         are associated with the array indices.
#             time        a Scalar defining the time in seconds TDB associated
#                         with the array indices.
#         """
#
#         indices = Vector.as_vector(indices, recursive=derivs)
#         uv = indices.to_pair((self.u_axis, self.v_axis))
#
#         # Mask based on (u,v) if necessary
#         if remask:
#             mask = ((uv.vals[...,0] < 0) | (uv.vals[...,0] > self.uv_shape[0]) |
#                     (uv.vals[...,1] < 0) | (uv.vals[...,1] > self.uv_shape[1]))
#             if np.any(mask):
#                 uv = uv.remask_or(mask)
#
#         # Get the time, inheriting the mask of uv
#         tstep = uv.to_scalar(self._cross_slit_uv_index)
#         time = self.cadence.time_at_tstep(tstep, remask=False, derivs=derivs)
#
#         return (uv, time)
#
#     #===========================================================================
#     def uvt_range(self, indices, remask=False):
#         """Ranges of (u,v) spatial coordinates and time for integer array
#         indices.
#
#         Input:
#             indices     a Scalar or Vector of array indices.
#             remask      True to mask values outside the field of view.
#
#         Return:         (uv_min, uv_max, time_min, time_max)
#             uv_min      a Pair defining the minimum values of FOV (u,v)
#                         associated the pixel.
#             uv_max      a Pair defining the maximum values of FOV (u,v)
#                         associated the pixel.
#             time_min    a Scalar defining the minimum time associated with the
#                         array indices. It is given in seconds TDB.
#             time_max    a Scalar defining the maximum time value.
#         """
#
#         # Interpret the (u,v) range
#         indices = Vector.as_vector(indices, recursive=False)
#         uv = indices.to_pair((self.u_axis, self.v_axis))
#         uv_min = uv.int(top=self.uv_shape, remask=remask)
#
#         # Intepret the time range, inheriting the mask of uv_min
#         tstep = uv_min.to_scalar(self._cross_slit_uv_index)
#         (time_min,
#          time_max) = self.cadence.time_range_at_tstep(tstep, remask=False)
#
#         return (uv_min, uv_min + Pair.INT11, time_min, time_max)
#
#     #===========================================================================
#     def time_range_at_uv(self, uv_pair, remask=False):
#         """The start and stop integration times for the spatial pixel (u,v).
#
#         Input:
#             uv_pair     a Pair of spatial (u,v) data array coordinates,
#                         truncated to integers if necessary.
#             remask      True to mask values outside the field of view.
#
#         Return:         a tuple containing Scalars of the start time and stop
#                         time of each (u,v) pair, as seconds TDB.
#         """
#
#         return self.time_range_at_uv_1d(uv_pair, remask=remask)
#         uv_pair = Pair.as_pair(uv_pair, recursive=False)
#         tstep = uv_pair.to_scalar(self._cross_slit_uv_index)
#         return self.cadence.time_range_at_tstep(tstep, remask=remask)
#
#     #===========================================================================
#     def uv_range_at_time(self, time, remask=False):
#         """The (u,v) range of spatial pixels active at the specified time.
#
#         Input:
#             time        a Scalar of time values in seconds TDB.
#             remask      True to mask values outside the time limits.
#
#         Return:         (uv_min, uv_max)
#             uv_min      the lower (u,v) corner Pair of the area observed at the
#                         specified time.
#             uv_max      the upper (u,v) corner Pair of the area observed at the
#                         specified time.
#         """
#
#         return Observation.uv_range_at_time_1d(self, time, self._slit_uv_shape,
#                                                axis=self._cross_slit_uv_index,
#                                                remask=remask)
#
#     #===========================================================================
#     def time_shift(self, dtime):
#         """A copy of the observation object with a time-shift.
#
#         Input:
#             dtime       the time offset to apply to the observation, in units of
#                         seconds. A positive value shifts the observation later.
#
#         Return:         a (shallow) copy of the object with a new time.
#         """
#
#         obs = Pushbroom(self.axes, self.cadence.time_shift(dtime),
#                         self.fov, self.path, self.frame)
#
#         for key in self.subfields.keys():
#             obs.insert_subfield(key, self.subfields[key])
#
#         return obs
#
#     #===========================================================================
#     def inventory(self, *args, **kwargs):
#         """Info about the bodies that appear unobscured inside the FOV. See
#         Snapshot.inventory() for details.
#
#         WARNING: Not properly updated for class Pushbroom. Use at your own risk.
#         This operates by returning every body that would have been inside the
#         FOV of this observation if it were instead a Snapshot, evaluated at the
#         given tfrac.
#         """
#
#         return self.snapshot.inventory(*args, **kwargs)

################################################################################
# UNIT TESTS
################################################################################

import unittest

class Test_Pushbroom(unittest.TestCase):

    def runTest(self):

        from oops.cadence.metronome import Metronome
        from oops.fov.flatfov import FlatFOV

        ########################################
        # Overall shape (10,20)
        # Time is second axis; time = v * 10.
        ########################################

        flatfov = FlatFOV((0.001,0.001), (10,20))
        cadence = Metronome(tstart=0., tstride=10., texp=10., steps=20)
        obs = Pushbroom(axes=('u','vt'), cadence=cadence, fov=flatfov,
                                         path='SSB', frame='J2000')

        indices = Vector([(0,0),(0,10),(0,20),(10,0),(10,10),(10,20),(10,21)])
        tstep = indices.to_scalar(1)

        indices_ = indices.copy()   # clipped at top
        indices_.vals[:,0][indices_.vals[:,0] == 10] -= 1
        indices_.vals[:,1][indices_.vals[:,1] == 20] -= 1

        # uvt() with remask == False
        (uv, time) = obs.uvt(indices)

        self.assertFalse(np.any(uv.mask))
        self.assertFalse(np.any(time.mask))
        self.assertEqual(time, cadence.time_at_tstep(tstep))
        self.assertEqual(uv, Pair.as_pair(indices))

        # uvt() with remask == True
        (uv, time) = obs.uvt(indices, remask=True)

        self.assertTrue(np.all(uv.mask == np.array(6*[False] + [True])))
        self.assertTrue(np.all(time.mask == uv.mask))
        self.assertEqual(time[:6], cadence.tstride * indices.to_scalar(1)[:6])
        self.assertEqual(uv[:6], Pair.as_pair(indices)[:6])

        # uvt_range() with remask == False
        (uv_min, uv_max, time_min, time_max) = obs.uvt_range(indices)

        self.assertFalse(np.any(uv_min.mask))
        self.assertFalse(np.any(uv_max.mask))
        self.assertFalse(np.any(time_min.mask))
        self.assertFalse(np.any(time_max.mask))

        self.assertEqual(uv_min, Pair.as_pair(indices_))
        self.assertEqual(uv_max, Pair.as_pair(indices_) + (1,1))
        self.assertEqual(time_min, cadence.time_range_at_tstep(tstep)[0])
        self.assertEqual(time_max, time_min + cadence.texp)

        # uvt_range() with remask == False, new indices
        non_ints = indices + (0.2,0.9)
        (uv_min, uv_max, time_min, time_max) = obs.uvt_range(non_ints)

        self.assertFalse(np.any(uv_min.mask))
        self.assertFalse(np.any(uv_max.mask))
        self.assertFalse(np.any(time_min.mask))
        self.assertFalse(np.any(time_max.mask))

        self.assertEqual(uv_min, Pair.as_pair(indices))
        self.assertEqual(uv_max, Pair.as_pair(indices) + (1,1))
        self.assertEqual(time_min, cadence.time_range_at_tstep(tstep)[0])
        self.assertEqual(time_max, time_min + cadence.texp)

        # uvt_range() with remask == True, new indices
        non_ints = indices + (0.2,0.9)
        (uv_min, uv_max, time_min, time_max) = obs.uvt_range(non_ints,
                                                             remask=True)

        self.assertTrue(np.all(uv_min.mask == np.array(2*[False] + 5*[True])))
        self.assertTrue(np.all(uv_max.mask == uv_min.mask))
        self.assertTrue(np.all(time_min.mask == uv_min.mask))
        self.assertTrue(np.all(time_max.mask == uv_min.mask))

        self.assertEqual(uv_min[:2], Pair.as_pair(indices)[:2])
        self.assertEqual(uv_max[:2], Pair.as_pair(indices)[:2] + (1,1))
        self.assertEqual(time_min[:2], cadence.time_range_at_tstep(tstep)[0][:2])
        self.assertEqual(time_max[:2], time_min[:2] + cadence.texp)

        # time_range_at_uv() with remask == False
        uv = Pair([(0,0),(0,20),(10,0),(10,20),(10,21)])
        tstep = uv.to_scalar(1)

        uv_ = uv.copy()
        uv_.vals[:,0][uv_.vals[:,0] == 10] -= 1
        uv_.vals[:,1][uv_.vals[:,1] == 20] -= 1

        (time0, time1) = obs.time_range_at_uv(uv)
        self.assertEqual(time0, cadence.time_range_at_tstep(tstep)[0])
        self.assertEqual(time1, time0 + cadence.texp)

        # time_range_at_uv() with remask == True
        (time0, time1) = obs.time_range_at_uv(uv, remask=True)
        self.assertTrue(np.all(time0.mask == 4*[False] + [True]))
        self.assertTrue(np.all(time1.mask == 4*[False] + [True]))
        self.assertEqual(time0[:4], cadence.tstride * uv_.to_scalar(1)[:4])
        self.assertEqual(time1[:4], time0[:4] + cadence.texp)

        ########################################
        # Alternative axis order ('ut','v')
        # Overall shape (10,20)
        # Time is first axis; time = v * 10.
        ########################################

        cadence = Metronome(tstart=0., tstride=10., texp=10., steps=10)
        obs = Pushbroom(axes=('ut','v'), cadence=cadence, fov=flatfov,
                                         path='SSB', frame='J2000')

        indices = Vector([(0,0),(0,10),(0,20),(10,0),(10,10),(10,20),(10,21)])
        indices_ = indices.copy()
        indices_.vals[:,0][indices_.vals[:,0] == 10] -= 1
        indices_.vals[:,1][indices_.vals[:,1] == 20] -= 1

        (uv, time) = obs.uvt(indices)

        uv_ = uv.copy()
        uv_.vals[:,0][uv_.vals[:,0] == 10] -= 1
        uv_.vals[:,1][uv_.vals[:,1] == 20] -= 1

        self.assertEqual(uv, Pair.as_pair(indices))
        self.assertEqual(time, cadence.tstride * indices.to_scalar(0))

        (uv_min, uv_max, time_min, time_max) = obs.uvt_range(indices)

        self.assertEqual(uv_min, Pair.as_pair(indices_))
        self.assertEqual(uv_max, Pair.as_pair(indices_) + (1,1))
        self.assertEqual(time_min, cadence.tstride * indices_.to_scalar(0))
        self.assertEqual(time_max, time_min + cadence.texp)

        (time0, time1) = obs.time_range_at_uv(indices)

        self.assertEqual(time0, cadence.tstride * uv_.to_scalar(0))
        self.assertEqual(time1, time0 + cadence.texp)

        ########################################################
        # Alternative texp for discontinuous time index
        # Overall shape (10,20)
        # Time is first axis; time = [0-8, 10-18, ..., 90-98]
        ########################################################

        cadence = Metronome(tstart=0., tstride=10., texp=8., steps=10)
        obs = Pushbroom(axes=('ut','v'), cadence=cadence, fov=flatfov,
                                         path='SSB', frame='J2000')

        self.assertEqual(obs.time[1], 98.)

        self.assertEqual(obs.uvt((0,0))[1],  0.)
        self.assertEqual(obs.uvt((5,0))[1], 50.)
        self.assertEqual(obs.uvt((5,5))[1], 50.)

        eps = 1.e-14
        delta = 1.e-13
        self.assertTrue(abs(obs.uvt((6      ,0))[1] - 60.) < delta)
        self.assertTrue(abs(obs.uvt((6.25   ,0))[1] - 62.) < delta)
        self.assertTrue(abs(obs.uvt((6.5    ,0))[1] - 64.) < delta)
        self.assertTrue(abs(obs.uvt((6.75   ,0))[1] - 66.) < delta)
        self.assertTrue(abs(obs.uvt((7 - eps,0))[1] - 68.) < delta)
        self.assertTrue(abs(obs.uvt((7.     ,0))[1] - 70.) < delta)

        self.assertEqual(obs.uvt((0,0))[0], (0.,0.))
        self.assertEqual(obs.uvt((5,0))[0], (5.,0.))
        self.assertEqual(obs.uvt((5,5))[0], (5.,5.))

        self.assertTrue(abs(obs.uvt((6      ,0))[0] - (6.0,0.)) < delta)
        self.assertTrue(abs(obs.uvt((6.2    ,1))[0] - (6.2,1.)) < delta)
        self.assertTrue(abs(obs.uvt((6.4    ,2))[0] - (6.4,2.)) < delta)
        self.assertTrue(abs(obs.uvt((6.6    ,3))[0] - (6.6,3.)) < delta)
        self.assertTrue(abs(obs.uvt((6.8    ,4))[0] - (6.8,4.)) < delta)
        self.assertTrue(abs(obs.uvt((7 - eps,5))[0] - (7.0,5.)) < delta)
        self.assertTrue(abs(obs.uvt((7.     ,6))[0] - (7.0,6.)) < delta)

        # Test the upper edge
        uv_list = []
        uvt_list = []
        for i,u in enumerate([10.-eps, 10., 10.+eps]):
          for j,v in enumerate([20.-eps, 20., 20.+eps]):
            uv_list.append((u,v))

            uvt = obs.uvt((u,v), remask=True)
            uvt_list.append(uvt)
            if (i < 2) and (j < 2):
                self.assertEqual(uvt[0], (u,v))
            else:
                self.assertEqual(uvt[0], Pair.MASKED)

            if (i < 2) and (j < 2):
                self.assertTrue((uvt[1] - (10. * u - 2.)).abs() < delta)
            else:
                self.assertEqual(uvt[1], Scalar.MASKED)

        # Try all at once
        uvt = obs.uvt(uv_list, remask=True)
        self.assertEqual(uvt[0], [a[0] for a in uvt_list])
        self.assertEqual(uvt[1], [a[1] for a in uvt_list])

########################################
if __name__ == '__main__':
    unittest.main(verbosity=2)
################################################################################
