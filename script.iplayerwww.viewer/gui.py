#
#      Copyright (C) 2014 Tommy Winther
#      http://tommy.winther.nu
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#      Modified for TV Guide Fullscren (2016)
#      by primaeval - primaeval.dev@gmail.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmc
import xbmcgui
import xbmcaddon

DEBUG = False

MODE_IPLAYER = 'IPLAYER'

ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_STOP = 13
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_MENU = 163
ACTION_LAST_PAGE = 160
ACTION_PLAY = 68
ACTION_PLAYER_PLAY = 79
ACTION_PLAYER_PLAYPAUSE = 229

ACTION_MOUSE_WHEEL_UP = 104
ACTION_MOUSE_WHEEL_DOWN = 105
ACTION_MOUSE_MOVE = 107

KEY_NAV_BACK = 92
KEY_CONTEXT_MENU = 117
KEY_HOME = 159
KEY_ESC = 61467

REMOTE_0 = 58
REMOTE_1 = 59
REMOTE_2 = 60
REMOTE_3 = 61
REMOTE_4 = 62
REMOTE_5 = 63
REMOTE_6 = 64
REMOTE_7 = 65
REMOTE_8 = 66
REMOTE_9 = 67

ACTION_JUMP_SMS2 = 142
ACTION_JUMP_SMS3 = 143
ACTION_JUMP_SMS4 = 144
ACTION_JUMP_SMS5 = 145
ACTION_JUMP_SMS6 = 146
ACTION_JUMP_SMS7 = 147
ACTION_JUMP_SMS8 = 148
ACTION_JUMP_SMS9 = 149

ADDON = xbmcaddon.Addon(id='script.iplayerwww.viewer')
SKIN = 'default'

def debug(s):
    if DEBUG: xbmc.log(str(s), xbmc.LOGDEBUG)

class IPlayerViewer(xbmcgui.WindowXML):

    C_IPLAYER = 15000
    C_IPLAYER_POPULAR = 15001
    C_IPLAYER_SEARCH = 15100
    C_IPLAYER_SEARCH_TEXT = 15101
    C_IPLAYER_SEARCH_DISPLAY_TEXT = 15102
    C_IPLAYER_SEARCH_VISIBLE = 15200
    C_IPLAYER_MOUSE_CONTROLS = 15300
    C_IPLAYER_MOUSE_EXIT = 15301

    def __new__(cls):
        return super(IPlayerViewer, cls).__new__(cls, 'script-iplayerwww-main.xml', ADDON.getAddonInfo('path'), SKIN)

    def __init__(self):
        super(IPlayerViewer, self).__init__()
        self.player = xbmc.Player()
        self.mode = MODE_IPLAYER

    def getControl(self, controlId):
        try:
            return super(IPlayerViewer, self).getControl(controlId)
        except Exception as detail:
            xbmc.log("EXCEPTION: (script.tvguide.dvr) IPlayerViewer.getControl %s" % detail, xbmc.LOGERROR)
            if controlId in self.ignoreMissingControlIds:
                return None
            if not self.isClosing:
                self.close()
            return None

    def close(self):
        super(IPlayerViewer, self).close()

    def onInit(self):
        control = self.getControl(self.C_IPLAYER_POPULAR)
        self._hideControl(self.C_IPLAYER_MOUSE_CONTROLS)
        self._showControl(self.C_IPLAYER)
        super(IPlayerViewer, self).setFocus(control)

    def onAction(self, action):
        debug('Mode is: %s' % self.mode)

        if self.mode == MODE_IPLAYER:
            self.onActionIPlayerMode(action)

    def onActionIPlayerMode(self, action):
        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK]:
            if self.player.isPlaying():
                self._hideIPlayer()
            else:
                self.close()

        elif action.getId() == ACTION_MOUSE_MOVE:
            self._showControl(self.C_IPLAYER_MOUSE_CONTROLS)
            return

        # catch the ESC key
        elif action.getId() == ACTION_PREVIOUS_MENU and action.getButtonCode() == KEY_ESC:
            if self.player.isPlaying():
                self._hideIPlayer()
            else:
                self.close()

        elif action.getId() == ACTION_SELECT_ITEM:
            # must be playable item
            if xbmc.getCondVisibility("Control.HasFocus(15100)"):
                control = self.getControl(self.C_IPLAYER_POPULAR)
                super(IPlayerViewer, self).setFocus(control)
                return
            elif self.player.isPlaying():
                self._hideIPlayer()

        else:
            xbmc.log('[script.iplayerwww.viewer] iplayer Unhandled ActionId: ' + str(action.getId()), xbmc.LOGDEBUG)

    def onClick(self, controlId):

        if controlId == self.C_IPLAYER_SEARCH:
            keyboard = xbmc.Keyboard('', 'Search iPlayer')
            keyboard.doModal()
            if keyboard.isConfirmed():
                search_entered = keyboard.getText() .replace(' ', '%20')  # sometimes you need to replace spaces with + or %20
                self.setControlLabel(self.C_IPLAYER_SEARCH_TEXT, '%s' % search_entered)
                self.setControlLabel(self.C_IPLAYER_SEARCH_DISPLAY_TEXT, '[CAPITALIZE]%s[/CAPITALIZE]' % keyboard.getText())
                control = self.getControl(self.C_IPLAYER_SEARCH_VISIBLE)
                control.setVisible(True)
            return
        elif controlId in [self.C_IPLAYER_MOUSE_EXIT]:
            self.close()
            return

    def onFocus(self, controlId):
        pass

    def _hideIPlayer(self):
        if self.player.isPlaying():
            xbmc.executebuiltin("Action(Fullscreen)")
        else:
            self.close()

    def _hideControl(self, *controlIds):
        """
        Visibility is inverted in skin
        """
        for controlId in controlIds:
            control = self.getControl(controlId)
            if control:
                control.setVisible(True)

    def _showControl(self, *controlIds):
        """
        Visibility is inverted in skin
        """
        for controlId in controlIds:
            control = self.getControl(controlId)
            if control:
                control.setVisible(False)

    def setControlImage(self, controlId, image):
        control = self.getControl(controlId)
        if control:
            control.setImage(image.encode('utf-8'))

    def setControlLabel(self, controlId, label):
        control = self.getControl(controlId)
        if control and label:
            control.setLabel(label)

    def setControlText(self, controlId, text):
        control = self.getControl(controlId)
        if control:
            control.setText(text)
