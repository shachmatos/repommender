import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from './app.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { HomeComponent } from './home/home.component';
import { JumbotronComponent } from './jumbotron/jumbotron.component';
import { HomeInfoComponent } from './home-info/home-info.component';
import { ChannelComponent } from './channel/channel.component';
import { ChannelService } from "./channel.service";
import { HttpClientModule } from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {ForbiddenValidatorDirective} from "./shared/forbidden-name.directive";
import {LoginService} from "./login.service";
import {CookieService} from "ngx-cookie-service";


const myRoots: Routes = [{
  path: '',
  component: HomeComponent
}];

@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    HomeComponent,
    JumbotronComponent,
    HomeInfoComponent,
    ChannelComponent,
    ForbiddenValidatorDirective
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(myRoots),
    HttpClientModule,
    FormsModule,
  ],
  exports: [
  ],
  providers: [
    ChannelService,
    LoginService,
    CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  test : string = "hello";
}
