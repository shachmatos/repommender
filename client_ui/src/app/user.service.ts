import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {User} from "./user";
import {Config} from "./config";

@Injectable()
export class UserService {

  static readonly base_url = Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/';


  constructor(private http: HttpClient) { }

  public getTopics(user: User): Array<string> {
    const url = UserService.base_url + 'topics/' + user.id;
    let result = this.http.get(url);
    return ['topic1', 'topic2', 'topic3'];
  }

  public getLanguages(user: User): Array<string> {
    return ['lang1', 'lang2', 'lang3'];
  }

  public saveTopics(user: User, topics: Array<string>): void {

  }

  public saveLanguages(user: User, languages: Array<string>): void {

  }


}
