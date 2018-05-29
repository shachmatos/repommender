import {AfterViewInit, Component, OnInit} from '@angular/core';
import {UserService} from "./user.service";
import {NgxSmartModalService} from "ngx-smart-modal";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewInit{
  title = 'Repommender';

  constructor(private userService: UserService, public modalService: NgxSmartModalService) {}

  ngOnInit(): void {
    this.userService.checkLogin();
  }

  ngAfterViewInit(): void {

  }


}
