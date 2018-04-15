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

  testName: number;


  @Output() onAuthentication : EventEmitter<any> = new EventEmitter<any>();

  constructor(private loginService : LoginService, private route: ActivatedRoute) {
    this.loginService.loginStatusChange.subscribe(val => {
      this.authenticated = val;
    });
  }

  ngOnInit() {
    if (this.loginService.checkLogin()) {
      this.authenticated = true;
    } else {
      this.route.queryParams.subscribe(params => {
        if (params['code']) {
          this.loginService.login(params['code']);
        }
      });
    }
    // this.authenticated = true;
  }

  setAuthenticated(val: boolean) {
    this.authenticated = val;
    this.onAuthentication.emit(val);
  }

  checkToken() {

  }

}
