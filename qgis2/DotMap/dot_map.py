# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DotMap
                                 A QGIS plugin
 Create a dot layer from polygon
                              -------------------
        begin                : 2018-06-04
        git sha              : $Format:%H$
        copyright            : (C) 2018 by jose
        email                : josema.mira@gmail.com
 ***************************************************************************/
 This plugin is based in Chapter 8: "Creating a dot density map" from book
 "QGIS Python Programming Cookbook", author: Joel Lawhead
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon


from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from dot_map_dialog import DotMapDialog
import os.path
import random

class DotMap:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DotMap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Dot Map')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'DotMap')
        self.toolbar.setObjectName(u'DotMap')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DotMap', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = DotMapDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/DotMap/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Dot Map'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # limpiar form
        self.dlg.layerComboBox.clear()
        self.dlg.fieldComboBox.clear()
        self.dlg.minValBox.clear()
        self.dlg.maxValBox.clear()
        self.dlg.valForDot.clear()
        self.dlg.simMaxValBox.clear()
        self.dlg.simMinValBox.clear()
        self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        #bar = self.dlg.bar
        #bar.setValue(0)
        #bar.setMaximum(100)


        # Listar capas poligonales
        #borrar lista
        self.dlg.layerComboBox.clear()
        layer_list = []
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.geometryType() == QGis.Polygon:
                layer_list.append(layer.name())
                self.dlg.layerComboBox.addItem(layer.name())



        self.dlg.layerComboBox.activated.connect(self.getNumFields)
        self.dlg.simulationButton.setEnabled(False)



        # si no hay capas poligonales
        if not layer_list:
            QMessageBox.about(self.iface.mainWindow(), 'Message','Polygon layers not found')
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        #else:
            # show the dialog
            #self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            #self.dlg.show()
        # Run the dialog event loop
        self.dlg.show()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Evento cuando se hace clic en boton OK
            #from PyQt4.QtGui import QProgressDialog, QProgressBar
            dialog = QProgressDialog()
            dialog.setWindowTitle("Dot progress")
            #dialog.setLabelText("text")
            bar = QProgressBar(dialog)
            bar.setTextVisible(True)
            bar.setValue(0)
            dialog.setBar(bar)
            dialog.setMinimumWidth(300)
            dialog.show()

            name = self.dlg.layerComboBox.currentText()
            layer = QgsMapLayerRegistry.instance().mapLayersByName( name )[0]
            crs = layer.crs().authid()
            divisor = self.dlg.valForDot.text().encode('ascii','ignore')
            cuenta = layer.featureCount()
            #print "cuenta es: "+ str(cuenta)
            try:
                #divisor = int(divisor)
                dotLyr =  QgsVectorLayer('Point?crs='+crs, self.dlg.fieldComboBox.currentText() +' (1 dot = '+divisor+')', "memory")
                i = layer.fieldNameIndex(self.dlg.fieldComboBox.currentText())
                features = layer.getFeatures()
                vpr = dotLyr.dataProvider()
                # simbologia
                symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'black', 'size':'1'})
                dotLyr.rendererV2().setSymbol(symbol)
                dotFeatures = []
                j = 0

                for feature in features:
                    pop = feature.attributes()[i]
                    #Update the progress bar
                    j = j + 1
                    percent = (j/float(cuenta)) * 100
                    #print "percent is: " + str(int(percent))+ " %"
                    #self.dlg.bar.setValue(int(percent))
                    bar.setValue(percent)

                    if pop != 0:
                        density = pop / int(divisor)
                        found = 0
                        dots = []
                        g = feature.geometry()
                        minx = g.boundingBox().xMinimum()
                        miny = g.boundingBox().yMinimum()
                        maxx = g.boundingBox().xMaximum()
                        maxy = g.boundingBox().yMaximum()

                        while found < density:
                            x = random.uniform(minx,maxx)
                            y = random.uniform(miny,maxy)
                            #print str(x) + ' '+ str(y)
                            pnt = QgsPoint(x,y)
                            if g.contains(pnt):
                                dots.append(pnt)
                                found += 1
                                #print str(found)
                        geom = QgsGeometry.fromMultiPoint(dots)
                        f = QgsFeature()
                        f.setGeometry(geom)
                        dotFeatures.append(f)

                vpr.addFeatures(dotFeatures)
                dotLyr.updateExtents()
                QgsMapLayerRegistry.instance().addMapLayers([dotLyr])
                # limpiar form
                self.dlg.layerComboBox.clear()
                self.dlg.fieldComboBox.clear()
                self.dlg.minValBox.clear()
                self.dlg.maxValBox.clear()
                self.dlg.valForDot.clear()






            except Exception:
                QMessageBox.about(self.iface.mainWindow(), 'Error','Input can only be a number')
                #pass




    def getNumFields(self):
        self.dlg.fieldComboBox.clear()
        #QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('HelloWorld', "HelloWorld"), QCoreApplication.translate('HelloWorld', "HelloWorld"))
        name = self.dlg.layerComboBox.currentText()
        layer = QgsMapLayerRegistry.instance().mapLayersByName( name )[0]
        fields = layer.pendingFields()
        field_names = []
        for field in fields:
            if (field.typeName() == 'Integer' or field.typeName() == 'Integer64'):  # Real, String ...
                #print field.name() + 'tipo: ' + field.typeName()
                self.dlg.fieldComboBox.addItem(field.name())

        self.dlg.fieldComboBox.activated.connect(self.getStats)
        self.dlg.simulationButton.setEnabled(True)
        self.dlg.simulationButton.clicked.connect(self.simulation)

    def getStats(self):
        fieldSel = self.dlg.fieldComboBox.currentText()
        #QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('HelloWorld', "HelloWorld"), fieldSel)
        name = self.dlg.layerComboBox.currentText()
        layer = QgsMapLayerRegistry.instance().mapLayersByName( name )[0]

        pob = []
        for feature in layer.getFeatures():
            value = feature[fieldSel]
            pob.append( int(value) )

        maxVal = sorted(pob, reverse=True)[0]
        minVal = sorted(pob)[0]
        self.dlg.minValBox.setText(str(minVal))
        self.dlg.maxValBox.setText(str(maxVal))

    def simulation(self):
        try:
            if  int(self.dlg.valForDot.text()) > int(self.dlg.maxValBox.text()) :
                QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('ERROR', "ERROR"), "Divisor higher than max value")
            else:
                simMaxVal = int(self.dlg.maxValBox.text()) / int(self.dlg.valForDot.text())
                simMinVal = int(self.dlg.minValBox.text()) / int(self.dlg.valForDot.text())
                self.dlg.simMaxValBox.setText(str(simMaxVal))
                self.dlg.simMinValBox.setText(str(simMinVal))
                self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        except Exception:
            QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('ERROR', "ERROR"), "Void divisor or lower than 0 or divisor higher than max value")


