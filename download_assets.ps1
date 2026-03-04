$htmlFiles = Get-ChildItem -Path ".\*.html"
$cssFiles = Get-ChildItem -Path ".\css\*.css"

$baseImgDir = "assets\images"
$doctorsDir = Join-Path $baseImgDir "doctors"
$iconsDir = Join-Path $baseImgDir "icons"
$bannersDir = Join-Path $baseImgDir "banners"

$downloaded = @{}
$docCounter = 1
$bannerCounter = 1
$iconCounter = 1

function Download-And-Get-Local-Path {
    param([string]$url, [string]$contextHint)
    
    if ($downloaded.ContainsKey($url)) {
        return $downloaded[$url]
    }
    
    Write-Host "Downloading $url ..."
    
    try {
        if ($contextHint -match "doctor" -or $url -match "w=300" -or $url -match "w=150") {
            $filename = "doctor_$docCounter.jpg"
            $localPath = Join-Path $doctorsDir $filename
            $urlPath = "assets/images/doctors/$filename"
            $script:docCounter++
        }
        elseif ($contextHint -match "banner" -or $url -match "w=1200" -or $url -match "w=800") {
            $filename = "banner_$bannerCounter.jpg"
            $localPath = Join-Path $bannersDir $filename
            $urlPath = "assets/images/banners/$filename"
            $script:bannerCounter++
        }
        else {
            $filename = "icon_$iconCounter.jpg"
            $localPath = Join-Path $iconsDir $filename
            $urlPath = "assets/images/icons/$filename"
            $script:iconCounter++
        }
        
        Invoke-WebRequest -Uri $url -OutFile $localPath -ErrorAction Stop
        $downloaded[$url] = $urlPath
        return $urlPath
    }
    catch {
        Write-Host "Failed to download $url : $_"
        return $url
    }
}

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    
    # Simple regex for finding img sources
    $imgRegex = [regex]'(?i)<img[^>]+src=["''](http[^"'']+)["'']'
    $matches = $imgRegex.Matches($content)
    
    foreach ($m in $matches) {
        $url = $m.Groups[1].Value
        $context = ""
        if ($url -match "w=300" -or $url -match "w=150") { $context = "doctor" }
        elseif ($url -match "w=1200") { $context = "banner" }
        
        $localUrl = Download-And-Get-Local-Path -url $url -contextHint $context
        $content = $content.Replace($url, $localUrl)
    }
    
    # Finding CSS background sources in inline styles
    $cssRegex = [regex]'(?i)(https://images\.unsplash\.com/[^\s"'',\)]+)'
    $matchesCss = $cssRegex.Matches($content)
    
    foreach ($m in $matchesCss) {
        $url = $m.Groups[1].Value
        $context = ""
        if ($url -match "w=1200") { $context = "banner" }
        
        $localUrl = Download-And-Get-Local-Path -url $url -contextHint $context
        $content = $content.Replace($url, $localUrl)
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        Write-Host "Updated $($file.Name)"
    }
}

foreach ($file in $cssFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    
    $cssRegex = [regex]'(?i)(https://images\.unsplash\.com/[^\s"'',\)]+)'
    $matchesCss = $cssRegex.Matches($content)
    
    foreach ($m in $matchesCss) {
        $url = $m.Groups[1].Value
        $context = "banner"
        
        $localUrl = Download-And-Get-Local-Path -url $url -contextHint $context
        $content = $content.Replace($url, $localUrl)
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        Write-Host "Updated $($file.Name)"
    }
}

Write-Host "Asset replacement complete."
