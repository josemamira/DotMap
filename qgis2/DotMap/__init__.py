# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DotMap
                                 A QGIS plugin
 Create a dot layer from polygon
                             -------------------
        begin                : 2018-06-04
        copyright            : (C) 2018 by jose
        email                : josema.mira@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load DotMap class from file DotMap.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .dot_map import DotMap
    return DotMap(iface)
