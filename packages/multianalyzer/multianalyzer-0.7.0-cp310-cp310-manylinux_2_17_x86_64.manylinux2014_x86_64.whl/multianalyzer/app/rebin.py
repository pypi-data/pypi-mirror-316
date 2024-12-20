#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Multianalyzer data rebinning
#             https://github.com/kif/multianalyzer
#
#
#    Copyright (C) 2021-2024 European Synchrotron Radiation Facility, Grenoble, France
#
#    Authors: Jérôme Kieffer <Jerome.Kieffer@ESRF.eu>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  .
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#  .
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

""" id22rebin utility to rebin multi-analyzer data"""
__author__ = "Jérôme Kieffer"
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "13/12/2024"
__status__ = "development"

import os
import sys
import signal
from argparse import ArgumentParser
from queue import Queue
from threading import Event
import logging
logger = logging.getLogger("id22rebin")

import numpy
try:
    import hdf5plugin  # noqa
except ImportError:
    logger.debug("Unable to load hdf5plugin, backtrace:", exc_info=True)

try:
    from rfoo.utils import rconsole
    rconsole.spawn_server()
except ImportError:
    logger.debug("No socket opened for debugging. Please install rfoo")

from .. import __version__
from .._multianalyzer import MultiAnalyzer
try:
    from ..opencl import OclMultiAnalyzer
except ImportError:
    OclMultiAnalyzer = None
from ..file_io import topas_parser, ID22_bliss_parser, save_rebin, all_entries, get_isotime, RoiColReader
from ..timer import Timer

abort = Event()


def sigterm_handler(_signo, _stack_frame):
    sys.stderr.write(f"\nCaught signal {_signo}, quitting !\n")
    sys.stderr.flush()
    abort.set()


signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)
queue = Queue()


def parse():
    name = "id22rebin"
    description = """Rebin ROI-collection into useable powder diffraction patterns.
    """
    epilog = """This software is MIT-licenced and available from https://github.com/kif/multianalyzer"""
    usage = f"{name} [options] ROIcol.h5"

    version = f"{name} version {__version__}"
    parser = ArgumentParser(usage=usage, description=description, epilog=epilog)
    parser.add_argument("-v", "--version", action='version', version=version)

    required = parser.add_argument_group('Required arguments')
    required.add_argument("args", metavar='FILE', type=str, nargs=1,
                        help="HDF5 file with ROI-collection")
    required.add_argument("-p", "--pars", metavar='FILE', type=str,
                          help="`topas` refinement file", required=True)

    optional = parser.add_argument_group('Optional arguments')
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="Output filename (in HDF5)")
    optional.add_argument("--entries", nargs="*", default=list(),
                           help="Entry names (aka scan names) in the input HDF5 file to process. It should be a `fscan`. "
                           "By default, the HDF5 is scanned and ALL `fscan` entries are processed.")
    optional.add_argument("-d", "--debug",
                        action="store_true", dest="debug", default=False,
                        help="switch to verbose/debug mode")
    optional.add_argument("--info",
                        action="store_true", dest="info", default=False,
                        help="switch to info mode, slightly verbose but less than debug")
    optional.add_argument("-w", "--wavelength", type=float, default=None,
                        help="Wavelength of the incident beam (in Å). Default: use the one in `topas` file")
    optional.add_argument("-e", "--energy", type=float, default=None,
                        help="Energy of the incident beam (in keV). Replaces wavelength")
    subparser = parser.add_argument_group('ROI layout in ROI-collection')
    subparser.add_argument("--num-analyzer", dest="num_analyzer", type=int, default=13,
                           help="Number of analyzer crystals (13)")
    subparser.add_argument("--num-row", dest="num_row", type=int, default=512,
                           help="Number of row in ROI-collection (512)")
    subparser.add_argument("--num-col", dest="num_col", type=int, default=1,
                           help="Number of columns in ROI-collection (1)")
    subparser.add_argument("--order", type=int, default=0,
                           help="Order of elements: 0:(col, analyzer, row), 1:(analyzer, col, row), 2: analyzer, row, col")
    subparser = parser.add_argument_group('Rebinning options')
    subparser.add_argument("-s", "--step", type=float, default=None,
                           help="Step size of the 2θ scale. Default: the step size of the scan of the arm")
    subparser.add_argument("-r", "--range", type=float, default=None, nargs=2,
                           help="2θ range in degree. Default: the scan of the arm + analyzer amplitude")
    subparser.add_argument("--phi", type=float, default=75,
                           help="φ_max: Maximum opening angle in azimuthal direction in degrees. Default: 75°")
    subparser.add_argument("--iter", type=int, default=250,
                           help="Maximum number of iteration for the 2theta convergence loop, default:250")
    subparser.add_argument("--startp", type=int, default=0,
                           help="Starting row on the detector, default:0")
    subparser.add_argument("--endp", type=int, default=1024,
                           help="End row on the detector to be considered, default:1024")
    subparser.add_argument("--pixel", type=float, default=75e-3,
                           help="Size of the pixel, default: 75e-3 mm")
    subparser.add_argument("--width", type=float, default=0.0,
                           help="Size of the beam-size on the sample, default from topas file: ~1 mm")
    subparser.add_argument("--delta2theta", type=float, default=0.0,
                           help="Resolution in 2θ, precision expected for 2 ROI being `width` appart on each side of the ROI of interest (disabled by default)")

    subparser = parser.add_argument_group('OpenCL options')
    subparser.add_argument("--device", type=str, default=None,
                           help="Use specified OpenCL device, comma separated (by default: Cython implementation)")

    options = parser.parse_args()

    if options.debug:
        logger.setLevel(logging.DEBUG)
        logging.root.setLevel(level=logging.DEBUG)
    elif options.info:
        logger.setLevel(logging.INFO)
        logging.root.setLevel(level=logging.INFO)
    return options


