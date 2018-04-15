import {Component, OnInit, Input, Output, EventEmitter} from '@angular/core';

@Component({
  selector: 'app-jumbotron',
  templateUrl: './jumbotron.component.html',
  styleUrls: ['./jumbotron.component.scss']
})
export class JumbotronComponent implements OnInit {
  @Input() title: string;
  @Input() subTitle: string;
  @Input() actionUrl: string;
  @Input() actionText: string;
  @Input() name: string;

  @Output() onLogin : EventEmitter<any> = new EventEmitter<any>();

  constructor() { }

  ngOnInit() {
  }

  loginClicked(e) {
    // e.preventDefault();
    // this.onLogin.emit(['login clicked']);
  }



}
