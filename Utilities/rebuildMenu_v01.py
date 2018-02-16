#rebuild function for importing and rebuilding the frogger menu
import FroggerMenu_v01 as fm
reload(fm)

def rebuild(v, *args, **kwargs):
    print "----- REBUILDING FROGGER MENU v%s -----"%v
    fm.Menu()