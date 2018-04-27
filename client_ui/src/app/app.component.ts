import {Component, OnInit} from '@angular/core';
import {LoginService} from "./login.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'Repommender';

  constructor(private loginService: LoginService) {}

  ngOnInit(): void {
    this.loginService.checkLogin();
  }


}
