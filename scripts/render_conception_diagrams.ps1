param([string]$DiagramDirectory = (Join-Path $PSScriptRoot '..\docs\diagrammes'))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
function Get-Color([string]$Value) { return [System.Drawing.ColorTranslator]::FromHtml($Value) }
foreach ($diagramFile in Get-ChildItem -LiteralPath $DiagramDirectory -Filter '*.json') {
    $diagram = Get-Content -Raw -Encoding utf8 -LiteralPath $diagramFile.FullName | ConvertFrom-Json
    $bitmap = [System.Drawing.Bitmap]::new([int]($diagram.width * 2), [int]($diagram.height * 2))
    $bitmap.SetResolution(240, 240)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.Clear([System.Drawing.Color]::White)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.ScaleTransform(2, 2)
    foreach ($shape in $diagram.shapes) {
        if ($shape.type -in @('rect','ellipse')) {
            $brush = [System.Drawing.SolidBrush]::new((Get-Color $shape.fill))
            $pen = [System.Drawing.Pen]::new((Get-Color $shape.stroke), 2)
            $rect = [System.Drawing.RectangleF]::new($shape.x, $shape.y, $shape.w, $shape.h)
            if ($shape.type -eq 'rect') { $graphics.FillRectangle($brush, $rect); $graphics.DrawRectangle($pen, $shape.x, $shape.y, $shape.w, $shape.h) }
            else { $graphics.FillEllipse($brush, $rect); $graphics.DrawEllipse($pen, $rect) }
            $brush.Dispose(); $pen.Dispose()
        } elseif ($shape.type -eq 'text') {
            $fontStyle = if ($shape.bold) { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
            $font = [System.Drawing.Font]::new('Arial', [float]$shape.size, $fontStyle, [System.Drawing.GraphicsUnit]::Pixel)
            $brush = [System.Drawing.SolidBrush]::new((Get-Color $shape.color))
            $format = [System.Drawing.StringFormat]::new()
            $format.LineAlignment = [System.Drawing.StringAlignment]::Center
            $format.Alignment = if ($shape.align -eq 'center') { [System.Drawing.StringAlignment]::Center } else { [System.Drawing.StringAlignment]::Near }
            $format.FormatFlags = [System.Drawing.StringFormatFlags]::NoWrap
            $graphics.DrawString($shape.text, $font, $brush, [System.Drawing.RectangleF]::new($shape.x, $shape.y, $shape.w, $shape.h), $format)
            $font.Dispose(); $brush.Dispose(); $format.Dispose()
        } elseif ($shape.type -eq 'line') {
            $pen = [System.Drawing.Pen]::new((Get-Color $shape.color), 2)
            if ($shape.dash) { $pen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash }
            $points = @($shape.points | ForEach-Object { [System.Drawing.PointF]::new([float]$_[0], [float]$_[1]) })
            $graphics.DrawLines($pen, [System.Drawing.PointF[]]$points)
            if ($shape.arrow -or $shape.hollow) {
                $a = $shape.points[-2]; $b = $shape.points[-1]
                $angle = [Math]::Atan2(($b[1]-$a[1]), ($b[0]-$a[0]))
                $length = if ($shape.hollow) { 20 } else { 13 }
                $tip = [System.Drawing.PointF[]]@(
                    [System.Drawing.PointF]::new($b[0], $b[1]),
                    [System.Drawing.PointF]::new(($b[0]-$length*[Math]::Cos($angle)+$length*.45*[Math]::Sin($angle)), ($b[1]-$length*[Math]::Sin($angle)-$length*.45*[Math]::Cos($angle))),
                    [System.Drawing.PointF]::new(($b[0]-$length*[Math]::Cos($angle)-$length*.45*[Math]::Sin($angle)), ($b[1]-$length*[Math]::Sin($angle)+$length*.45*[Math]::Cos($angle)))
                )
                $brush = [System.Drawing.SolidBrush]::new($(if ($shape.hollow) { [System.Drawing.Color]::White } else { Get-Color $shape.color }))
                $graphics.FillPolygon($brush, $tip); $graphics.DrawPolygon($pen, $tip)
                $brush.Dispose()
            }
            $pen.Dispose()
        }
    }
    $outputPath = [System.IO.Path]::ChangeExtension($diagramFile.FullName, '.png')
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose(); $bitmap.Dispose()
    Write-Output "Rendered $([System.IO.Path]::GetFileName($outputPath))"
}
