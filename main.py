#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sip
# Tell qt to return python string instead of QString
# These are only needed for Python v2 but are harmless for Python v3.

sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore
QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf-8"))
from ggpo.common.controller import Controller
from ggpo.common.settings import Settings
from ggpo.gui.colortheme import ColorTheme
from ggpo.gui.ggpowindow import GGPOWindow
from ggpo.gui.logindialog import LoginDialog
# noinspection PyUnresolvedReferences
import ggpo.resources.ggpo_rc


def main(argv=None):
    app = None

    # create the application if necessary
    if not QtGui.QApplication.instance():
        app = QtGui.QApplication(argv)
        app.setQuitOnLastWindowClosed(True)
        app.setOrganizationName("FightCade")
        QtCore.QCoreApplication.setApplicationName("FightCade")
    ColorTheme.saveDefaultStyle()
    if not Settings.value(Settings.COLORTHEME) or Settings.value(Settings.COLORTHEME)=='fightcade' or Settings.value(Settings.COLORTHEME)=='ggpong':
        ColorTheme.setGNGTheme(True)
    controller = Controller()
    thread = QtCore.QThread()
    controller.moveToThread(thread)
    thread.started.connect(controller.selectLoop)
    thread.start()

    def loggedIn():
        UDP=False
        port=6009
        while True:
            UDP = controller.connectUdp(port)
            port=port-1
            if (UDP==True or port < 6006):
                break
        window = GGPOWindow()
        window.setWindowIcon(QtGui.QIcon(':/assets/icon-128.png'))
        window.setController(controller)
        window.restorePreference()
        controller.sendListChannels()
        window.show()
        window.raise_()
        window.activateWindow()

    logindialog = LoginDialog()
    logindialog.setController(controller)
    logindialog.accepted.connect(loggedIn)
    logindialog.rejected.connect(sys.exit)
    logindialog.exec_()
    logindialog.raise_()
    logindialog.activateWindow()

    return app.exec_()


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
