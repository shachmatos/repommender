import {Repository} from "./repository";

export class Channel {

  constructor(public user_id: number, public title: string, public source: Repository, public repositories: Array<Repository> = null) {}
}
