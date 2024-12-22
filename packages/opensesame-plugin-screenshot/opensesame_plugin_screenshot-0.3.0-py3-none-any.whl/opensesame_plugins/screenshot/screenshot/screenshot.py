"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from pathlib import Path
import os
from PIL import ImageGrab


class Screenshot(Item):

    def reset(self):
        self.var.verbose = 'yes'
        self.var.window_stim = 'yes'
        self.var.window_full = 'no'
        self.var.filename_screenshot = ''

    def prepare(self):
        super().prepare()
        self.verbose = self.var.verbose

        if self.var.canvas_backend != 'psycho':
            raise OSException('Screenshot plugin only supports PsychoPy as backend')

        self.experiment_path = Path(os.path.normpath(os.path.dirname(self.var.logfile)))

        if self.var.window_stim == 'yes':
            self.path_stim = self.experiment_path / 'screenshots_stim' / ('subject-' + str(self.var.subject_nr))
            Path(self.path_stim).mkdir(parents=True, exist_ok=True)
        if self.var.window_full == 'yes':
            self.path_full = self.experiment_path / 'screenshots_all' / ('subject-' + str(self.var.subject_nr))
            Path(self.path_full).mkdir(parents=True, exist_ok=True)

    def run(self):
        self.set_item_onset()

        if self.var.window_stim == 'yes':
            fname_stim =  self.path_stim / self.var.filename_screenshot
            image_stim = self.experiment.window._getFrame()
            image_stim.save(fname_stim)
            self._show_message('Screenshot saved to: %s' % fname_stim)
        if self.var.window_full == 'yes':
            fname_full =  self.path_full / self.var.filename_screenshot
            image_full = ImageGrab.grab(all_screens=True)
            image_full.save(fname_full)
            self._show_message('Screenshot saved to: %s' % fname_full)

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtScreenshot(Screenshot, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        Screenshot.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
