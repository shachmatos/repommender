export class User {
  constructor(public id: number,
              public access_token: string,
              public login: string,
              public name: string,
              public avatar: string = "",
              public gravatar_id: string = "",
              public preferred_topics: Array<string> = []) {}

}


