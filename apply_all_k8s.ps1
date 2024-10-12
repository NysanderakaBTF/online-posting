$basePath = ".\"

Get-ChildItem -Path $basePath -Directory | ForEach-Object {
    $folderPath = $_.FullName
    Get-ChildItem -Path $folderPath -Filter *.yaml | ForEach-Object {
        $yamlFile = $_.FullName
        kubectl apply -f $yamlFile
    }
}