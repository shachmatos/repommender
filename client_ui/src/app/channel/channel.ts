import {Repository} from "./repository";
import {EventEmitter} from "@angular/core";

export class Channel {
  public info_open: boolean = false;
  public selected_repo: Repository = null;

  public selected: EventEmitter<Channel> = new EventEmitter<Channel>();

  constructor(public user_id: number, public title: string, public source: any, public repositories: Array<Repository> = []) {

  }

  public addRepository(repo: Repository) {
    this.repositories.push(repo);
    repo.selected.subscribe( repo => {
      this.onRepoSelected(repo);
    });
  }

  private onRepoSelected(repo: Repository) {
    if (this.info_open && repo == this.selected_repo) {
      this.info_open = false;
    } else {
      this.info_open = true;
    }
    this.selected.emit(this);
    this.selected_repo = repo;
  }

  public sortByScore() {
    this.repositories.sort((a: Repository,b: Repository) => { return b.score - a.score });
  }
}
