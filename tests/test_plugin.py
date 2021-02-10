

from functools import partial
from ctypes import c_bool, c_void_p
import sip
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry
from qgis.testing import start_app, unittest
from qgis.testing.mocked import get_iface
from ..ConflictResolver import ConflictResolver

APP = start_app()

IFACE = get_iface()

PLUGIN = ConflictResolver(IFACE)

class TestConflictResolverPlugin(unittest.TestCase):

    def testAllowEdit(self):
        """Test validators"""

        def _validate_gis_application(layer):
            """Evaluate a decent GIS application"""

            ok = True
            buffer = layer.editBuffer()
            if buffer:
                for fid, f in buffer.addedFeatures().items():
                    try:
                        if not f.attribute('gis_app').upper().startswith("QGIS"):
                            ok = False
                    except KeyError:
                        pass

            PLUGIN.libqgispatches.setAllowCommit(c_void_p(sip.unwrapinstance(layer)), c_bool(ok))

        layer = QgsVectorLayer("Point?srid=EPSG:4326&field=gis_app:string",
                               "gis_apps", "memory")
        self.assertTrue(layer.isValid())
        layer.beforeCommitChanges.connect(partial(_validate_gis_application, layer))

        self.assertTrue(layer.startEditing())
        f = QgsFeature(layer.fields())
        g = QgsGeometry.fromWkt('point(9 45)')
        f.setGeometry(g)
        f.setAttributes(['QGIS'])
        self.assertTrue(layer.addFeatures([f]))
        self.assertTrue(layer.commitChanges())

        self.assertTrue(layer.startEditing())
        f = QgsFeature(layer.fields())
        g = QgsGeometry.fromWkt('point(9 45)')
        f.setGeometry(g)
        f.setAttributes(['ArcGIS'])
        self.assertTrue(layer.addFeatures([f]))
        self.assertFalse(layer.commitChanges())

        buffer = layer.editBuffer()
        fid = list(buffer.addedFeatures().values())[0].id()
        self.assertTrue(layer.changeAttributeValue(fid, 0, 'QGIS is better than ArcGIS'))
        self.assertTrue(layer.commitChanges())

        # Verify
        self.assertEqual([f.attribute('gis_app') for f in layer.getFeatures()], ['QGIS', 'QGIS is better than ArcGIS'])


if __name__ == "__main__":
    unittest.main()
