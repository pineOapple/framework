#include "ObjectFactory.h"
#include "OBSWConfig.h"
#include <bsp_hosted/fsfwconfig/objects/systemObjectList.h>
#include <bsp_hosted/fsfwconfig/tmtc/apid.h>
#include <bsp_hosted/fsfwconfig/tmtc/pusIds.h>

#include "fsfw_tests/integration/task/TestTask.h"

#include "example/utility/TmFunnel.h"
#include "example/core/GenericFactory.h"

#include <fsfw/monitoring/MonitoringMessageContent.h>
#include <fsfw/storagemanager/PoolManager.h>
#include <fsfw/datapoollocal/LocalDataPoolManager.h>
#include <fsfw/tmtcpacket/pus/tm.h>
#include <fsfw/tmtcservices/CommandingServiceBase.h>
#include <fsfw/tmtcservices/PusServiceBase.h>

#if  OBSW_USE_TCP_SERVER == 0
#include <fsfw/osal/common/UdpTcPollingTask.h>
#include <fsfw/osal/common/UdpTmTcBridge.h>
#else
#include "fsfw/osal/common/TcpTmTcServer.h"
#include "fsfw/osal/common/TcpTmTcBridge.h"
#endif

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

    // TMTC Reception via TCP/IP socket
#if  OBSW_USE_TCP_SERVER == 0
    auto tmtcBridge = new UdpTmTcBridge(objects::TCPIP_TMTC_BRIDGE, objects::CCSDS_DISTRIBUTOR);
    tmtcBridge->setMaxNumberOfPacketsStored(50);
    sif::info << "Opening UDP TMTC server on port " << tmtcBridge->getUdpPort() << std::endl;
    new UdpTcPollingTask(objects::TCPIP_TMTC_POLLING_TASK, objects::TCPIP_TMTC_BRIDGE);
#else
    auto tmtcBridge = new TcpTmTcBridge(objects::TCPIP_TMTC_BRIDGE, objects::CCSDS_DISTRIBUTOR);
    tmtcBridge->setMaxNumberOfPacketsStored(50);
    auto tmtcServer = new TcpTmTcServer(objects::TCPIP_TMTC_POLLING_TASK, objects::TCPIP_TMTC_BRIDGE);
    sif::info << "Opening TCP TMTC server on port " << tmtcServer->getTcpPort() << std::endl;
#endif

#endif /* OBSW_ADD_CORE_COMPONENTS == 1 */

    bool periodicEvent = false;
#if OBSW_TASK_PERIODIC_EVENT == 1
    periodicEvent = true;
#endif
    new TestTask(objects::TEST_TASK, false, periodicEvent);

    ObjectFactory::produceGenericObjects();
}
