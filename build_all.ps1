
Get-ChildItem -Path . -Recurse -Filter 'build_docker.ps1' | ForEach-Object {
    $scriptPath = $_.FullName
    $scriptDirectory = Split-Path -Path $scriptPath -Parent
    Write-Host "Executing $scriptPath in directory $scriptDirectory..."
    Push-Location -Path $scriptDirectory

    # Execute the build_docker.ps1 script in its own directory
    & .\build_docker.ps1

    Pop-Location
}