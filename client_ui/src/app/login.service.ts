import {EventEmitter, Injectable, OnInit, Output} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Config} from "./config";
import {CookieService} from "ngx-cookie-service";

@Injectable()
export class LoginService {

  private code: string = null;
  private access_token: string = null;

  @Output() loginStatusChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() loginSuccess: EventEmitter<any> = new EventEmitter<any>();
  @Output() loginFailed: EventEmitter<any> = new EventEmitter<any>();
  @Output() loginExpired: EventEmitter<any> = new EventEmitter<any>();

  constructor(private route: ActivatedRoute, private http: HttpClient, private cookies: CookieService) { }

  checkLogin(): boolean {
    return this.cookies.check('access_token') && this.validateToken(this.cookies.get('access_token'));
  }

  login(code: string): void {
    if (code) {
      this.validateCode(code);
    }
  }

  private validateCode(code: string): void {
    const url = 'http://' + Config.repommender_config.server_url + ':' + Config.repommender_config.server_port+ '/api/get_token/' + code;
    let res = this.http.post(url, {}, {});
    res.subscribe(
      val => {
          this.access_token = val['access_token'];
          this.saveToken();
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

  private validateToken(token: string): boolean {

    return true;
  }


  private saveToken(): void {
    this.cookies.set('access_token', this.access_token);
  }

}
