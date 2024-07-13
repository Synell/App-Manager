#----------------------------------------------------------------------

    # Libraries
from ..QtUtils import QUtilsColor, QColorSet
import os
#----------------------------------------------------------------------

    # Class
class Info:
    def __new__(cls) -> None:
        return None

    build: str = '07e7d408'
    version: str = 'Experimental'

    application_name: str = 'App Manager'

    save_path: str = os.path.abspath('./data/save.dat').replace('\\', '/')

    main_color_set: QColorSet = QColorSet(
        'cyan',
        QUtilsColor.from_hex('#00B4BE'),
        QUtilsColor.from_hex('#009CA8'),
        QUtilsColor.from_hex('#00C8D4'),
        QUtilsColor.from_hex('#0F545A'),
    )
    neutral_color_set: QColorSet = QColorSet(
        'white',
        QUtilsColor.from_hex('#E3E3E3'),
        QUtilsColor.from_hex('#D7D7D7'),
        QUtilsColor.from_hex('#EFEFEF'),
        QUtilsColor.from_hex('#CACACA'),
    )

    icon_path: str = './data/icons/AppManager.svg'
#----------------------------------------------------------------------
