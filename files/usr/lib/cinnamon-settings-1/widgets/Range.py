#!/usr/bin/env python

# Numerical scale interface.

from functools import partial
import math
from Adjustment import Adjustment
from InputWidget import InputWidget

class Range(InputWidget):
    fallback = 0
    modifier = staticmethod(lambda value:value)
    inverse_modifier = staticmethod(lambda value:value)

    def __init__(self, **descriptor):
        if "modifier" in descriptor:
            self.modifier = staticmethod(descriptor["modifier"])
        if "inverse_modifier" in descriptor:
            self.inverse_modifier = staticmethod(descriptor["inverse_modifier"])

        if descriptor.get("exponential", False):
            self.modifier         = lambda value,m=self.modifier        :math.pow (m(value),2)
            self.inverse_modifier = lambda value,m=self.inverse_modifier:math.sqrt(m(value)  )
        elif descriptor.get("logarithmic", False):
            self.modifier         = lambda value,m=self.modifier        :math.pow(math.e,m(value))
            self.inverse_modifier = lambda value,m=self.inverse_modifier:math.log(       m(value))

        if descriptor.get("inverted", False):
            self.set_inverted(True)

        descriptor["min" ] = self.inverse_modifier(descriptor.get("min" ,   0))
        descriptor["max" ] = self.inverse_modifier(descriptor.get("max" , 100))
        descriptor["step"] = self.inverse_modifier(descriptor.get("step",   1))
        descriptor["page"] = self.inverse_modifier(descriptor.get("page",  10))
        self.set_adjustment(Adjustment(**descriptor))

        print "THE STEP INCREMENT IS "+str(self.get_adjustment().get_step_increment())

        InputWidget.__init__(self, **descriptor)

        if "setting" in descriptor:
            self.changed = self.connect('button-release-event', Range.on_button_release_event)
            self.changed = self.connect("scroll-event", Range.on_scroll_event)

    def on_button_release_event(self, event):
        if event.button == 1:
            Range.on_changed(self)
    def on_scroll_event(self, event):
        found, delta_x, delta_y = event.get_scroll_deltas()
        if found:
            print "was "+str(self.get_value())
            if delta_y < 0:
                print "less "+str(self.get_adjustment().get_step_increment())
                self.set_value(self.get_value()-self.get_adjustment().get_step_increment())
            else:
                print "more "+str(self.get_adjustment().get_step_increment())
                self.set_value(self.get_value()+self.get_adjustment().get_step_increment())
            print "now "+str(self.get_value())
            Range.on_changed(self)
        return True

    def _get_value(self):
        return self.modifier(self.get_value())
    def _set_value(self, value):
        self.set_value(self.inverse_modifier(value))

