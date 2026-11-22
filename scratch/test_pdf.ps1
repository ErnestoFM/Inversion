try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    Write-Output "Word COM is available: $($word.Version)"
    $word.Quit()
} catch {
    Write-Output "Word COM failed: $_"
}
