param(
    [Parameter(Mandatory = $true)][string]$appName
)

$body = ConvertTo-Json @{ app_name = $appName }
$uri = 'https://scoop.zhoujin7.com/search'
$queryResult = Invoke-RestMethod -URI $uri -Method Post -ContentType 'application/json' -Body $body
Write-Output $queryResult
