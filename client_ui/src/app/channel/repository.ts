export class Repository {

  constructor(
    public id: number,
    public name: string,
    public description: string,
    public url: string,
    public topics: Array<string> = null
  ) {}

}
