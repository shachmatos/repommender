import { Component, OnInit } from '@angular/core';
import {LoginService} from "../login.service";
import {Config} from "../config";
import {User} from "../user";

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.scss'],
})
export class NavBarComponent implements OnInit {

  login_url = 'https://github.com/login/oauth/authorize?client_id=' + Config.repommender_config.github_client_id + '&allow_signup=true';
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
  username: string = "unknown";
  user: User = null;

  constructor(private loginService: LoginService) { }

  ngOnInit() {
    this.loginService.userChanged.subscribe(user => {
      this.onUserChange(user);
    });
  }

  logout(e: Event): void {
    e.preventDefault();
    this.loginService.logout();
  }

  private onUserChange(user: User) {
    this.user = user;
  }

}
