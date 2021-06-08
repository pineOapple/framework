#ifndef POLLINGSEQUENCE_POLLINGSEQUENCFACTORY_H_
#define POLLINGSEQUENCE_POLLINGSEQUENCFACTORY_H_

#include "OBSWConfig.h"
#include <fsfw/returnvalues/HasReturnvaluesIF.h>

class FixedTimeslotTaskIF;

namespace pst {
ReturnValue_t pollingSequenceExamples(FixedTimeslotTaskIF *thisSequence);
ReturnValue_t pollingSequenceDevices(FixedTimeslotTaskIF* thisSequence);
}

#endif /* POLLINGSEQUENCE_POLLINGSEQUENCFACTORY_H_ */
