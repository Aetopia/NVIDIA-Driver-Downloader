# Made by Aetopia.
# Ported NVIDIA Driver Downloader Functions: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/legacy/nvddl.py

function Get-NVIDIADriver {
    <#
        .SYNOPSIS
        Get all available driver versions.
    #>
    param (
        [switch]$Studio
    )
    $GameReadyVersions = @()
    $File = (Invoke-WebRequest 'https://www.nvidia.com/Download/processFind.aspx?psid=101&pfid=845&osid=57&lid=1&whql=1&ctk=0&dtcid=1').RawContent
    foreach ($Line in $File.Split('`n')){
        if ($Line -match "<td class=""gridItem"">*.*</td>") {
            $Version = $Line.Split('>')[5].Split('<')[0]
            $GameReadyVersions += $Version 
        }
    }
    if ($Studio.IsPresent -eq $true) {
        $StudioVersions = @()
        foreach ($Version in $GameReadyVersions) {
            try {
                $DriverLink = "https://international.download.nvidia.com/Windows/$Version/$Version-desktop-win10-win11-64bit-international-nsd-dch-whql.exe"
                $StatusCode = (Invoke-WebRequest -Uri "$DriverLink" -DisableKeepAlive -Method Head).StatusCode
                if ($StatusCode -eq 200){$StudioVersions += $Version}
            }
            catch {}
        }
        return $StudioVersions
    }
    else {return $GameReadyVersions}
}

function Invoke-NVIDIADriver {
    <#
        .SYNOPSIS
        Download an NVIDIA driver package.
    #>
    param (
        [string]$Version = 'Latest',
        [switch]$Studio,
        [switch]$Minimal
    )
    $Components = @("Display.Driver", 
                    "NVI2", 
                    "EULA.txt", 
                    "ListDevices.txt", 
                    "GFExperience/*.txt", 
                    "GFExperience/locales", 
                    "GFExperience/EULA.html", 
                    "GFExperience/PrivacyPolicy", 
                    "setup.cfg", 
                    "setup.exe") -join " "
    if ($Version.ToLower() -eq 'latest') {
        if ($Studio.IsPresent -eq $true) {$Version = (Get-NVIDIADriver -Studio)[0]}
        else {$Version = (Get-NVIDIADriver)[0]}
    } 
    if ($Studio.IsPresent -eq $True) {
        $Type = "Studio"
        $DriverLink = "https://international.download.nvidia.com/Windows/$Version/$Version-desktop-win10-win11-64bit-international-nsd-dch-whql.exe" 
    }
    else {
        $Type = "Game Ready"
        $DriverLink = "https://international.download.nvidia.com/Windows/$Version/$Version-desktop-win10-win11-64bit-international-dch-whql.exe"
    }    
    Write-Output "Checking Download..."
    try {$StatusCode = (Invoke-WebRequest -Uri "$DriverLink" -DisableKeepAlive -Method Head).StatusCode}
    catch {$StatusCode = 0}
    if ($StatusCode -eq 200) {
        Write-Output "Downloading ($Type - $Version)..."
        curl.exe -# "$DriverLink" -o "$env:TEMP/$Type - $Version.exe" 
        if ($Minimal.IsPresent -eq $true) {
            Write-Output "Looking for (7z.exe)..."
            $7Zip = @((Get-ChildItem -Path "C:\*7z.exe" -Recurse -Force -ErrorAction 'silentlycontinue').FullName)[0]
            if ($7Zip -eq @()) {
                Write-Output 'Please install 7-Zip!'
            }
            else {
                Write-Output "Unpacking driver package with minimal components..."
                cmd /c """$7Zip"" x -bso0 -bsp1 -bse1 -aoa ""$env:TEMP/$Type - $Version.exe"" $Components -o""$env:TEMP/$Type - $Version"""
                Write-Output "Unpacked ($Type - $Version)!"
                try {Start-Process "$env:TEMP/$Type - $Version/setup.exe" -ErrorAction 'silentlycontinue'}
                catch {}
            }
        }
        else {
            try {Start-Process "$env:TEMP/$Type - $Version.exe" -erroraction 'silentlycontinue'}
            catch {}
            }

    }        
    else {Write-Output "Version is invaild!"}
} 

# CLI
if ($args[0] -eq $null) {
    Write-Output "NVIDIA Driver Downloader Help:

-List [-Studio] 
> Show all available driver versions.

-Download [<Driver Version> -Studio -Minimal] 
> Download the latest driver or a specified driver version.
"    
}
elseif ($args[0].ToLower() -in @('-d', '-download')) {
    try {
        if (!($args[1] -in @('-minimal', '-studio'))) {$args[1] = '-Version ' + $args[1]}
    }
    catch {} 
    Invoke-Expression ("Invoke-NVIDIADriver " + $args[1]+ " " + $args[2] + " " + $args[3])
}
elseif ($args[0].ToLower() -in @('-ls', '-list')){
    if ($args[1] -ne $null -and $args[1].ToLower() -eq '-studio') {Write-Output "Looking for Studio Drivers..."}
    else {Write-Output "Looking for Game Ready Drivers..."}
    Invoke-Expression ("Get-NVIDIADriver "+ $args[1])
} 