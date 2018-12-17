import os

# Workarround for nvidia propietary drivers

import ctypes
import ctypes.util

ctypes.CDLL(ctypes.util.find_library("GL"), mode=ctypes.RTLD_GLOBAL)

# end of Workarround

# from hal import component, HAL_BIT, HAL_IN

from qtpy.QtCore import Signal, Slot, QUrl
from qtpy.QtQuickWidgets import QQuickWidget

from qtpyvcp.plugins import getPlugin

STATUS = getPlugin('status')

WIDGET_PATH = os.path.dirname(os.path.abspath(__file__))


# def _initComp():
#     halcomp = component("atc_widget")
#     halcomp.newpin("fwd", HAL_BIT, HAL_IN)
#     halcomp.newpin("rev", HAL_BIT, HAL_IN)
#     halcomp.ready()
#
#     return halcomp


class DynATC(QQuickWidget):

    def __init__(self, parent=None):
        super(DynATC, self).__init__(parent)

        if not parent:
            return

        self.engine().rootContext().setContextProperty("atc_spiner", self)
        url = QUrl.fromLocalFile(os.path.join(WIDGET_PATH, "atc.qml"))
        self.setSource(url)

        # try:
        #     self.halcomp = _initComp()
        # except Exception as e:
        #     self.halcomp = None

        self.fwd_pin = 0
        self.rev_pin = 0

        self.prev_fwd_pin = 0
        self.prev_rev_pin = 0

        self.atc_position = 0

        # STATUS.tool_in_spindle.onValueChanged(self.on_tool_in_spindle)
        # STATUS.pocket_prepped.onValueChanged(self.on_pocket_prepped)

    # def on_pocket_prepped(self, pocket_num):
    #     print "Pocket Prepared: ", pocket_num
    #
    # def on_tool_in_spindle(self, tool_num):
    #     print "Tool in Spindle: ", tool_num

    rotateFwdSig = Signal(int, arguments=['rotate_forward'])
    @Slot()
    def rotate_forward(self):
        self.rotateFwdSig.emit(self.atc_position)
        self.atc_position += 1

    rotateRevSig = Signal(int, arguments=['rotate_reverse'])
    @Slot()
    def rotate_reverse(self):
        self.rotateRevSig.emit(self.atc_position)
        self.atc_position -= 1

    # pinSig = Signal(arguments=['get_pins'])
    # @Slot()
    # def get_pins(self):
    #     pass
    #
    #     if self.halcomp is None:
    #        return
    #
    #     self.fwd_pin = self.halcomp["fwd"]
    #     if self.fwd_pin != self.prev_fwd_pin:
    #         self.prev_fwd_pin = self.fwd_pin
    #         self.rotateFwdSig.emit(self.atc_position)
    #         self.atc_position += 1
    #
    #     self.rev_pin = self.halcomp["rev"]
    #     if self.rev_pin != self.prev_rev_pin:
    #         self.prev_rev_pin = self.rev_pin
    #         self.rotateRevSig.emit(self.atc_position)
    #         self.atc_position += 1
