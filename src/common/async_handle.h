// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <atomic>
#include <condition_variable>
#include <mutex>
#include "common/lite_trace.h"

namespace Common {
struct AsyncHandle {
    AsyncHandle(bool done = false) : is_done{done} {}
    [[nodiscard]] bool IsDone() noexcept {
        // Publish the shader module/pipeline written by the compilation worker.
        return is_done.load(std::memory_order_acquire);
    }
    void WaitDone() noexcept {
        if (IsDone()) return;
        LiteTrace::Scope trace{LiteTrace::Event::ShaderWait};
        std::unique_lock lock{mutex};
        condvar.wait(lock, [this] { return IsDone(); });
    }
    void MarkDone(bool done = true) noexcept {
        {
            // Keep predicate mutation under the wait mutex to prevent lost wakeups.
            std::scoped_lock lock{mutex};
            is_done.store(done, std::memory_order_release);
        }
        condvar.notify_all();
    }
private:
    std::condition_variable condvar;
    std::mutex mutex;
    std::atomic_bool is_done{false};
};
} // namespace Common
