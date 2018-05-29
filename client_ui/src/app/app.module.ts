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
import {FormsModule} from "@angular/forms";
import {ForbiddenValidatorDirective} from "./shared/forbidden-name.directive";
import {CookieService} from "ngx-cookie-service";
import { UserPreferencesComponent } from './user-preferences/user-preferences.component';
import {TagInputModule} from "ngx-chips";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {UserService} from "./user.service";
import {PrefService} from "./pref.service";
import {Ng4LoadingSpinnerModule, Ng4LoadingSpinnerService} from "ng4-loading-spinner";
import {NgxSmartModalModule, NgxSmartModalService} from "ngx-smart-modal";


const myRoots: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  // {
  //   path: 'preferences',
  //   component: UserPreferencesComponent
  // }
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
    UserPreferencesComponent,
  ],
  imports: [
    BrowserModule,
    NgxSmartModalModule.forRoot(),
    BrowserAnimationsModule,
    RouterModule.forRoot(myRoots),
    HttpClientModule,
    FormsModule,
    Ng4LoadingSpinnerModule.forRoot(),
    TagInputModule
  ],
  exports: [
  ],
  providers: [
    ChannelService,
    CookieService,
    NgxSmartModalService,
    PrefService,
    Ng4LoadingSpinnerService,
    UserService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {

}
