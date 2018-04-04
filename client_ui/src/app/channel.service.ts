import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Injectable()
export class ChannelService {

  constructor(private http : HttpClient) { }


  public getChannels() {
    const data = this.http.get('http://localhost:8000/service/1/fetch_channels');
    return data;
    // return [
    //   {
    //     title: 'Channel 1',
    //     repositories: [
    //       {
    //         name: 'Ch1 - Repo 1',
    //         desc: 'Ch1 - Repo 1 - repository 1 in channel 1',
    //         url: 'http://www.google.com/?q=repositroy 1'
    //       },
    //       {
    //         name: 'Ch1 - Repo 2',
    //         desc: 'Ch1 - Repo 2 - repository 2 in channel 1',
    //         url: 'http://www.google.com/?q=repositroy 2'
    //       },
    //       {
    //         name: 'Ch1 - Repo 3',
    //         desc: 'Ch1 - Repo 3 - repository 3 in channel 1',
    //         url: 'http://www.google.com/?q=repositroy 3'
    //       },
    //       {
    //         name: 'Ch1 - Repo 4',
    //         desc: 'Ch1 - Repo 4 - repository 4 in channel 1',
    //         url: 'http://www.google.com/?q=repositroy 4'
    //       },
    //     ]
    //   },
    //   {
    //     title: 'Channel 2',
    //     repositories: [
    //       {
    //         name: 'Ch2 - Repo 1',
    //         desc: 'Ch2 - Repo 1 - repository 1 in channel 2',
    //         url: 'http://www.google.com/?q=repositroy 1'
    //       },
    //       {
    //         name: 'Ch2 - Repo 2',
    //         desc: 'Ch2 - Repo 2 - repository 2 in channel 2',
    //         url: 'http://www.google.com/?q=repositroy 2'
    //       },
    //       {
    //         name: 'Ch2 - Repo 3',
    //         desc: 'Ch2 - Repo 3 - repository 3 in channel 2',
    //         url: 'http://www.google.com/?q=repositroy 3'
    //       },
    //       {
    //         name: 'Ch2 - Repo 4',
    //         desc: 'Ch2 - Repo 4 - repository 4 in channel 2',
    //         url: 'http://www.google.com/?q=repositroy 4'
    //       },
    //     ]
    //   },
    // ];
  }


}
