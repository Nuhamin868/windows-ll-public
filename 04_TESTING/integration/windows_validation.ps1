$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$exe = Join-Path $root 'build/windows/windows_ll.exe'
$data = Join-Path $root '04_TESTING/test_data'
function Invoke-Program([string]$Program, [string[]]$Arguments, [bool]$Success) {
    $prior = $ErrorActionPreference
    try {
        # Native stderr is diagnostic data, including on successful commands.
        $ErrorActionPreference = 'Continue'
        $lines = & $Program @Arguments 2>&1
        $code = $LASTEXITCODE
    } finally { $ErrorActionPreference = $prior }
    $lines | ForEach-Object { Write-Output $_.ToString() }
    if (($code -eq 0) -ne $Success) { throw "Unexpected exit $code for $Arguments" }
}
function Invoke-Case([string[]]$Arguments, [bool]$Success) {
    Invoke-Program $exe $Arguments $Success
}
Push-Location $root
try {
    Invoke-Program (Join-Path $root 'build/windows/winll_unit.exe') @($data) $true
    Invoke-Program (Join-Path $root 'build/windows/winll_windows_unit.exe') @($data) $true
    Invoke-Case @('hash') $true
    Invoke-Case @('metadata','space argument','λ') $true
    Invoke-Case @('processes','windows_ll') $true
    Invoke-Case @('pe',$exe) $true
    Invoke-Case @('artifact',"$data/artifact.bin","$data/test-key.bin") $true
    foreach ($bad in @('bad-tag.bin','bad-schema.bin','truncated-artifact.bin')) {
        Invoke-Case @('artifact',"$data/$bad","$data/test-key.bin") $false
    }
    Invoke-Case @('artifact',"$data/artifact.bin","$data/wrong-key.bin") $false
    Invoke-Case @('https','http://example.invalid/x','example.invalid',"$data/test-key.bin") $false
    Invoke-Case @('https','https://other.invalid/x','example.invalid',"$data/test-key.bin") $false
    Invoke-Case @('https','https://example.invalid:444/x','example.invalid',"$data/test-key.bin") $false
    Invoke-Case @('unknown') $false
    Invoke-Case @('pe',"$data/bad_mz.bin") $false
    # Pre-existing test keys are never overwritten.
    $key='HKCU:\Software\WindowsLL\TestArtifacts'
    if (Test-Path $key) { throw 'Registry test key already exists; isolate test account before running.' }
    try {
        New-Item -Path $key -Force | Out-Null
        New-ItemProperty -Path $key -Name Data -PropertyType Binary -Value ([IO.File]::ReadAllBytes("$data/artifact.bin")) | Out-Null
        Invoke-Case @('registry',"$data/test-key.bin") $true
        Set-ItemProperty -Path $key -Name Data -Value ([byte[]]::new(1048577))
        Invoke-Case @('registry',"$data/test-key.bin") $false
        Remove-ItemProperty -Path $key -Name Data
        New-ItemProperty -Path $key -Name Data -PropertyType String -Value 'inert' | Out-Null
        Invoke-Case @('registry',"$data/test-key.bin") $false
        Remove-ItemProperty -Path $key -Name Data
        Invoke-Case @('registry',"$data/test-key.bin") $false
    } finally { if (Test-Path $key) { Remove-Item $key } }
    $log=Join-Path $root '08_EVIDENCE/test_logs/mutex-holder.log'
    $holder=Start-Process -FilePath $exe -ArgumentList @('hold','10000') -PassThru -RedirectStandardError $log
    try {
        $ready=$false
        for($i=0;$i -lt 50;$i++) {
            if ((Test-Path $log) -and ((Get-Content $log -Raw) -match 'acquired')) {$ready=$true;break}
            if ($holder.HasExited) {throw 'Mutex holder exited early'}
            Start-Sleep -Milliseconds 100
        }
        if (-not $ready) { throw 'Mutex readiness timed out' }
        Invoke-Case @('hash') $false
    } finally { if (-not $holder.HasExited) { Stop-Process -Id $holder.Id; $holder.WaitForExit() } }
    Invoke-Case @('hash') $true
    Write-Output 'PASS Windows offline integration cases'
} finally { Pop-Location }
# Live HTTPS success, certificate rejection, redirect denial, timeout and oversized
# responses need a controlled, trusted TLS endpoint. See TEST_PLAN.md; not claimed here.
