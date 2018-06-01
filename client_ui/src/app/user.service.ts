import {EventEmitter, Injectable, Output} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {User} from "./user";
import {Config} from "./config";
import {CookieService} from "ngx-cookie-service";
import {ActivatedRoute} from "@angular/router";

@Injectable()
export class UserService {

  // static readonly base_url = Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/';
  private static readonly repommender_base_url: string =  'http://' + Config.repommender_config.server_url + ':' + Config.repommender_config.server_port + '/';
  private static readonly github_base_url: string = 'http://api.github.com/';


  private code: string = null;
  private user: User = null;
  private access_token: string = null;


  @Output() loginStatusChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() loginSuccess: EventEmitter<any> = new EventEmitter<any>();
  @Output() loginFailed: EventEmitter<any> = new EventEmitter<any>();
  @Output() loginExpired: EventEmitter<any> = new EventEmitter<any>();
  @Output() tokenValidated: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() userChanged: EventEmitter<User> = new EventEmitter<User>();
  @Output() preferencesSaved: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() userPreferencesFetched: EventEmitter<any> = new EventEmitter<any>();


  constructor(private route: ActivatedRoute, private http: HttpClient,
              private cookies: CookieService) { }

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
    const url = UserService.repommender_base_url + 'api/get_token/' + code;
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
    const url = UserService.github_base_url +  'user?access_token=' + token;
    let result = this.http.get(url);
    result.subscribe(
      data => {
        this.user = new User(data['id'], token, data['login'], data['name'], data['avatar_url']);
        this.userChanged.emit(this.user);
        this.getUserPreferences();
        this.tokenValidated.emit(true);
      },
      error => {
        console.log(error);
        this.user = null;
        this.userChanged.emit(this.user);
        this.tokenValidated.emit(false);
      });
  }


  private saveToken(): void {
    if (this.access_token != undefined)
      this.cookies.set('access_token', this.access_token);
  }

  public getUser(): User {
    return this.user;
  }

  public getUserPreferences(): void {
    const url = UserService.repommender_base_url + 'api/get_user_preferences/' + this.user.id;
    this.http.get(url).subscribe(
      data => { this.userPreferencesFetched.emit(data); },
      err => { console.log(err); }
    );
  }

  public saveUserPreferences(user: User, topics: Array<string>): void {
    let headers = new HttpHeaders();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    let payload = {topics: JSON.stringify(topics), languages: JSON.stringify([])};
    this.http.post(UserService.repommender_base_url + "api/save_preferences/" + user.id,
      payload,
      {headers: headers})
      .subscribe(
        result => {
          this.preferencesSaved.emit(true);
        },
        err => {
          this.preferencesSaved.emit(false);
        }
    );
  }


}
