################################################################################
# oops/calibration/rawcounts.py: RawCounts subclass of Calibration
################################################################################

import numpy as np

from polymath                   import Scalar, Pair, Qube
from oops.calibration.flatcalib import FlatCalib

class RawCounts(FlatCalib):
    """A Calibration subclass for an image array of raw photon counts.

    When viewing a source of uniform brightness in a distorted FOV, the raw
    counts tend to be larger where the pixel areas are larger.
    """

    def __init__(self, name, fov, factor, baseline=0.):
        """Constructor for a RawCounts Calibration.

        Input:
            name        the name of the value returned by the calibration, e.g.,
                        "REFLECTIVITY".
            fov         the field of view, used to model the distortion.
                        Alternatively, it can be a 2-D array containing the
                        pixel area corrections.
            factor      a constant scale factor to be applied to every pixel in
                        the field of view.
            baseline    an optional baseline value to subtract from the image
                        before applying the scale factor.
        """

        self.name = name
        self.fov = fov

        factor = Scalar.as_scalar(factor)
        baseline = Scalar.as_scalar(baseline)
        self.has_baseline = np.any(baseline.vals != 0)

        (self.factor, self.baseline) = Qube.broadcast(factor, baseline)
        self.shape = self.factor.shape

    def __getstate__(self):
        return (self.name, self.fov, self.factor, self.baseline)

    def __setstate__(self, state):
        self.__init__(*state)

    #===========================================================================
    def extended_from_dn(self, dn, uv_pair):
        """Extended-source calibrated values for image DN and pixel coordinates.

        Input:
            dn          a Scalar or array of un-calibrated image array values at
                        the given pixel coordinates.
            uv_pair     associated (u,v) pixel coordinates in the image. Note
                        the dn and uv_pair will be casted to the same shape.

        Return:         calibrated values.
        """

        uv_pair = Pair.as_pair(uv_pair)

        if uv_pair.shape and self.shape:
            indx = (Ellipsis,) + len(uv_pair.shape) * (None,)
            factor = self.factor[indx]
            baseline = self.baseline[indx]
        else:
            factor = self.factor
            baseline = self.baseline

        if self.has_baseline:
            dn = dn - baseline

        return dn * factor / self.area_factor(uv_pair)

    #===========================================================================
    def dn_from_extended(self, value, uv_pair):
        """Un-calibrated image DN from extended-source calibrated values.

        Input:
            value       a Scalar or array of calibrated values at the given
                        pixel coordinates.
            uv_pair     associated (u,v) pixel coordinates in the image. Note
                        the dn and uv_pair will be casted to the same shape.

        Return:         an object of the same class and shape as value, but
                        containing the uncalibrated DN values.
        """

        uv_pair = Pair.as_pair(uv_pair)

        if uv_pair.shape and self.shape:
            indx = (Ellipsis,) + len(uv_pair.shape) * (None,)
            factor = self.factor[indx]
            baseline = self.baseline[indx]
        else:
            factor = self.factor
            baseline = self.baseline

        dn = value * self.area_factor(uv_pair) / factor

        if self.has_baseline:
            dn += baseline

        return dn

    #===========================================================================
    def prescale(self, factor, baseline=0., name=''):
        """A version of this Calibration in which image DNs are re-scaled before
        the calibration is applied.

        Input:
            factor      scale factor to apply to DN values.
            baseline    an optional baseline value to subtract from every DN
                        value before applying the new scale factor.
            name        optional new name. If blank, the existing name is
                        preserved.

        Return:         a new object with the given scale factor and baseline
                        incorporated.
        """

        # new_dn = factor * (dn - baseline)
        #
        # value = self.factor * (dn - self.baseline)
        #   = self.factor * (factor * (dn - baseline) - self.baseline)
        #   = (self.factor*factor) * (dn - baseline - self.baseline/factor)
        #
        # new_factor = self.factor * factor
        # new_baseline = baseline + self.baseline/factor

        return RawCounts(name or self.name,
                         fov = self.fov,
                         factor = factor * self.factor,
                         baseline = baseline + self.baseline/factor)

################################################################################
