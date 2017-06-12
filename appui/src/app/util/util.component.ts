import { Component, OnInit } from '@angular/core';
import * as Chartist from 'chartist';

@Component({templateUrl: 'util.component.html'})
export class UtilComponent {

  constructor() { }

  startAnimationForLineChart(chart) {
    let seq = 0;
    const delays = 80;
    const durations = 500;
    chart.on('draw', (data) => {
      if (data.type === 'line' || data.type === 'area') {
        data.element.animate({
          d: {
            begin: 600,
            dur: 700,
            from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
            to: data.path.clone().stringify(),
            easing: Chartist.Svg.Easing.easeOutQuint
          }
        });
      } else if (data.type === 'point') {
        seq++;
        data.element.animate({
          opacity: {
            begin: seq * delays,
            dur: durations,
            from: 0,
            to: 1,
            easing: 'ease'
          }
        });
      }
    });
  }
}
