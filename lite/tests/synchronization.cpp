// SPDX-License-Identifier: GPL-2.0-or-later
#include <cassert>
#include <cstdint>
#include <future>
#include <random>
#include <thread>
#include <vector>
#include "common/async_handle.h"
#include "common/stream_buffer_wait.h"

struct Watch { std::uint64_t tick, upper_bound; };
int main() {
    Common::AsyncHandle ready{true};
    ready.WaitDone();
    for (int repeat = 0; repeat < 250; ++repeat) {
        Common::AsyncHandle handle;
        int payload = 0;
        std::vector<std::future<int>> readers;
        for (int i = 0; i < 4; ++i) readers.emplace_back(std::async(std::launch::async, [&] {
            handle.WaitDone();
            return payload;
        }));
        std::thread producer([&] { payload = 123456; handle.MarkDone(); });
        for (auto& reader : readers) assert(reader.get() == 123456);
        producer.join();
        assert(handle.IsDone());
        handle.WaitDone();
    }
    // Compare the exact cursor, bound and final waited tick with the original loop.
    std::mt19937 random{42};
    for (int trial = 0; trial < 5000; ++trial) {
        std::vector<Watch> watches;
        std::uint64_t tick = 0, upper = 0;
        const auto count = random() % 300;
        for (unsigned i = 0; i < count; ++i) {
            tick += random() % 3;
            upper += random() % 100;
            watches.push_back({tick, upper});
        }
        std::size_t cursor = 0;
        std::uint64_t bound = 0;
        for (int request = 0; request < 100; ++request) {
            const std::uint64_t requested = random() % (upper + 200);
            auto original_cursor = cursor;
            auto original_bound = bound;
            std::uint64_t original_tick = 0;
            bool waited = false;
            while (requested > original_bound && original_cursor < watches.size()) {
                const auto& watch = watches[original_cursor++];
                original_bound = watch.upper_bound;
                original_tick = watch.tick;
                waited = true;
            }
            const auto last = Common::LastWatchToWait(std::span<const Watch>{watches}, cursor, bound, requested);
            assert((last != watches.size()) == waited);
            if (last != watches.size()) {
                assert(watches[last].tick == original_tick);
                bound = watches[last].upper_bound;
                cursor = last + 1;
            }
            assert(cursor == original_cursor && bound == original_bound);
        }
    }
    // Diagnostic scopes are disabled by default and cumulative when enabled.
    using namespace Common::LiteTrace;
    auto before = Read();
    { Scope disabled{Event::TextureDecode}; }
    assert(Read()[3].calls == before[3].calls);
    enabled = true;
    { Scope active{Event::TextureDecode}; }
    enabled = false;
    assert(Read()[3].calls == before[3].calls + 1);
}
