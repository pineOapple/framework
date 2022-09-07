#ifndef FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H
#define FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H

#include <utility>

#include "fsfw/cfdp/handler/DestHandler.h"
#include "fsfw/objectmanager/SystemObject.h"
#include "fsfw/tasks/ExecutableObjectIF.h"
#include "fsfw/tmtcservices/AcceptsTelecommandsIF.h"

struct HandlerCfg {
  HandlerCfg(object_id_t objectId, cfdp::LocalEntityCfg cfg, HasFileSystemIF& vfs,
             AcceptsTelemetryIF& packetDest, cfdp::PacketInfoListBase& packetInfo,
             cfdp::LostSegmentsListBase& lostSegmentsList)
      : objectId(objectId),
        cfg(std::move(cfg)),
        vfs(vfs),
        packetInfoList(packetInfo),
        lostSegmentsList(lostSegmentsList),
        packetDest(packetDest) {}
  object_id_t objectId{};
  cfdp::LocalEntityCfg cfg;
  HasFileSystemIF& vfs;
  cfdp::PacketInfoListBase& packetInfoList;
  cfdp::LostSegmentsListBase& lostSegmentsList;
  AcceptsTelemetryIF& packetDest;
};

class CfdpHandler : public SystemObject,
                    public cfdp::UserBase,
                    public cfdp::RemoteConfigTableIF,
                    public ExecutableObjectIF,
                    public AcceptsTelecommandsIF {
 public:
  explicit CfdpHandler(const HandlerCfg& cfg);
  bool getRemoteCfg(const cfdp::EntityId& remoteId, cfdp::RemoteEntityCfg** cfg) override;
  [[nodiscard]] const char* getName() const override;
  [[nodiscard]] uint32_t getIdentifier() const override;
  [[nodiscard]] MessageQueueId_t getRequestQueue() const override;

  ReturnValue_t initialize() override;
  ReturnValue_t performOperation(uint8_t operationCode) override;
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

 private:
  MessageQueueIF* msgQueue = nullptr;
  cfdp::DestHandler destHandler;
};

#endif  // FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H
