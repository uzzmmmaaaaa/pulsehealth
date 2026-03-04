Write-Host "Downloading WordPress..."
Invoke-WebRequest -Uri "https://wordpress.org/latest.zip" -OutFile "latest.zip"
Write-Host "Extracting WordPress to XAMPP htdocs..."
Expand-Archive -Path "latest.zip" -DestinationPath "C:\xampp\htdocs" -Force
Write-Host "WordPress successfully extracted to C:\xampp\htdocs\wordpress"

Write-Host "Starting XAMPP Apache and MySQL..."
Start-Process "C:\xampp\xampp_start.exe" -NoNewWindow
Write-Host "XAMPP Services started."
