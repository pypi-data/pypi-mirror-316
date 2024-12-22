from .figure import *

class CompegraphBar:
  def __init__(self, name, values):
    self.Name = name
    self.Values = values

class CompegraphAxis:
  def __init__(self, names, bars, tick = None):
    self.Names = names
    self.Bars = bars
    if tick is None:
      tick = FigureTick()
    self.Tick = tick

class CompegraphColors:
  def __init__(self, layoutTitle = "black", xTitle = "black", yTitle = "black", grid = "gray", background = "white", bars = []):
    self.LayoutTitle = layoutTitle
    self.XTitle = xTitle
    self.YTitle = yTitle
    self.Grid = grid
    self.Background = background
    self.Bars = bars

  def bar(self, index = 0):
    if index < len(self.Bars):
      return self.Bars[index]
    return None

class Compegraph:
  def __init__(self, axis, colors = None):
    self.Axis = axis
    if colors is None:
      colors = CompegraphColors()
    self.Colors = colors

  def to_figure(self):
    figure = Figure()
    for i, bar in enumerate(self.Axis.Bars):
      barColor = self.Colors.bar(i)
      figure.add_trace(pgo.Bar(showlegend = True, name = bar.Name, x = bar.Values, y = self.Axis.Names, marker_color = barColor, textfont = dict(size = 24, color = barColor)))
    figure.update_traces(orientation = "h", textposition = "outside", texttemplate = " %{x:} ")
    figure.update_xaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, tickformat = self.Axis.Tick.Format, dtick = self.Axis.Tick.Dtick, linecolor = self.Colors.Grid, linewidth = 3, gridcolor = self.Colors.Grid, griddash = "dot", mirror = True)
    figure.update_yaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, linecolor = self.Colors.Grid, linewidth = 3, mirror = True, autorange = "reversed")
    figure.update_layout(title = dict(text = "", font = dict(color = self.Colors.LayoutTitle, size = 26), x = 0.5),
      xaxis = dict(title = "", color = self.Colors.XTitle),
      yaxis = dict(title = "", color = self.Colors.YTitle),
      legend = dict(orientation = "h", xanchor = "right", x = 1, yanchor = "bottom", y = 1.01, font = dict(size = 20, color = self.Colors.YTitle)),
      font = dict(size = 20),
      paper_bgcolor = self.Colors.Background, plot_bgcolor = self.Colors.Background)
    return figure
