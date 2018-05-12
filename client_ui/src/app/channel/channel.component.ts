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
      let repos_raw = JSON.parse(c['repositories']);
      let source_raw = JSON.parse(c['source']);
      let repos = [];
      let source = new Repository(source_raw['pk'], source_raw['fields']['name'], 'soon', source_raw['fields']['url'], source_raw['fields']['topics']);
      for (let r of repos_raw) {
        let fields = r['fields'];
        let repo = new Repository(r['pk'], fields['name'], "soon", fields['url'], fields['topics']);
        repos.push(repo);
      }
      this.channels.push(new Channel(user.id, c['title'], source, repos));
    }
  }

  private onUserChanged(user: User): void {
    if (user != null)
      this.loadChannels(user);
    else
      this.clearChannels();
  }


}
