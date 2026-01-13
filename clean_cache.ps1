# 设置内部处理编码
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Cleaning..."
# 清理 __pycache__
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Force -Recurse
# 清理 Blender 备份文件 (*.blend1)
Get-ChildItem -Path . -Filter "*.blend1" -Recurse | Remove-Item -Force
Write-Host "Done!"
Start-Sleep -Seconds 2