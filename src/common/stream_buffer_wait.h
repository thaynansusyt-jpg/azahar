// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <span>

namespace Common {
// Watches in one ring-buffer epoch have nondecreasing upper_bound and submission tick.
// Waiting for the last covered tick also covers every earlier submission on the queue.
// Returns watches.size() when no wait is needed, otherwise the LAST watch to consume.
template <class Watch>
std::size_t LastWatchToWait(std::span<const Watch> watches, std::size_t cursor,
                           std::uint64_t bound, std::uint64_t requested) {
    if (requested <= bound || cursor >= watches.size()) return watches.size();
    const auto it = std::lower_bound(watches.begin() + cursor, watches.end(), requested,
        [](const Watch& watch, std::uint64_t value) { return watch.upper_bound < value; });
    return it == watches.end() ? watches.size() - 1 : static_cast<std::size_t>(it - watches.begin());
}
} // namespace Common
