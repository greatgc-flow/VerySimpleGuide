# Windows PowerShell 2.0 syntax; compatible with 5.x.
# Python validator mirrors every line of its stdout to EvidenceFile (UTF-8).
# If Python cannot even start, emit the startup error without writing files.
param(
    [string]$Python = "python",
    [string]$EvidenceFile = ".validation\validation_evidence.txt"
)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Command = Get-Command $Python -ErrorAction SilentlyContinue
if ($Command -eq $null) {
    $Line = "ERROR=python-executable-not-found:$Python"
    Write-Output $Line
    exit 1
}
& $Python (Join-Path $ScriptDir "validate_package.py") --evidence-file $EvidenceFile
$Code = $LASTEXITCODE
if ($Code -eq $null) { $Code = 1 }
exit $Code
