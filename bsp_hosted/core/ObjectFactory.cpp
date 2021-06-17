#include "ObjectFactory.h"
#include "OBSWConfig.h"
#include <bsp_hosted/fsfwconfig/objects/systemObjectList.h>
#include <bsp_hosted/fsfwconfig/tmtc/apid.h>
#include <bsp_hosted/fsfwconfig/tmtc/pusIds.h>

#include <test/TestTask.h>

#include <mission/utility/TmFunnel.h>
#include <mission/core/GenericFactory.h>

#include <fsfw/monitoring/MonitoringMessageContent.h>
#include <fsfw/storagemanager/PoolManager.h>
#include <fsfw/datapoollocal/LocalDataPoolManager.h>
#include <fsfw/tmtcpacket/pus/tm.h>
#include <fsfw/tmtcservices/CommandingServiceBase.h>
#include <fsfw/tmtcservices/PusServiceBase.h>

#include <fsfw/osal/common/UdpTcPollingTask.h>
#include <fsfw/osal/common/UdpTmTcBridge.h>

void ObjectFactory::produce(void* args) {
    Factory::setStaticFrameworkObjectIds();

#if OBSW_ADD_CORE_COMPONENTS == 1
    {
        LocalPool::LocalPoolConfig poolCfg = {
                {16, 100}, {32, 50}, {64, 25}, {128,15}, {1024, 5}
        };
        new PoolManager(objects::TC_STORE, poolCfg);
    }

    {
        LocalPool::LocalPoolConfig poolCfg = {
                {16, 100}, {32, 50}, {64, 25}, {128,15}, {1024, 5}
        };
        new PoolManager(objects::TM_STORE, poolCfg);
    }

    {
        LocalPool::LocalPoolConfig poolCfg = {
                {16, 100}, {32, 50}, {64, 25}, {128,15}, {1024, 5}
        };
        new PoolManager(objects::IPC_STORE, poolCfg);
    }

    /* TMTC Reception via UDP socket */
    auto tmtcBridge = new UdpTmTcBridge(objects::UDP_BRIDGE, objects::CCSDS_DISTRIBUTOR);
    tmtcBridge->setMaxNumberOfPacketsStored(20);
    new UdpTcPollingTask(objects::UDP_POLLING_TASK, objects::UDP_BRIDGE);

#endif /* OBSW_ADD_CORE_COMPONENTS == 1 */

    new TestTask(objects::TEST_TASK, false);

    ObjectFactory::produceGenericObjects();
}
