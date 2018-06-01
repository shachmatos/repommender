import { Component, OnInit } from '@angular/core';
import {ChannelService} from "../channel.service";
import {UserService} from "../user.service";
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
  constructor(private userService: UserService, private channelService : ChannelService) {

  }

  ngOnInit() {
    this.userService.userChanged.subscribe(user => {
      this.onUserChanged(user);
    });

    if (this.userService.getUser() != null) {
      this.onUserChanged(this.userService.getUser());
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
      let repos_raw = c['repositories'];
      let source_raw = c['source'];
      let repos = [];
      // let source = new Repository(source_raw['id'], source_raw['name'], source_raw['desc'], source_raw['url'], source_raw['topics']);

      for (let r of repos_raw) {
        // let shared_topics = r['topics'].filter((function(n) { return source.topics.indexOf(n) !== -1 }))
        // console.log(r);
        let topics = r['topics']; //.sort((a,b) => { return source.topics.indexOf(b) - source.topics.indexOf(a)});
        let repo = new Repository(r['id'], r['name'], r['desc'], r['url'], r['image'], topics, r['score']);
        repos.push(repo);
      }
      repos.sort((a: Repository,b: Repository) => { return b.score - a.score })
      this.channels.push(new Channel(user.id, c['title'], { placeholder: true }, repos));
    }
  }

  private onUserChanged(user: User): void {
    if (user != null)
      this.loadChannels(user);
    else
      this.clearChannels();
  }


}
