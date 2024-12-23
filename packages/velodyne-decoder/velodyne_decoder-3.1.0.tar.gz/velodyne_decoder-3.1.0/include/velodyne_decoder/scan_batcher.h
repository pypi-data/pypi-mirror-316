// Copyright (c) 2023, Martin Valgur
// SPDX-License-Identifier: BSD-3-Clause

#pragma once

#include "velodyne_decoder/config.h"
#include "velodyne_decoder/types.h"

#include <gsl/span>
#include <memory>
#include <optional>
#include <vector>

namespace velodyne_decoder {

template <typename PacketT = VelodynePacket> class ScanBatcher {
public:
  explicit inline ScanBatcher(const Config &config);

  /** @brief Pushes a packet into the batcher.
   * @return true if the scan is complete, false otherwise.
   */
  inline bool push(const PacketT &packet);

  [[nodiscard]] inline bool empty() const;

  [[nodiscard]] inline size_t size() const;

  /** @brief True if the current scan is complete.
   */
  [[nodiscard]] inline bool scanComplete() const;

  /** @brief The contents of the current scan.
   */
  [[nodiscard]] inline const std::shared_ptr<std::vector<PacketT>> &scanPackets() const;

  inline void reset(std::shared_ptr<std::vector<PacketT>> scan_packets);

  inline void reset();

private:
  std::shared_ptr<std::vector<PacketT>> scan_packets_ = std::make_shared<std::vector<PacketT>>();
  int initial_azimuth_                                = -1;
  int coverage_                                       = 0;
  bool scan_complete_                                 = false;
  std::optional<PacketT> kept_last_packet_            = std::nullopt;

  // config
  const bool is_device_time_valid_;
  const int cut_angle_;
  const double duration_threshold_ = 0.3; // max scan duration at ~4 Hz
};

inline PacketView toPacketView(const VelodynePacket &packet) { return {packet}; }

extern template class ScanBatcher<VelodynePacket>;

} // namespace velodyne_decoder

#include "scan_batcher.inl"
