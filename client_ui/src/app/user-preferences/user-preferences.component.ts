import { Component, OnInit } from '@angular/core';
import {LoginService} from "../login.service";
import {Router} from "@angular/router";
import {UserService} from "../user.service";
import {User} from "../user";
import {PrefService} from "../pref.service";

@Component({
  selector: 'app-user-preferences',
  templateUrl: './user-preferences.component.html',
  styleUrls: ['./user-preferences.component.scss']
})
export class UserPreferencesComponent implements OnInit {

  topics: Array<string> = [];
  languages: Array<string> = [];
  user: User = null;

  constructor(private loginService: LoginService, private userService: UserService, private router: Router, private prefService: PrefService) { }

  ngOnInit() {
    this.loginService.tokenValidated.subscribe(val => { this.onTokenValidated()});
    this.loginService.loginFailed.subscribe(val => { this.onLoginFailed()});
    this.loginService.loginStatusChange.subscribe(val => { if (!val) this.onLogout()});
    this.loginService.userChanged.subscribe(user => { this.onUserCHanged(user)});
    this.prefService.getTopics().subscribe(data => { this.onGetTopics(data) });
    this.prefService.getLanguages().subscribe( data => { this.onGetLanguages(data)});
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

  private onGetTopics(data: any) {
    this.topics = [];
    for (let item of data) {
      this.topics.push(item.pk);
    }
  }

  private onGetLanguages(data: any) {
    this.languages = [];
    for (let item of data) {
      this.languages.push(item.pk);
    }
  }
}
