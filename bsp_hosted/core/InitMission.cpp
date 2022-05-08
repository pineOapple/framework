#include <OBSWConfig.h>
#include <bsp_hosted/core/InitMission.h>
#include <bsp_hosted/fsfwconfig/objects/systemObjectList.h>
#include <bsp_hosted/fsfwconfig/pollingsequence/pollingSequenceFactory.h>
#include <fsfw/modes/HasModesIF.h>
#include <fsfw/returnvalues/HasReturnvaluesIF.h>
#include <fsfw/serviceinterface.h>
#include <fsfw/tasks/FixedTimeslotTaskIF.h>
#include <fsfw/tasks/PeriodicTaskIF.h>
#include <fsfw/tasks/TaskFactory.h>

#include "example/utility/TaskCreation.h"
#include "fsfw_tests/integration/assemblies/TestAssembly.h"

#ifdef _WIN32
#include <fsfw/osal/windows/winTaskHelpers.h>
#endif

void InitMission::createTasks() {
  TaskFactory* taskFactory = TaskFactory::instance();
  if (taskFactory == nullptr) {
    return;
  }

  TaskPriority currPrio;
#ifdef _WIN32
  currPrio = tasks::makeWinPriority();
#endif

  TaskDeadlineMissedFunction deadlineMissedFunc = nullptr;
#if OBSW_PRINT_MISSED_DEADLINES == 1
  deadlineMissedFunc = TaskFactory::printMissedDeadline;
#endif

#if OBSW_ADD_CORE_COMPONENTS == 1

#ifdef __unix__
  currPrio = 40;
#endif
  /* TMTC Distribution */
  PeriodicTaskIF* distributerTask = taskFactory->createPeriodicTask(
      "DIST", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.1, deadlineMissedFunc);
  ReturnValue_t result = distributerTask->addComponent(objects::CCSDS_DISTRIBUTOR);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("CCSDS distributor", objects::CCSDS_DISTRIBUTOR);
  }
  result = distributerTask->addComponent(objects::PUS_DISTRIBUTOR);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS distributor", objects::PUS_DISTRIBUTOR);
  }
  result = distributerTask->addComponent(objects::TM_FUNNEL);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("TM funnel", objects::TM_FUNNEL);
  }

#ifdef __unix__
  currPrio = 50;
#endif
  /* UDP bridge */
  PeriodicTaskIF* udpBridgeTask = taskFactory->createPeriodicTask(
      "TCPIP_TMTC_BRIDGE", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.2, deadlineMissedFunc);
  result = udpBridgeTask->addComponent(objects::TCPIP_TMTC_BRIDGE);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("TMTC bridge", objects::TCPIP_TMTC_BRIDGE);
  }

#ifdef __unix__
  currPrio = 80;
#endif
  PeriodicTaskIF* udpPollingTask = taskFactory->createPeriodicTask(
      "TMTC_POLLING", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 2.0, deadlineMissedFunc);
  result = udpPollingTask->addComponent(objects::TCPIP_TMTC_POLLING_TASK);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("TMTC polling", objects::TCPIP_TMTC_POLLING_TASK);
  }

#ifdef __unix__
  currPrio = 20;
#endif
  PeriodicTaskIF* eventTask = taskFactory->createPeriodicTask(
      "EVENT", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.100, deadlineMissedFunc);
  result = eventTask->addComponent(objects::EVENT_MANAGER);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("Event Manager", objects::EVENT_MANAGER);
  }
#endif /* OBSW_ADD_CORE_COMPONENTS == 1 */

#if OBSW_ADD_TASK_EXAMPLE == 1

#ifdef __unix__
  currPrio = 50;
#endif
  FixedTimeslotTaskIF* timeslotDemoTask = taskFactory->createFixedTimeslotTask(
      "PST_TASK", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.5, deadlineMissedFunc);
  result = pst::pollingSequenceExamples(timeslotDemoTask);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    FSFW_LOGE("InitMission::createTasks: Timeslot demo task initialization failed\n");
  }

#ifdef __unix__
  currPrio = 40;
#endif
  PeriodicTaskIF* readerTask = taskFactory->createPeriodicTask(
      "READER_TASK", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 1.0, deadlineMissedFunc);
  result = readerTask->addComponent(objects::TEST_DUMMY_4);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("Dummy 4", objects::TEST_DUMMY_4);
  }
#endif /* OBSW_ADD_TASK_EXAMPLE == 1 */

#if OBSW_ADD_PUS_STACK == 1
  /* PUS Services */
#ifdef __unix__
  currPrio = 45;
#endif
  PeriodicTaskIF* pusVerification = taskFactory->createPeriodicTask(
      "PUS_VERIF_1", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.200, deadlineMissedFunc);
  result = pusVerification->addComponent(objects::PUS_SERVICE_1_VERIFICATION);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 1", objects::PUS_SERVICE_1_VERIFICATION);
  }

#ifdef __unix__
  currPrio = 50;
#endif
  PeriodicTaskIF* pusHighPrio = taskFactory->createPeriodicTask(
      "PUS_HIGH_PRIO", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.2, deadlineMissedFunc);
  result = pusHighPrio->addComponent(objects::PUS_SERVICE_2_DEVICE_ACCESS);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 2", objects::PUS_SERVICE_2_DEVICE_ACCESS);
  }
  result = pusHighPrio->addComponent(objects::PUS_SERVICE_5_EVENT_REPORTING);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 5", objects::PUS_SERVICE_5_EVENT_REPORTING);
  }
  result = pusHighPrio->addComponent(objects::PUS_SERVICE_9_TIME_MGMT);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 9", objects::PUS_SERVICE_9_TIME_MGMT);
  }

