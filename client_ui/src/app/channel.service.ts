import {Injectable, Optional} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import { Config } from "./config";
import {User} from "./user";

@Injectable()
export class ChannelService {

  constructor(private http : HttpClient) { }

  public getChannels(user: User) {
    const url = 'http://' + Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/service/fetch_channels';

    let headers = new HttpHeaders()
      .append("Accept", "application/json");

    let params = new HttpParams()
      .append('access_token', user.access_token)
      .append('user_id', user.id.toString());

    return this.http.get(url,{
      headers: headers,
      params: params
    });
  }

}
