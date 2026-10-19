// SPDX-License-Identifier: GPL-2.0-or-later
package org.citra.citra_emu.features.settings.model

/** One-shot presets: normal settings remain editable after applying. */
object LitePerformance {
    fun settings(): List<AbstractSetting> = listOf(
        IntSetting.RESOLUTION_FACTOR, IntSetting.TEXTURE_FILTER, IntSetting.FRAME_LIMIT,
        IntSetting.USE_FRAME_LIMIT, IntSetting.CPU_CLOCK_SPEED, IntSetting.STEREOSCOPIC_3D_DEPTH,
        BooleanSetting.DISK_SHADER_CACHE, BooleanSetting.SHADERS_ACCURATE_MUL,
        BooleanSetting.LINEAR_FILTERING, BooleanSetting.ASYNC_SHADERS,
        BooleanSetting.DISABLE_RIGHT_EYE_RENDER
    )

    fun apply(profile: Int): List<AbstractSetting> {
        require(profile in 0..2)
        IntSetting.RESOLUTION_FACTOR.int = 1
        IntSetting.TEXTURE_FILTER.int = 0
        IntSetting.FRAME_LIMIT.int = 100
        IntSetting.USE_FRAME_LIMIT.int = 1
        IntSetting.CPU_CLOCK_SPEED.int = 100
        IntSetting.STEREOSCOPIC_3D_DEPTH.int = 0
        BooleanSetting.DISK_SHADER_CACHE.boolean = true
        BooleanSetting.SHADERS_ACCURATE_MUL.boolean = true
        BooleanSetting.LINEAR_FILTERING.boolean = profile == 0
        BooleanSetting.ASYNC_SHADERS.boolean = profile == 2
        BooleanSetting.DISABLE_RIGHT_EYE_RENDER.boolean = profile == 2
        // Backend, VSync and SPIR-V remain user choices until device A/B testing.
        return listOf(
            IntSetting.RESOLUTION_FACTOR,
            IntSetting.TEXTURE_FILTER,
            IntSetting.FRAME_LIMIT,
            IntSetting.USE_FRAME_LIMIT,
            IntSetting.CPU_CLOCK_SPEED,
            IntSetting.STEREOSCOPIC_3D_DEPTH,
            BooleanSetting.DISK_SHADER_CACHE,
            BooleanSetting.SHADERS_ACCURATE_MUL,
            BooleanSetting.LINEAR_FILTERING,
            BooleanSetting.ASYNC_SHADERS,
            BooleanSetting.DISABLE_RIGHT_EYE_RENDER
        )
    }
}
