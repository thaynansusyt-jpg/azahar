// SPDX-License-Identifier: GPL-3.0-or-later
#include "core/perf_stats.h"
static_assert(Core::PerfStats::Clock::is_steady);
static_assert(Core::FrameLimiter::Clock::is_steady);
int main() {}
