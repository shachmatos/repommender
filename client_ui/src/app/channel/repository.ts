import {EventEmitter} from "@angular/core";
import {moment} from "ngx-bootstrap/chronos/test/chain";

export class Repository {

  public selected: EventEmitter<Repository> = new EventEmitter<Repository>();

  constructor(
    public id: number,
    public name: string,
    public description: string,
    public url: string,
    public img: string,
    public open_issues: number,
    public forks_count: number,
    public size: number,
    public subscribers_count: number,
    public watchers_count: number,
    public topics: Array<string> = null,
    public languages: Array<string> = null,
    public score: number = null,
    public pushed_at: Date = null,
    public updated_at: Date = null
  ) {}


  public getScore(): number {
    return Math.trunc(this.score * 100);
  }

  public getLanguageList() {
    let result = [];
    for (let k in this.languages) {
      result.push(k);
    }
    result.sort((a: string,b: string) => { return this.languages[b] - this.languages[a] });
    return result;
  }

  public getDate() {
    return moment(this.updated_at).format('DD/MM/YYYY');
  }
}
