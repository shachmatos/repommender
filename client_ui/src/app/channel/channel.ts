import {Repository} from "./repository";

export class Channel {

  constructor(public user_id: number, public title: string, public repositories: Array<Repository> = null) {}
}
