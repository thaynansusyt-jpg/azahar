// Copyright 2026 Azahar Lite contributors
// Licensed under GPLv2 or any later version
// Refer to the misc/licenses/gplv2.txt file included.

package org.citra.citra_emu.utils

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import android.widget.Toast
import androidx.preference.PreferenceManager
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import java.util.Locale
import org.citra.citra_emu.R
import org.citra.citra_emu.features.settings.model.BooleanSetting
import org.citra.citra_emu.features.settings.model.IntSetting
import org.citra.citra_emu.features.settings.utils.SettingsFile
import org.ini4j.Wini

/** Recommendations are explicit and never run automatically on launch. */
object LiteSettings {
    private const val BACKUP = "lite_config_backup"
    private const val BACKUP_URI = "lite_config_backup_uri"

    fun show(context: Context) {
        val memory = ActivityManager.MemoryInfo()
        (context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager)
            .getMemoryInfo(memory)
        val gib = 1024.0 * 1024.0 * 1024.0
        val soc = if (Build.VERSION.SDK_INT >= 31) Build.SOC_MODEL else Build.HARDWARE
        val message = context.getString(
            R.string.lite_device_summary,
            "${Build.MANUFACTURER} ${Build.MODEL} ($soc)",
            String.format(Locale.getDefault(), "%.1f", memory.totalMem / gib),
            String.format(Locale.getDefault(), "%.1f", memory.availMem / gib),
            Runtime.getRuntime().availableProcessors(),
            context.getString(
                if (memory.lowMemory) R.string.lite_low_memory else R.string.lite_normal_memory
            )
        )
        val prefs = PreferenceManager.getDefaultSharedPreferences(context)
        val dialog = MaterialAlertDialogBuilder(context)
            .setTitle(R.string.lite_profile_title)
            .setMessage(message)
            .setPositiveButton(R.string.lite_apply) { _, _ -> update(context, false) }
            .setNegativeButton(android.R.string.cancel, null)
        if (prefs.contains(BACKUP)) {
            dialog.setNeutralButton(R.string.lite_restore) { _, _ -> update(context, true) }
        }
        dialog.show()
    }

    private fun update(context: Context, restore: Boolean) {
        val resolver = context.contentResolver
        val prefs = PreferenceManager.getDefaultSharedPreferences(context)
        var original: String? = null
        var uri: android.net.Uri? = null
        var writeStarted = false
        try {
            val target = SettingsFile.getSettingsFile(SettingsFile.FILE_NAME_CONFIG).uri
            uri = target
            val before = checkNotNull(resolver.openInputStream(target)).bufferedReader().use {
                it.readText()
            }
            original = before
            val replacement = if (restore) {
                check(prefs.getString(BACKUP_URI, null) == target.toString())
                checkNotNull(prefs.getString(BACKUP, null))
            } else {
                // Keep the original snapshot when applying again to the same user folder.
                if (prefs.getString(BACKUP_URI, null) != target.toString()) {
                    check(prefs.edit().putString(BACKUP, before)
                        .putString(BACKUP_URI, target.toString()).commit())
                }
                val ini = Wini(before.byteInputStream())
                val ints = mapOf(
                    IntSetting.RESOLUTION_FACTOR to 1,
                    IntSetting.STEREOSCOPIC_3D_MODE to 0,
                    IntSetting.STEREOSCOPIC_3D_DEPTH to 0,
                    IntSetting.TEXTURE_FILTER to 0
                )
                val booleans = mapOf(
                    BooleanSetting.CPU_JIT to true,
                    BooleanSetting.HW_SHADER to true,
                    BooleanSetting.SHADER_JIT to true,
                    BooleanSetting.DISK_SHADER_CACHE to true,
                    BooleanSetting.CUSTOM_TEXTURES to false,
                    BooleanSetting.PRELOAD_TEXTURES to false,
                    BooleanSetting.DUMP_TEXTURES to false
                )
                ints.forEach { (setting, value) -> ini.put(setting.section, setting.key, value) }
                booleans.forEach { (setting, value) -> ini.put(setting.section, setting.key, value) }
                java.io.StringWriter().use { writer ->
                    ini.store(writer)
                    writer.toString()
                }
            }
            writeStarted = true
            checkNotNull(resolver.openOutputStream(target, "wt")).bufferedWriter().use {
                it.write(replacement)
            }
            // Reload Java setting models from disk; the native core loads on next launch.
            org.citra.citra_emu.features.settings.model.Settings().loadSettings()
            if (restore) prefs.edit().remove(BACKUP).remove(BACKUP_URI).apply()
            Toast.makeText(context, R.string.lite_saved, Toast.LENGTH_LONG).show()
        } catch (exception: Exception) {
            val rollbackUri = uri
            val rollbackText = original
            if (writeStarted && rollbackUri != null && rollbackText != null) {
                runCatching {
                    checkNotNull(resolver.openOutputStream(rollbackUri, "wt")).bufferedWriter().use {
                        it.write(rollbackText)
                    }
                }
            }
            Log.error("[Azahar Lite] Could not update configuration: ${exception.message}")
            Toast.makeText(context, R.string.lite_failed, Toast.LENGTH_LONG).show()
        }
    }
}
