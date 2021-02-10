#include "qgispatch.h"

bool setAllowCommit(QgsVectorLayer * layer, bool allow)
{
    if ( layer && layer->allowCommit() != allow)
    {
        layer->setAllowCommit( allow );
        return true;
    }
    return false;
}
