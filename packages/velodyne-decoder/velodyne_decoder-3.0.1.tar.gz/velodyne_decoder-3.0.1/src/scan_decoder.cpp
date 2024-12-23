// Copyright (c) 2021-2023, Martin Valgur
// SPDX-License-Identifier: BSD-3-Clause

#include "velodyne_decoder/scan_decoder.h"
#include "velodyne_decoder/types.h"

namespace velodyne_decoder {

ScanDecoder::ScanDecoder(const Config &config)
    : packet_decoder_(config), timestamp_first_packet_(config.timestamp_first_packet) {}

std::pair<TimePair, PointCloud> ScanDecoder::decode(const std::vector<PacketView> &scan_packets) {
  cloud_.clear();
  TimePair scan_stamp =
      timestamp_first_packet_ ? scan_packets.front().stamp : scan_packets.back().stamp;
  for (const auto &packet : scan_packets) {
    packet_decoder_.unpack(packet, scan_stamp, cloud_);
  }
  std::pair<TimePair, PointCloud> result;
  result.first = scan_stamp;
  result.second.reserve(cloud_.capacity());
  cloud_.swap(result.second);
  return result;
}

std::pair<TimePair, PointCloud>
ScanDecoder::decode(const std::vector<VelodynePacket> &scan_packets) {
  std::vector<PacketView> packet_views;
  packet_views.reserve(scan_packets.size());
  for (PacketView packet : scan_packets)
    packet_views.emplace_back(packet);
  return decode(packet_views);
}

std::optional<ModelId> ScanDecoder::modelId() const { return packet_decoder_.modelId(); }

std::optional<ReturnMode> ScanDecoder::returnMode() const { return packet_decoder_.returnMode(); }

} // namespace velodyne_decoder
