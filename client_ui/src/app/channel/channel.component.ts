import { Component, OnInit } from '@angular/core';
import {ChannelService} from "../channel.service";
import {UserService} from "../user.service";
import {User} from "../user";
import {Channel} from "./channel";
import {Repository} from "./repository";
import {animate, keyframes, query, stagger, state, style, transition, trigger} from "@angular/animations";
import {PerfectScrollbarConfigInterface} from 'ngx-perfect-scrollbar';

@Component({
  selector: 'app-channel',
  templateUrl: './channel.component.html',
  styleUrls: ['./channel.component.scss'],
  animations: [
    trigger('infoPanelOpen', [
      transition('void => *', [
        style({height: 0}),
        animate(500, style({height: '*'})),
      ]),
      transition('* => void', [
        style({height: '*'}),
        animate(500, style({height: 0})),
      ])
    ])
  ]
})
export class ChannelComponent implements OnInit {
  channels : Array<Channel> = [];
  open_info_channel: Channel = null;

  public config: PerfectScrollbarConfigInterface = {
    wheelPropagation: true,
    swipeEasing: true,
    minScrollbarLength: 100
  };

  constructor(private userService: UserService, private channelService: ChannelService) {

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

  private createChannel(user: User, raw_channel): Channel {
    let repos_raw = raw_channel['repositories'];
    let source_raw = raw_channel['source'];
    let channel = null;
    if (source_raw == undefined) {
      channel = new Channel(user.id, "Picks for you", {});
    } else {
      let source = new Repository(
        source_raw['id'],
        source_raw['name'],
        source_raw['description'],
        source_raw['url'],
        source_raw['image'],
        source_raw['open_issues'],
        source_raw['forks_count'],
        source_raw['size'],
        source_raw['subscribers_count'],
        source_raw['watchers_count'],
        source_raw['topics'],
        source_raw['languages'],
        source_raw['score'],
        source_raw['pushed_at'],
        source_raw['updated_at']
      );
      channel = new Channel(user.id, "Picks for you", source);
    }
    // let source = new Repository(source_raw['id'], source_raw['name'], source_raw['desc'], source_raw['url'], source_raw['topics']);
    for (let r of repos_raw) {
      let topics = r['topics']; //.sort((a,b) => { return source.topics.indexOf(b) - source.topics.indexOf(a)});
      let languages = r['languages'];
      let repo = new Repository(
        r['id'],
        r['name'],
        r['description'],
        r['url'],
        r['image'],
        r['open_issues'],
        r['forks_count'],
        r['size'],
        r['subscribers_count'],
        r['watchers_count'],
        topics,
        languages,
        r['score'],
        r['pushed_at'],
        r['updated_at']
      );
      // repos.push(repo);
      channel.addRepository(repo);
    }
    channel.sortByScore();
    channel.selected.subscribe(chan => { this.onChannelSelected(chan)});
    return channel;
  }

  private onGetChannels(user: User, data: Object) {
    let picks_for_you = this.createChannel(user, data['picks_for_you'][0]);
    this.channels.push(picks_for_you);


    for (let c of data['channels']) {
      let channel = this.createChannel(user, c);
      this.channels.push(channel);
    }
  }

  private onUserChanged(user: User): void {
    if (user != null)
      this.loadChannels(user);
    else
      this.clearChannels();
  }


  private onChannelSelected(channel: Channel): void {
    this.open_info_channel = channel;
  }


}
