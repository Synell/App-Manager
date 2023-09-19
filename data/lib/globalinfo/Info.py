#----------------------------------------------------------------------

    # Libraries
from ..qtUtils import QSaveData, QUtilsColor
import os
#----------------------------------------------------------------------

    # Class
class Info:
    def __new__(cls) -> None:
        return None

    build: str = '07e79429'
    version: str = 'Experimental'

    application_name: str = 'App Manager'

    save_path: str = os.path.abspath('./data/save.dat').replace('\\', '/')

    main_color_set: QSaveData.ColorSet = QSaveData.ColorSet(
        'cyan',
        QUtilsColor.from_hex('#00D2A8'),
        QUtilsColor.from_hex('#00BC99'),
        QUtilsColor.from_hex('#07E8BC'),
        QUtilsColor.from_hex('#236E61'),
    )
    neutral_color_set: QSaveData.ColorSet = QSaveData.ColorSet(
        'white',
        QUtilsColor.from_hex('#E3E3E3'),
        QUtilsColor.from_hex('#D7D7D7'),
        QUtilsColor.from_hex('#EFEFEF'),
        QUtilsColor.from_hex('#CACACA'),
    )

    icon_path: str = './data/icons/AppManager.svg'
#----------------------------------------------------------------------
