#ifndef FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H
#define FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H

#include <utility>

#include "fsfw/cfdp/handler/DestHandler.h"
#include "fsfw/objectmanager/SystemObject.h"
#include "fsfw/tasks/ExecutableObjectIF.h"
#include "fsfw/tmtcservices/AcceptsTelecommandsIF.h"
#include "fsfw/tmtcservices/TmTcMessage.h"

struct FsfwHandlerParams {
  FsfwHandlerParams(object_id_t objectId, HasFileSystemIF& vfs, AcceptsTelemetryIF& packetDest,
                    StorageManagerIF& tcStore, StorageManagerIF& tmStore)
      : objectId(objectId), vfs(vfs), packetDest(packetDest), tcStore(tcStore), tmStore(tmStore) {}
  object_id_t objectId{};
  HasFileSystemIF& vfs;
  AcceptsTelemetryIF& packetDest;
  StorageManagerIF& tcStore;
  StorageManagerIF& tmStore;
};

struct CfdpHandlerCfg {
  CfdpHandlerCfg(cfdp::EntityId localId, cfdp::IndicationCfg indicationCfg,
                 cfdp::PacketInfoListBase& packetInfo, cfdp::LostSegmentsListBase& lostSegmentsList,
                 cfdp::RemoteConfigTableIF& remoteCfgProvider)
      : id(std::move(localId)),
        indicCfg(indicationCfg),
        packetInfoList(packetInfo),
        lostSegmentsList(lostSegmentsList),
        remoteCfgProvider(remoteCfgProvider) {}

  cfdp::EntityId id;
  cfdp::IndicationCfg indicCfg;
  cfdp::PacketInfoListBase& packetInfoList;
  cfdp::LostSegmentsListBase& lostSegmentsList;
  cfdp::RemoteConfigTableIF& remoteCfgProvider;
};

class CfdpHandler : public SystemObject,
                    public cfdp::UserBase,
                    public cfdp::FaultHandlerBase,
                    public ExecutableObjectIF,
                    public AcceptsTelecommandsIF {
 public:
  explicit CfdpHandler(const FsfwHandlerParams& fsfwParams, const CfdpHandlerCfg& cfdpCfg);

  [[nodiscard]] const char* getName() const override;
  [[nodiscard]] uint32_t getIdentifier() const override;
  [[nodiscard]] MessageQueueId_t getRequestQueue() const override;

  ReturnValue_t initialize() override;
  ReturnValue_t performOperation(uint8_t operationCode) override;

  // CFDP user overrides
  void transactionIndication(const cfdp::TransactionId& id) override;
  void eofSentIndication(const cfdp::TransactionId& id) override;
  void transactionFinishedIndication(const cfdp::TransactionFinishedParams& params) override;
  void metadataRecvdIndication(const cfdp::MetadataRecvdParams& params) override;
  void fileSegmentRecvdIndication(const cfdp::FileSegmentRecvdParams& params) override;
  void reportIndication(const cfdp::TransactionId& id, cfdp::StatusReportIF& report) override;
  void suspendedIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code) override;
  void resumedIndication(const cfdp::TransactionId& id, size_t progress) override;
  void faultIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code,
                       size_t progress) override;
  void abandonedIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code,
                           size_t progress) override;
  void eofRecvIndication(const cfdp::TransactionId& id) override;
  void noticeOfSuspensionCb(cfdp::ConditionCode code) override;
  void noticeOfCancellationCb(cfdp::ConditionCode code) override;
  void abandonCb(cfdp::ConditionCode code) override;
  void ignoreCb(cfdp::ConditionCode code) override;

 private:
  MessageQueueIF* msgQueue = nullptr;
  cfdp::DestHandler destHandler;
  StorageManagerIF* tcStore = nullptr;
  StorageManagerIF* tmStore = nullptr;

  ReturnValue_t handleCfdpPacket(TmTcMessage& msg);
};

#endif  // FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H
