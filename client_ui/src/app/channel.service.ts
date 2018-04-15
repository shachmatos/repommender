import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import { Config } from "./config";

@Injectable()
export class ChannelService {

  constructor(private http : HttpClient) { }

  public getChannels() {

    const headers = new HttpHeaders().set("Accept", "application/json");

    return this.http.get('http://' + Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/service/1/fetch_channels');
  }

}
