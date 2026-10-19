// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <string_view>

namespace Common::LiteTrace {
enum class Event : std::size_t {
    ShaderWait, PipelineBuild, TextureLoad, TextureDecode, StreamReuseWait,
    GpuWait, GlShaderPath, StorageRead, StorageWrite, TextureUpload, GlProgramLink, Count
};
inline constexpr std::array<std::string_view, static_cast<std::size_t>(Event::Count)> Names{
    "shader_wait", "pipeline_build", "texture_load", "texture_decode", "stream_reuse_wait",
    "gpu_wait", "gl_shader_path", "storage_read", "storage_write", "texture_upload", "gl_program_link"};
struct Value { std::uint64_t calls{}, ns{}; };
using Snapshot = std::array<Value, Names.size()>;
struct Counter { std::atomic<std::uint64_t> calls{0}, ns{0}; };
inline std::array<Counter, Names.size()> counters{};
inline std::atomic_bool enabled{false};
// Counters are process lifetime cumulative. Snapshots use deltas; never reset live workers.
inline Snapshot Read() {
    Snapshot out{};
    for (std::size_t i = 0; i < out.size(); ++i) {
        out[i] = {counters[i].calls.load(std::memory_order_relaxed),
                  counters[i].ns.load(std::memory_order_relaxed)};
    }
    return out;
}
class Scope {
public:
    explicit Scope(Event event_) : event{event_}, active{enabled.load(std::memory_order_relaxed)} {
        if (active) start = Clock::now();
    }
    ~Scope() {
        if (!active) return;
        auto& counter = counters[static_cast<std::size_t>(event)];
        counter.ns.fetch_add(std::chrono::duration_cast<std::chrono::nanoseconds>(Clock::now() - start).count(),
                             std::memory_order_relaxed);
        counter.calls.fetch_add(1, std::memory_order_relaxed);
    }
    Scope(const Scope&) = delete;
    Scope& operator=(const Scope&) = delete;
private:
    using Clock = std::chrono::steady_clock;
    Event event;
    bool active;
    Clock::time_point start{};
};
} // namespace Common::LiteTrace
