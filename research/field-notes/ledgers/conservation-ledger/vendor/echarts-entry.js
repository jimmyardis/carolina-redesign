// Only what the Conservation Ledger page actually draws: bar and line series,
// a category/value grid, tooltips, legend, title and series labels. Everything
// else in echarts (maps, graphs, 3D, candlestick, dataset, toolbox...) is left
// out, which is most of it.
import * as echarts from 'echarts/core';
import { BarChart, LineChart } from 'echarts/charts';
import {
  GridComponent, TooltipComponent, LegendComponent, TitleComponent,
  AxisPointerComponent,
} from 'echarts/components';
import { LabelLayout } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  BarChart, LineChart,
  GridComponent, TooltipComponent, LegendComponent, TitleComponent,
  AxisPointerComponent, LabelLayout, CanvasRenderer,
]);
window.echarts = echarts;
