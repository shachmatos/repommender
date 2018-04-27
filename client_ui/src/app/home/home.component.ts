import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Config} from "../config";
import {FormsModule, FormControl, FormGroup, FormBuilder} from "@angular/forms";
import {LoginService} from "../login.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  providers: [ FormsModule ]
})
export class HomeComponent implements OnInit {
  authenticated : boolean = false;
  actionUrl : string = "https://github.com/login/oauth/authorize?client_id=" + Config.repommender_config.github_client_id + "&allow_signup=true";
  actionText : string = "Login with Github";


  @Output() onAuthentication : EventEmitter<any> = new EventEmitter<any>();

  constructor(private loginService : LoginService, private route: ActivatedRoute) {

  }

  ngOnInit() {
    if (this.loginService.getUser() != null) this.authenticated = true;
    // this.loginService.checkLogin();
    this.loginService.tokenValidated.subscribe(status => {this.onLoginStatusChange(status);});
    this.loginService.loginStatusChange.subscribe(status => {this.onLoginStatusChange(status);});
  }

  private onLoginSuccess() {
    this.authenticated = true;
  }

  private onLogout() {
    this.authenticated = false;
  }

  private onLoginStatusChange(status: boolean) {
    this.authenticated = status;
  }

  setAuthenticated(val: boolean) {
    this.authenticated = val;
    this.onAuthentication.emit(val);
  }

}
