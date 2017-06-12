import { Component, OnInit } from '@angular/core';
import * as $ from 'jquery';

import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(public router: Router) { }

  ngOnInit() {
    const $page = $('.full-page');
    const image_src = $page.data('image');
    const image_container = '<div class="full-page-background" style="background-image: url(' + image_src + ') "></div>'
    $('.full-page').append(image_container);
    setTimeout(function() {
     $('.card').removeClass('card-hidden');
     }, 300);
  }

  login() {
    window.localStorage.setItem('currentUser', 'jg');
    this.router.navigate(['']);
  }

}
