import { Component, OnInit } from '@angular/core';
import {ChannelService} from "../channel.service";
import {LoginService} from "../login.service";
import {User} from "../user";
import {Channel} from "./channel";
import {Repository} from "./repository";

@Component({
  selector: 'app-channel',
  templateUrl: './channel.component.html',
  styleUrls: ['./channel.component.scss']
})
export class ChannelComponent implements OnInit {
  channels : Array<Channel> = [];
  constructor(private loginService: LoginService, private channelService : ChannelService) {

  }

  ngOnInit() {
    this.loginService.userChanged.subscribe(user => {
      this.onUserChanged(user);
    });

    if (this.loginService.getUser() != null) {
      this.onUserChanged(this.loginService.getUser());
    }
  }

  loadChannels(user: User): void {
    this.clearChannels();
    this.channelService.getChannels(user).subscribe(data => {
      this.onGetChannels(user, data);
    });
  }

  clearChannels() : void {
    this.channels = [];
  }

  private onGetChannels(user: User, data: Object) {
    for (let c of data['channels']) {
      let repos = [];
      for (let r of c['repositories']) {
        let repo = new Repository(r['id'], r['name'], r['description'], r['url']);
        repos.push(repo);
      }
      this.channels.push(new Channel(user.id, c['title'], repos));
    }
  }

  private onUserChanged(user: User): void {
    if (user != null)
      this.loadChannels(user);
    else
      this.clearChannels();
  }


}
