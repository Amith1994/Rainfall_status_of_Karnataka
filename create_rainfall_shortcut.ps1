$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = "e:\1. AntiGravity\Rainfall_Status_App" }

$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop "Rainfall Status Auto-Updater.lnk"
$targetPath = Join-Path $scriptDir "Update_Rainfall_Status.bat"
$workDir = $scriptDir

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $targetPath
$Shortcut.WorkingDirectory = $workDir
$Shortcut.WindowStyle = 1
$Shortcut.Description = "KSNDMC Rainfall Status Auto-Updater & Analytics App"
$Shortcut.IconLocation = "shell32.dll,238"
$Shortcut.Save()

Write-Host "Desktop shortcut updated successfully at: $shortcutPath"
Write-Host "Target: $targetPath"
