# graspgraph
Create easy-to-understand graphs

## Concept
Make it easier to understand with graphs

### Stats
![](./images/stats/usage.png)

### Database ER diagram-like
![](./images/dber/usage.png)

### Comparison
![](./images/compe/usage.png)

## What is possible
### statsgraph
1. Graphing statistics

### dbergraph
1. Graphing database table definition information

### compegraph
1. Graphing the comparison

## Reason for development
- I want to make things that are difficult to understand through text alone easier to understand by creating graphs

## Versions

|Version|Summary|
|:--|:--|
|0.3.0|Add compegraph|
|0.2.5|Refactoring|
|0.2.4|Add dbergraph|
|0.1.0|Release graspgraph(statsgraph)|

## Installation
### [graspgraph](https://pypi.org/project/graspgraph/)
`pip install graspgraph`

### [Graphviz](https://graphviz.org/download/)
Required for PDF output

### [Poppler](https://github.com/Belval/pdf2image?tab=readme-ov-file)
Required for PDF image conversion

## Usage
### statsgraph
![](./images/stats/usage.png)
```python
import graspgraph as gg

statsgraph = gg.Statsgraph(
  gg.StatsgraphAxis([1, 2, 3, 4, 5]),
  gg.StatsgraphAxis([11, 12, 13, 14, 15]),
  gg.FigureColors(line = "blue"))
figure = statsgraph.to_figure()
figure.LayoutTitleText = "<b>[statsgraph]<br>タイトル</b>"
figure.XTitleText = "X軸"
figure.YTitleText = "Y軸"
figure.Write("./statsgraph.png")
```

### dbergraph
![](./images/dber/usage.png)
```python
import graspgraph as gg

prefix = "./database"
dbergraph = gg.Dbergraph(gg.Database.from_file_path(gg.Path.join(prefix, "yaml")))
dbergraph.Database.update()
dot = dbergraph.to_dot()
dot.TitleText = "<b>[dbergraph]</b>"
pdfFilePath = gg.Path.join(prefix, "pdf")
pngFilePath = gg.Path.join(prefix, "png")
dot.Write(pdfFilePath)
gg.Pdf.convert(pdfFilePath, pngFilePath)
```

### compegraph
![](./images/compe/usage.png)
```python
import graspgraph as gg

compegraph = gg.Compegraph(
  gg.CompegraphAxis(["1月", "2月", "3月"], [
    gg.CompegraphBar("収入", [1, 2, 3]),
    gg.CompegraphBar("支出", [-1, -2.5, -2]),
    gg.CompegraphBar("利益", [0, -0.5, 1]),
  ], gg.FigureTick(2)),
  gg.CompegraphColors(bars = ["blue", "red", "yellow"]))
figure = compegraph.to_figure()
figure.LayoutTitleText = "<b>[compegraph]</b>"
figure.XTitleText = "金額(百万円)"
figure.YTitleText = "月次"
figure.Write("./compegraph.png")
```

## CLI
### pdf.convert
Convert PDF to image

#### 1. Image(PNG) conversion by CLI execution

```
pdf.convert # <pdf file path> <image file path>
```
`graspgraph pdf.convert graph.pdf graph.png`
```
graph.png is done.
```
