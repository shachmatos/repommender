import { Component, OnInit } from '@angular/core';
import {ChannelService} from "../channel.service";
import {LoginService} from "../login.service";
import {User} from "../user";

@Component({
  selector: 'app-channel',
  templateUrl: './channel.component.html',
  styleUrls: ['./channel.component.scss']
})
export class ChannelComponent implements OnInit {
  channels : Object = [];
  constructor(private loginService: LoginService, private channelService : ChannelService) {

  }

  ngOnInit() {
    this.loginService.userChanged.subscribe(user => {
      this.onUserChanged(user);
    });

    if (this.loginService.getUser() != null)
      this.onUserChanged(this.loginService.getUser());
  }

  loadChannels(user: User): void {
    this.clearChannels();
    this.channelService.getChannels(user).subscribe(data => {
      this.channels = data['channels'] as Object[];
    });
  }

  clearChannels() : void {
    this.channels = [];
  }

  private onUserChanged(user: User): void {
    if (user != null)
      this.loadChannels(user);
    else
      this.clearChannels();
  }


}
