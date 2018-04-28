import {EventEmitter, Injectable, Output} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Config} from "./config";
import {CookieService} from "ngx-cookie-service";
import {User} from "./user";

/*
    avatar_url: "https://avatars0.githubusercontent.com/u/2797277?v=4"
    bio: null
    blog: ""
    company:null
    created_at: "2012-11-14T16:06:33Z"
    email: null
    events_url: "https://api.github.com/users/shachmatos/events{/privacy}"
    followers: 2
    followers_url: "https://api.github.com/users/shachmatos/followers"
    following: 1
    following_url: "https://api.github.com/users/shachmatos/following{/other_user}"
    gists_url: "https://api.github.com/users/shachmatos/gists{/gist_id}"
    gravatar_id: ""
    hireable: null
    html_url: "https://github.com/shachmatos"
    id: 2797277
    location: null
    login: "shachmatos"
    name: "Yftah Livny"
    organizations_url: "https://api.github.com/users/shachmatos/orgs"
    public_gists: 0
    public_repos: 2
    received_events_url: "https://api.github.com/users/shachmatos/received_events"
    repos_url: "https://api.github.com/users/shachmatos/repos"
    site_admin: false
    starred_url: "https://api.github.com/users/shachmatos/starred{/owner}{/repo}"
    subscriptions_url: "https://api.github.com/users/shachmatos/subscriptions"
    type: "User"
    updated_at: "2018-04-14T13:59:09Z"
    url:"https://api.github.com/users/shachmatos"

   */

@Injectable()
export class LoginService {

  private code: string = null;
  private user: User = null;
  private access_token: string = null;
  private static readonly repommender_base_url: string =  'http://' + Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/';
  private static readonly github_base_url: string = 'http://api.github.com/';


  @Output() loginStatusChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() loginSuccess: EventEmitter<any> = new EventEmitter<any>();
  @Output() loginFailed: EventEmitter<any> = new EventEmitter<any>();
  @Output() loginExpired: EventEmitter<any> = new EventEmitter<any>();
  @Output() tokenValidated: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() userChanged: EventEmitter<User> = new EventEmitter<User>();


  constructor(private route: ActivatedRoute, private http: HttpClient, private cookies: CookieService) { }

  checkLogin(): void {
    if (this.cookies.check('access_token')) {
      this.validateToken(this.cookies.get('access_token'));
    } else {
      this.route.queryParams.subscribe(
        params => {
          if (params['code']) {
            this.login(params['code']);
          }
        }
      );
    }
  }

  login(code: string): void {
    if (code) {
      this.validateCode(code);
    }
  }

  logout(): void {

    this.access_token = null;
    this.code = null;
    this.user = null;
    this.cookies.deleteAll();
    this.userChanged.emit(null);
    this.loginStatusChange.emit(false);
  }

  private validateCode(code: string): void {
    const url = LoginService.repommender_base_url + 'api/get_token/' + code;
    let res = this.http.post(url, {}, {});
    res.subscribe(
      val => {
          this.access_token = val['access_token'];
          this.saveToken();
          this.validateToken(this.access_token);
          this.loginSuccess.emit(this.access_token);
          this.loginStatusChange.emit(true);
        },
        err => {
          this.loginFailed.emit(code);
          this.loginStatusChange.emit(false);
        },
      () => {

      });
  }

  private validateToken(token: string): void {
    const url = LoginService.github_base_url +  'user?access_token=' + token;
    // const url = LoginService.github_base_url +  'user';
    let headers = new HttpHeaders();
    // headers = headers.append('Authorization', token + ' OAUTH-TOKEN');
    // console.log(headers.get('Authorization'));
    let result = this.http.get(url, {headers: headers});
    result.subscribe(
      data => {
        this.user = new User(data['id'], token, data['login'], data['name']);
        this.userChanged.emit(this.user);
        this.tokenValidated.emit(true);
      },
      error => {
        this.user = null;
        this.userChanged.emit(this.user);
        this.tokenValidated.emit(false);
      });
  }


  private saveToken(): void {
    this.cookies.set('access_token', this.access_token);
  }

  public getUser(): User{
    return this.user;
  }

}
