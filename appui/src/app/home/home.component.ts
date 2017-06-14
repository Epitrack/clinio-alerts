import {Component, OnInit} from '@angular/core';
import * as jQuery from 'jquery';
import * as Chartist from 'chartist';
import {UtilComponent} from '../util/util.component';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent extends UtilComponent implements OnInit {


  seq2 = 0;
  delays2 = 80;
  durations2 = 500;

  constructor() {
    super();
  }

  ngOnInit() {
    this.salesGraph();
    this.initCharts();
    this.initMap();
  }

  salesGraph() {
    const dataDailySalesChart = {
      labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
      series: [
        [12, 17, 7, 17, 23, 18, 38]
      ]
    };

    const optionsDailySalesChart = {
      lineSmooth: Chartist.Interpolation.cardinal({
        tension: 0
      }),
      low: 0,
      high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
      chartPadding: {top: 0, right: 0, bottom: 0, left: 0},
    }

    const dailySalesChart = new Chartist.Line('#dailySalesChart', dataDailySalesChart, optionsDailySalesChart);
    this.startAnimationForLineChart(dailySalesChart);
  }

  initCharts() {
    const dataCompletedTasksChart = {
      labels: ['12p', '3p', '6p', '9p', '12p', '3a', '6a', '9a'],
      series: [
        [230, 750, 450, 300, 280, 240, 200, 190]
      ]
    };

    const optionsCompletedTasksChart = {
      lineSmooth: Chartist.Interpolation.cardinal({
        tension: 0
      }),
      low: 0,
      high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
      chartPadding: { top: 0, right: 0, bottom: 0, left: 0}
    }

    const completedTasksChart = new Chartist.Line('#completedTasksChart', dataCompletedTasksChart, optionsCompletedTasksChart);

    // start animation for the Completed Tasks Chart - Line Chart
    this.startAnimationForLineChart(completedTasksChart);
  }

  initMap() {
    // // Regular Map
    // let myLatlng = new google.maps.LatLng(40.748817, -73.985428);
    // let mapOptions = {
    //   zoom: 8,
    //   center: myLatlng,
    //   scrollwheel: false,
    // }
    //
    // let map = new google.maps.Map(document.getElementById("regularMap"), mapOptions);
    //
    // let marker = new google.maps.Marker({
    //   position: myLatlng,
    //   title:"Regular Map!"
    // });
    //
    // marker.setMap(map);
    //
    //
    // // Custom Skin & Settings Map
    //  myLatlng = new google.maps.LatLng(40.748817, -73.985428);
    //  mapOptions = {
    //   zoom: 13,
    //   center: myLatlng,
    //   scrollwheel: false,
    //   disableDefaultUI: true,
    //   zoomControl: true,
    //   styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]
    //
    // }
    //
    // map = new google.maps.Map(document.getElementById("customSkinMap"), mapOptions);
    //
    // marker = new google.maps.Marker({
    //   position: myLatlng,
    //   title:"Custom Skin & Settings Map!"
    // });
    //
    // marker.setMap(map);
    //
    // // Satellite Map
    //  myLatlng = new google.maps.LatLng(40.748817, -73.985428);
    //  mapOptions = {
    //   zoom: 3,
    //   scrollwheel: false,
    //   center: myLatlng,
    //   mapTypeId: google.maps.MapTypeId.SATELLITE
    // }
    //
    //  map = new google.maps.Map(document.getElementById("satelliteMap"), mapOptions);
    //
    //  marker = new google.maps.Marker({
    //   position: myLatlng,
    //   title:"Satellite Map!"
    // });
    //
    // marker.setMap(map);
  }

}

