import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Config} from "../config";
import {FormsModule, FormControl, FormGroup, FormBuilder} from "@angular/forms";
import {UserService} from "../user.service";
import {ActivatedRoute} from "@angular/router";
import {Ng4LoadingSpinnerService} from "ng4-loading-spinner";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  providers: [ FormsModule ]
})
export class HomeComponent implements OnInit {
  authenticated : boolean = false;
  loading : boolean = true;
  actionUrl : string = "https://github.com/login/oauth/authorize?client_id=" + Config.repommender_config.github_client_id + "&allow_signup=true";
  actionText : string = "Login with Github";


  @Output() onAuthentication : EventEmitter<any> = new EventEmitter<any>();

  constructor(private userService : UserService, private route: ActivatedRoute, private spinner: Ng4LoadingSpinnerService, private cookies: CookieService) {

  }

  ngOnInit() {
    this.spinner.show();
    if (this.userService.getUser() != null) {
      this.authenticated = true;
      this.loading = false;
      this.spinner.hide();
    }

    if (!this.cookies.check('access_token')) {
      this.loading = false;
      this.spinner.hide();
    }

    // this.loginService.checkLogin();
    this.userService.tokenValidated.subscribe(status => {this.onLoginStatusChange(status);});
    this.userService.loginStatusChange.subscribe(status => {this.onLoginStatusChange(status);});
  }

  private onLoginSuccess() {
    this.authenticated = true;
  }

  private onLogout() {
    this.authenticated = false;
  }

  private onLoginStatusChange(status: boolean) {
    this.authenticated = status;
    this.loading = false;
    this.spinner.hide();
  }
}
