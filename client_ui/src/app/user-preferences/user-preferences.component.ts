import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  QueryList,
  Renderer2,
  ViewChild,
  ViewChildren, ViewContainerRef
} from '@angular/core';
import {Router} from "@angular/router";
import {UserService} from "../user.service";
import {User} from "../user";
import {PrefService} from "../pref.service";
import {TagInputComponent} from "ngx-chips";
import {NgxSmartModalComponent, NgxSmartModalService} from "ngx-smart-modal";
import {document} from "ngx-bootstrap/utils/facade/browser";
import {Ng4LoadingSpinnerService} from "ng4-loading-spinner";
import {ToastsManager} from "ng2-toastr";

@Component({
  selector: 'app-user-preferences',
  templateUrl: './user-preferences.component.html',
  styleUrls: ['./user-preferences.component.scss']
})
export class UserPreferencesComponent implements OnInit, AfterViewInit {

  topics: Array<any> = [];
  languages: Array<any> = [];
  user: User = null;
  placeholder: string = "+Topics";
  @ViewChild('topics_input') topics_input: TagInputComponent;
  @ViewChildren('tagbtn') buttons: QueryList<any>;
  @ViewChild('prefModal') prefModal: NgxSmartModalComponent;

  constructor(private userService: UserService,
              private router: Router,
              private renderer: Renderer2,
              private prefService: PrefService,
              public modalService: NgxSmartModalService,
              private elRef: ElementRef,
              private spinner: Ng4LoadingSpinnerService,
              private toastr: ToastsManager,
              private vcr: ViewContainerRef
  ) {
    this.toastr.setRootViewContainerRef(vcr);
  }

  ngOnInit() {
    this.userService.tokenValidated.subscribe(val => { this.onTokenValidated()});
    this.userService.loginFailed.subscribe(val => { this.onLoginFailed()});
    this.userService.loginStatusChange.subscribe(val => { if (!val) this.onLogout()});
    this.userService.userChanged.subscribe(user => { this.onUserCHanged(user)});
    this.prefService.getTopics().subscribe(data => { this.onGetTopics(data) });
    this.prefService.getLanguages().subscribe( data => { this.onGetLanguages(data)});
    this.userService.preferencesSaved.subscribe(
      data => { data ? this.onPrefSaved() : this.onPrefSaveError(); }
      );
    this.userService.userPreferencesFetched.subscribe(data => {this.onUserPreferencesFetched(data)});
  }

  private onUserCHanged(newUser: User) {
    this.user = newUser;
  }

  private onLogout() {
    this.router.navigate(['']);
  }

  private onLoginFailed() {
    this.router.navigate(['']);
  }

  private onTokenValidated() {

  }

  private onGetTopics(data: any) {
    this.topics = [];
    for (let item of data) {
      this.topics.push({'value': item.pk, 'display': item.fields.display_name});
    }
  }

  private onGetLanguages(data: any) {
    this.languages = [];
    for (let item of data) {
      this.languages.push(item.pk);
    }
  }

  private onPrefSaved() {
    this.prefModal.close();
    this.toastr.success("Preferences Saved Successfully!");
    this.spinner.hide();
  }

  private onUserPreferencesFetched(e) {
    if (e.topics) {
      for (let topic of e.topics) {
        console.log(topic);
        let item = this.buttons.find(item => { return item.nativeElement.id == topic});
        item.nativeElement.click();
      }
    }

    if (e.languages) {
      for (let lang of e.languages) {
        // TODO: add lang or not
      }
    }
  }

  public onTopicClick(e) {

    // let new_tag = {value: e.target.id, display: e.target.innerHTML};
    let new_tag = {'value': e.target.getAttribute('id'), 'display': e.target.innerHTML};
    let tag = this.topics_input.tags.find(item => item.model['value'] === new_tag.value);
    if (tag) {
      tag.remove(e);
    } else {
      this.topics_input.appendTag(new_tag);
      this.topics_input.onAdd.emit(new_tag);
    }
  }

  public onAddTopic(e) {
    let item = this.buttons.find(item => { return item.nativeElement.id == e.value});
    if (item) {
      this.renderer.removeClass(item.nativeElement, 'btn-info');
      this.renderer.addClass(item.nativeElement, 'btn-success');
    }

    if (this.topics_input.tags.length == this.topics.length) {
      this.placeholder = '';
    }
  }

  public onRemoveTopic(e) {
    let item = this.buttons.find(item => { console.log(item); return item.nativeElement.id == e.value});
    this.renderer.removeClass(item.nativeElement, 'btn-success');
    this.renderer.addClass(item.nativeElement, 'btn-info');

    if (this.topics_input.tags.length < this.topics.length) {
      this.placeholder = "+Topics";
    }
  }

  public saveUserPreferences() {
    this.spinner.show();
    let selected_topics = [];
    this.topics_input.tags.forEach(item => selected_topics.push(item.model['value']));
    this.userService.saveUserPreferences(this.user, selected_topics);
  }

  ngAfterViewInit(): void {
    let tag_input_div = this.elRef.nativeElement.querySelector('.ng2-tag-input');
    this.renderer.setStyle(tag_input_div,"min-height", "100%");
  }

  private onPrefSaveError() {
    this.toastr.error("Failed to save.");
    this.spinner.hide();
  }
}
