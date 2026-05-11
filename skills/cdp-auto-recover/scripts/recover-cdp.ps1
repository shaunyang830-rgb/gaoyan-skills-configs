Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @('--remote-debugging-port=9222','--remote-allow-origins=*','--user-data-dir=C:\Users\杨顺\AppData\Local\Google\Chrome\User Data\CursorCDP2','--no-first-run','--no-default-browser-check') | Out-Null
Start-Sleep -Seconds 2
node 'c:\Users\杨顺\Documents\Obsidian Vault\.claude\skills\web-access\scripts\check-deps.mjs'
Invoke-RestMethod -Uri 'http://127.0.0.1:3456/targets' -Method Get | ConvertTo-Json -Depth 3
