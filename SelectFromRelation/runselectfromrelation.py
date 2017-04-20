
### Original code by Salvatore Larosa###

'''
QGIS macro to enable selection on referenced geometry layer from
referencing geometryless table in a Project with Relations.
How it works:
1. Enable macros for the QGIS Project
2. Paste this code in Project->Macro
3. Save the Project.
Note: The QGIS project must have relationship between tables.
See https://goo.gl/w4NMZJ on how to create one-to-many relations.
'''

from qgis.PyQt.QtCore import QSettings
from PyQt4.QtGui import *
from qgis.utils import iface, reloadProjectMacros
from qgis.core import QgsFeatureRequest, QgsProject
from functools import partial

class RunSelectFromRelation(QDialog):
    s = QSettings()
    s.setValue("qgis/enableMacros", 3)

    def openProject(self):
        def selectionChanged(rl, fts):
            referencingLayer = rl.referencingLayer()
            referencedLayer = rl.referencedLayer()

            request = QgsFeatureRequest().setFilterFids(fts)

            ids = []
            for f in referencingLayer.getFeatures(request):
                ids.append(rl.getReferencedFeature(f).id())

            referencedLayer.setSelectedFeatures(ids)
            iface.setActiveLayer(referencedLayer)

        rM = QgsProject.instance().relationManager()
        rls = rM.relations()
        
        if bool(rls) != True:
            QMessageBox.warning(self, "Warning", "No relationship set in Project properties",  QMessageBox.Ok)
        else:
            for rlid, rl in rls.iteritems():
                referencingLayer = rl.referencingLayer()
                referencingLayer.selectionChanged.connect(partial(selectionChanged, rl))


    def saveProject(self):
        reloadProjectMacros()


