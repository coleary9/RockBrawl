# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremey Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import state
import glob


class Exit(state.State):

    """A state to control saving the game and exiting."""

    def __init__(self, s):
        """
        Constructor.
        """
        self.s = s
        self.name = glob.exitString

    def draw(self):
        """Perform all graphical tasks for this frame."""
        pass

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        pass

    def processKeys(self, keys, dt):
        pass

if __name__ == "__main__":
    main()
