# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


class Metro(object):

    """A metronome object for abstracting time flow."""

    def __init__(self, redTime=0, greenTime=0,
                 delay=0, initState=False):
        """Constructor."""
        # How many millis the metro will be in a "False" state.
        self.redTime = redTime
        # How many millis the metro will be in a "True" state.
        self.greenTime = greenTime
        self.time = -delay
        self.state = initState
        self.assignTickTime()

    def tick(self, dt):
        """Updates by a millisecond argument and returns its current state."""
        self.time += dt
        if self.time > self.tickTime:
            self.time -= self.tickTime
            self.state = not self.state
            self.assignTickTime()
        return self.state

    def assignTickTime(self):
        """Assigns the current state length."""
        if self.state:
            self.tickTime = self.greenTime
        else:
            self.tickTime = self.redTime

    def zero(self):
        """Resets the time to 0 seconds."""
        self.time = 0

    def getPercentGreen(self):
        """Returns the time divided by the greenTime."""
        return float(self.time) / self.greenTime


class CoolDownMetro(object):

    """Handles a timer that fires, then can't fire for awhile."""

    def __init__(self, coolDown):
        """Constructor."""
        self.metro = Metro(0, coolDown)
        self.hasFired = False

    def tick(self, dt):
        """
        Updates the internal metro by the passed milliseconds and sets the
        state.
        """
        if self.hasFired:
            self.hasFired = self.metro.tick(dt)
        if not self.hasFired and not self.metro.time == 0:
            self.metro.zero()
        return self.hasFired

    def fire(self):
        """Goes to the fired state."""
        self.hasFired = True

    def fizzle(self):
        """Goes back to the unfired state prematurely."""
        self.hasFired = False

    def getState(self):
        return self.hasFired

    def getPercent(self):
        """
        If in the fired state, returns what fraction of the state we've
        passed. Otherwise returns 0.
        """
        if self.hasFired:
            return self.metro.getPercentGreen()
        else:
            return 0

    def getTime(self):
        return self.metro.time
