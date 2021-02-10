

#ifndef QGSPATCH_H
#define QGSPATCH_H

#include "qgsvectorlayer.h"
#include "qgis_core.h"

#if defined qgispatches_EXPORTS
    #define QGISPATCHES_EXPORT Q_DECL_EXPORT
#else
    #define QGISPATCHES_EXPORT Q_DECL_IMPORT
#endif

extern "C"
bool QGISPATCHES_EXPORT setAllowCommit(QgsVectorLayer * layer, bool allow);


#endif
