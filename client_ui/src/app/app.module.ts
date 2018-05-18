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
import { UserPreferencesComponent } from './user-preferences/user-preferences.component';
import {TagInputModule} from "ngx-chips";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {UserService} from "./user.service";
import {PrefService} from "./pref.service";


const myRoots: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'preferences',
    component: UserPreferencesComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    HomeComponent,
    JumbotronComponent,
    HomeInfoComponent,
    ChannelComponent,
    ForbiddenValidatorDirective,
    UserPreferencesComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    RouterModule.forRoot(myRoots),
    HttpClientModule,
    FormsModule,
    TagInputModule
  ],
  exports: [
  ],
  providers: [
    ChannelService,
    LoginService,
    CookieService,
    PrefService,
    UserService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  // static loginService: LoginService;
  //
  // static getLoginService() {
  //   return this.loginService;
  // }
}
