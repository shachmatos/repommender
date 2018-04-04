import { Component, OnInit } from '@angular/core';
import {ChannelService} from "../channel.service";

@Component({
  selector: 'app-channel',
  templateUrl: './channel.component.html',
  styleUrls: ['./channel.component.scss']
})
export class ChannelComponent implements OnInit {
  channels : Object = [];
  constructor(private channelService : ChannelService) {

  }

  ngOnInit() {
    this.channels = this.channelService.getChannels();
  }

  clearChannels() : void {
    this.channels = [];
  }


}