#ifdef __unix__
  currPrio = 40;
#endif
  PeriodicTaskIF* pusMedPrio = taskFactory->createPeriodicTask(
      "PUS_MED_PRIO", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.6, deadlineMissedFunc);
  result = pusMedPrio->addComponent(objects::PUS_SERVICE_3_HOUSEKEEPING);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 3", objects::PUS_SERVICE_3_HOUSEKEEPING);
  }
  result = pusMedPrio->addComponent(objects::PUS_SERVICE_8_FUNCTION_MGMT);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 8", objects::PUS_SERVICE_8_FUNCTION_MGMT);
  }
  result = pusMedPrio->addComponent(objects::PUS_SERVICE_20_PARAMETERS);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 20", objects::PUS_SERVICE_20_PARAMETERS);
  }
  result = pusMedPrio->addComponent(objects::PUS_SERVICE_200_MODE_MGMT);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 200", objects::PUS_SERVICE_200_MODE_MGMT);
  }

#ifdef __unix__
  currPrio = 30;
#endif
  PeriodicTaskIF* pusLowPrio = taskFactory->createPeriodicTask(
      "PUS_LOW_PRIO", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 1.2, deadlineMissedFunc);
  result = pusLowPrio->addComponent(objects::PUS_SERVICE_17_TEST);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("PUS 17", objects::PUS_SERVICE_17_TEST);
  }
#endif /* OBSW_ADD_PUS_STACK == 1 */

#if OBSW_ADD_DEVICE_HANDLER_DEMO == 1
#ifdef __unix__
  currPrio = 60;
#elif _WIN32
  currPrio =
      tasks::makeWinPriority(tasks::PriorityClass::CLASS_HIGH, tasks::PriorityNumber::HIGHEST);
#endif
  FixedTimeslotTaskIF* testDevicesTimeslotTask = taskFactory->createFixedTimeslotTask(
      "PST_TEST_TASK", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 2.0, deadlineMissedFunc);
  result = pst::pollingSequenceDevices(testDevicesTimeslotTask);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    FSFW_LOGE("InitMission::createTasks: Test PST initialization failed\n");
  }

#if _WIN32
  currPrio = tasks::makeWinPriority();
#endif

  PeriodicTaskIF* assemblyTask = taskFactory->createPeriodicTask(
      "ASS_TASK", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 2.0, nullptr);
  if (assemblyTask == nullptr) {
    task::printInitError("ASS_TASK", objects::TEST_ASSEMBLY);
  }
  result = assemblyTask->addComponent(objects::TEST_ASSEMBLY);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("ASS_TASK", objects::TEST_ASSEMBLY);
  }
#endif /* OBSW_ADD_DEVICE_HANDLER_DEMO == 1 */

#if OBSW_ADD_CONTROLLER_DEMO == 1
#ifdef __unix__
  currPrio = 45;
#endif
  PeriodicTaskIF* controllerTask = taskFactory->createPeriodicTask(
      "TEST_CTRL", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 0.8, deadlineMissedFunc);
  result = controllerTask->addComponent(objects::TEST_CONTROLLER);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("Controller Task", objects::TEST_CONTROLLER);
  }
#endif /* OBSW_ADD_CONTROLLER_DEMO == 1 */
#ifdef __unix__
  currPrio = 15;
#endif
  PeriodicTaskIF* testTask = TaskFactory::instance()->createPeriodicTask(
      "TEST_TASK", currPrio, PeriodicTaskIF::MINIMUM_STACK_SIZE, 1.0, deadlineMissedFunc);
  result = testTask->addComponent(objects::TEST_TASK);
  if (result != HasReturnvaluesIF::RETURN_OK) {
    task::printInitError("Test Task", objects::TEST_TASK);
  }

  FSFW_LOGI("Starting tasks..\n");

#if OBSW_ADD_CORE_COMPONENTS == 1
  distributerTask->startTask();
  udpBridgeTask->startTask();
  udpPollingTask->startTask();
  eventTask->startTask();
#endif /* OBSW_ADD_CORE_COMPONENTS == 1 */

#if OBSW_ADD_PUS_STACK == 1
  pusVerification->startTask();
  pusHighPrio->startTask();
  pusMedPrio->startTask();
  pusLowPrio->startTask();
#endif /* OBSW_ADD_PUS_STACK == 1 */

#if OBSW_ADD_TASK_EXAMPLE == 1
  timeslotDemoTask->startTask();
  readerTask->startTask();
#endif /* OBSW_ADD_TASK_EXAMPLE == 1 */

#if OBSW_ADD_DEVICE_HANDLER_DEMO == 1
  testDevicesTimeslotTask->startTask();
  assemblyTask->startTask();
#endif /* OBSW_ADD_DEVICE_HANDLER_DEMO == 1 */

#if OBSW_ADD_CONTROLLER_DEMO == 1
  controllerTask->startTask();
#endif /* OBSW_ADD_CONTROLLER_DEMO == 1 */

  testTask->startTask();

  FSFW_LOGI("Tasks started\n");

#if OBSW_ADD_DEVICE_HANDLER_DEMO
  auto* assembly = ObjectManager::instance()->get<HasModesIF>(objects::TEST_ASSEMBLY);
  if (assembly == nullptr) {
    return;
  }
#endif /* OBSW_ADD_DEVICE_HANDLER_DEMO */
}
