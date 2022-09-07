#ifndef POLLINGSEQUENCE_POLLINGSEQUENCFACTORY_H_
#define POLLINGSEQUENCE_POLLINGSEQUENCFACTORY_H_

#include <fsfw/retval.h>

#include "OBSWConfig.h"

class FixedTimeslotTaskIF;

namespace pst {
ReturnValue_t pollingSequenceExamples(FixedTimeslotTaskIF* thisSequence);
ReturnValue_t pollingSequenceDevices(FixedTimeslotTaskIF* thisSequence);
}  // namespace pst

#endif /* POLLINGSEQUENCE_POLLINGSEQUENCFACTORY_H_ */
