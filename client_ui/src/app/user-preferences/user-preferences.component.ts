import { Component, OnInit } from '@angular/core';
import {LoginService} from "../login.service";
import {Router} from "@angular/router";
import {UserService} from "../user.service";
import {User} from "../user";

@Component({
  selector: 'app-user-preferences',
  templateUrl: './user-preferences.component.html',
  styleUrls: ['./user-preferences.component.scss']
})
export class UserPreferencesComponent implements OnInit {

  user: User = null;

  constructor(private loginService: LoginService, private userService: UserService, private router: Router) { }

  ngOnInit() {
    this.loginService.tokenValidated.subscribe(val => { this.onTokenValidated()});
    this.loginService.loginFailed.subscribe(val => { this.onLoginFailed()});
    this.loginService.loginStatusChange.subscribe(val => { if (!val) this.onLogout()});
    this.loginService.userChanged.subscribe(user => { this.onUserCHanged(user)});
  }

  private onUserCHanged(newUser: User) {
    this.user = newUser;
  }

  private onLogout() {
    this.router.navigate(['']);
  }

  private onLoginFailed() {
    this.router.navigate(['']);
  }

  private onTokenValidated() {

  }

}
