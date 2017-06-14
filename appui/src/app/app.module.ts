import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { LockscreenComponent } from './lockscreen/lockscreen.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MapsComponent } from './maps/maps.component';
import { TimelineComponent } from './timeline/timeline.component';
import { DiseasesComponent } from './diseases/diseases.component';
import { PushsComponent } from './pushs/pushs.component';
import { MainComponent } from './main/main.component';
import { HomeComponent } from './home/home.component';
import { routing } from './app.routing';
import { AuthService } from './auth.service';
// import { SweetAlertService } from 'ng2-sweetalert2';

import {ChartistModule} from 'ng-chartist';
import { SidemenuComponent } from './sidemenu/sidemenu.component';
import { TopbarComponent } from './topbar/topbar.component';
import { FixedpluginComponent } from './fixedplugin/fixedplugin.component';
import { UtilComponent } from './util/util.component';

import { AgmCoreModule } from '@agm/core';
import { FooterComponent } from './footer/footer.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    LockscreenComponent,
    DashboardComponent,
    MapsComponent,
    TimelineComponent,
    DiseasesComponent,
    PushsComponent,
    MainComponent,
    HomeComponent,
    SidemenuComponent,
    TopbarComponent,
    FixedpluginComponent,
    UtilComponent,
    FooterComponent,
    // SweetAlertService
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    routing,
    ChartistModule,
    AgmCoreModule.forRoot()
    // SweetAlertService
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