def rebin_result_generator(filename=None, entries=None, hdf5_data=None, output=None, timer=None, pars=None, device=None, debug=None, energy=None, wavelength=None,
               pixel=None, step=None, range=None, phi=None, width=None, delta2theta=None, iter=None, startp=None, endp=None,
               num_analyzer=None, num_row=512, num_col=1, order=0, info=None):
    if not pars:
        raise ValueError("'pars' parameter is missing")
    if pixel is None:
        pixel = 75e-3
    if phi is None:
        phi = 75
    if width is None:
        width = 0.0
    if delta2theta is None:
        delta2theta = 0.0
    if startp is None:
        startp = 0
    if endp is None:
        endp = 1024
    if iter is None:
        iter = 250
    if timer is None:
        timer = Timer()
    if hdf5_data is None:
        output = output or os.path.splitext(filename)[0] + "_rebin.h5"
        source_name = filename
    else:
        if not output:
            raise ValueError("'output' parameter is missing")
        source_name = "<memory>"
    processed = all_entries(output)

    print(f"Load topas refinement file: {pars}")
    param = topas_parser(pars)
    # Ensure all units are consitent. Here lengths are in milimeters.
    L = param["L1"]
    L2 = param["L2"]

    # Angles are all given in degrees
    center = numpy.array(param["centre"])
    psi = numpy.rad2deg(param["offset"])
    rollx = numpy.rad2deg(param["rollx"])
    rolly = numpy.rad2deg(param["rolly"])

    # tha = hdf5_data["tha"]
    # thd = hdf5_data["thd"]
    tha = numpy.rad2deg(param["manom"])
    thd = numpy.rad2deg(param["mantth"])

    if num_analyzer and num_analyzer != len(center):
        raise RuntimeError(f"*num_analyzer* (value: {num_analyzer}) needs to be consistent with the *topas* param file which contains ({len(center)}) entries")

    # Finally initialize the rebinning engine.
    if device and OclMultiAnalyzer:
        mma = OclMultiAnalyzer(L, L2, pixel, center, tha, thd, psi, rollx, rolly, device=device.split(","))
        print(f"Using device {mma.ctx.devices[0]}")
        block_size = mma.get_max_size()
    else:
        mma = MultiAnalyzer(L, L2, pixel, center, tha, thd, psi, rollx, rolly)
        print("Using Cython+OpenMP")
        block_size = None

    if hdf5_data is None:
        print(f"Read ROI-collection from HDF5 file: {filename}")
        with timer.timeit_read():
            hdf5_data = ID22_bliss_parser(filename, entries=entries, exclude_entries=processed, block_size=block_size)
    print(f"Processing {len(hdf5_data)} entries: {list(hdf5_data)}")

    to_process = []
    to_read = []
    for entry in hdf5_data:
        if entry in processed:
            logger.warning("Skip entry '%s' (already processed)", entry)
            continue
        if "roicol" not in hdf5_data[entry]:
            to_read += hdf5_data[entry]["roicol_lst"]
        to_process.append(entry)
    if to_read:
        logger.debug("Asynchronous read of: \n" + "\n".join(str(i) for i in to_read))
        reader = RoiColReader(to_read, queue, abort, timer.timeit_read)
        reader.start()
    else:
        reader = None

    for entry in to_process:
        arm = hdf5_data[entry]["arm"]
        mon = hdf5_data[entry]["mon"]
        if "roicol" in hdf5_data[entry]:
            roicol = hdf5_data[entry]["roicol"]
            if len(roicol) != len(arm) or len(arm) != len(mon):
                kept_points = min(len(roicol), len(arm), len(mon))
                roicol = roicol[:kept_points]
                arm = arm[:kept_points]
                mon = mon[:kept_points]
                logger.warning(f"Some arrays have different length, was the scan interrupted ? shrinking scan size: {kept_points} !")
        scan = hdf5_data[entry]["scan"]
        dtth = step or scan.step_size
        tth_min = scan.start + psi.min()
        tth_max = scan.stop + psi.max()
        if range:
            if numpy.isfinite(range[0]): 
                tth_min = range[0]
            if numpy.isfinite(range[1]):
                tth_max = range[1]

        print(f"Rebin data from {source_name}::{entry}")
        if "roicol" in hdf5_data[entry]:
            roicol = hdf5_data[entry]["roicol"]
            with timer.timeit_rebin():
                res = mma.integrate(roicol,
                                    arm,
                                    mon,
                                    tth_min, tth_max, dtth=dtth,
                                    iter_max=iter,
                                    roi_min=startp,
                                    roi_max=endp,
                                    phi_max=phi,
                                    num_row=num_row,
                                    num_col=num_col,
                                    columnorder=order,  # // 0: (column=31, channel=13, row=512), 1: (channel=13, column=31, row=512), 2: (channel=13, row=512, column=31)
                                    width=width or param.get("wg", 0.0),
                                    dtthw=delta2theta)
        else:
            desc, data = queue.get()
            if desc.stop < len(arm):
                with timer.timeit_rebin():
                    mma.init_integrate(desc.stop, arm,
                                        mon,
                                        tth_min, tth_max, dtth=dtth,
                                        iter_max=iter,
                                        roi_min=startp,
                                        roi_max=endp,
                                        phi_max=phi,
                                        num_row=num_row,
                                        num_col=num_col,
                                        columnorder=order,  # // 0: (column=31, channel=13, row=512), 1: (channel=13, column=31, row=512), 2: (channel=13, row=512, column=31)
                                        width=width or param.get("wg", 0.0),
                                        dtthw=delta2theta)
                    mma.partial_integate(desc, data)
                while desc.stop < len(arm):
                    desc, data = queue.get()
                    with timer.timeit_rebin():
                        mma.partial_integate(desc, data)
                with timer.timeit_rebin():
                    res = mma.finish_integrate()
            else:
                with timer.timeit_rebin():
                    res = mma.integrate(data,
                                        arm,
                                        mon,
                                        tth_min, tth_max, dtth=dtth,
                                        iter_max=iter,
                                        roi_min=startp,
                                        roi_max=endp,
                                        phi_max=phi,
                                        num_row=num_row,
                                        num_col=num_col,
                                        columnorder=order,  # // 0: (column=31, channel=13, row=512), 1: (channel=13, column=31, row=512), 2: (channel=13, row=512, column=31)
                                        width=width or param.get("wg", 0.0),
                                        dtthw=delta2theta)

        if debug and res.cycles is not None:
            numpy.savez("dump", res.cycles)

        if output:
            print(f"Save to {output}::{entry}")
            with timer.timeit_write():
                save_rebin(output, beamline="id22", name="id22rebin", topas=param, res=res, start_time=timer.start_time, entry=entry)
        yield entry, res


def rebin_file(**kwargs):
    return [entry for entry, _ in rebin_result_generator(**kwargs)]


def main():
    """Entry point of the program, called by the generated warpper"""
    try:
        logging.basicConfig(level=logging.WARNING, force=True)
    except ValueError:
        logging.basicConfig(level=logging.WARNING)
    logging.captureWarnings(True)
    
    options = vars(parse())
    filenames = options.pop("args")
    timer = Timer()
    for filename in filenames:
        rebin_file(filename=filename, timer=timer, **options)
    timer.print()


if __name__ == "__main__":
    main()
