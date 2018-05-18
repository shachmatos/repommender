import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Config} from "./config";
import {Observable} from "rxjs/Observable";

@Injectable()
export class PrefService {

  static readonly base_url = 'http://' + Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/';

  constructor(private http: HttpClient) { }

  public getTopics(): Observable<any> {
    return this.http.get(PrefService.base_url + "api/topics");
  }

  public getLanguages(): Observable<any> {
    return this.http.get(PrefService.base_url + "api/languages");
  }

}
