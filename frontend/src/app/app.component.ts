import {Component, ElementRef, ViewChild} from '@angular/core';
import {NewsApiService, PostModel} from './services/news-api.service';
import {FormControl} from '@angular/forms';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatAutocomplete, MatAutocompleteSelectedEvent, MatChipInputEvent} from '@angular/material';
import {Observable} from 'rxjs';
import {SatDatepickerInputEvent, SatDatepickerRangeValue} from 'saturn-datepicker';
import {ɵallowPreviousPlayerStylesMerge} from "@angular/animations/browser";
import {map, startWith} from "rxjs/operators";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';

  viewLiked = false;

  allPosts: PostModel[] = [];
  posts: PostModel[];
  stories: string[];

  celebCtrl = new FormControl();
  filteredCelebrities: Observable<string[]>;
  celebrities: string[] = [];
  allCelebrities: string[];

  tagCtrl = new FormControl();
  filteredTags: Observable<string[]>;
  tags: string[] = [];
  allTags: string[];

  separatorKeysCodes: number[] = [ENTER, COMMA];
  activePost = 0;
  range: SatDatepickerRangeValue<Date>;

  @ViewChild('celebInput', {static: false}) celebInput: ElementRef<HTMLInputElement>;
  @ViewChild('tagInput', {static: false}) tagInput: ElementRef<HTMLInputElement>;
  @ViewChild('auto', {static: false}) matAutocomplete: MatAutocomplete;
  storyCtrl = new FormControl();
  story: string = "";
  contactCtrl = new FormControl();
  contactCelebrities: string[];
  likedPosts: PostModel[] = [];


  constructor(private newsApi: NewsApiService) {
    this.newsApi.getCelebrities().subscribe(celebs => {
      this.allCelebrities = celebs;
      this.contactCelebrities = this.allCelebrities.slice().sort();

      this.contactCtrl.valueChanges.subscribe(value => {
        this.contactCelebrities = this.allCelebrities.filter(c => c.toLowerCase().includes(value.toLowerCase()))
      });

      this.filteredCelebrities = this.celebCtrl.valueChanges.pipe(
        startWith(null),
        map(celeb => celeb ? this._filter(this.allCelebrities, celeb) : this.allCelebrities.slice()));
    });

    this.newsApi.getTags().subscribe(tags => {
      this.allTags = tags;
      this.filteredTags = this.tagCtrl.valueChanges.pipe(
        startWith(null),
        map(tag => tag ? this._filter(this.allTags, tag) : this.allTags.slice()))
    });

    this.newsApi.likedPosts().subscribe(posts => {
      this.likedPosts = posts;
    });

    this.setWeek();
  }

  remove(items: string[], item: string) {
    const index = items.indexOf(item);

    if (index >= 0) {
      items.splice(index, 1);
    }

    this.filter();
  }

  add(event: MatChipInputEvent, items: string[], ctrl: FormControl) {
    if (!this.matAutocomplete.isOpen) {
      const input = event.input;
      const value = event.value;

      if ((value || '').trim()) {
        items.push(value.trim());
      }

      if (input) {
        input.value = '';
      }

      ctrl.setValue(null);
    }
  }

  selectedCeleb(event: MatAutocompleteSelectedEvent) {
    this.celebrities.push(event.option.viewValue);
    this.celebInput.nativeElement.value = '';
    this.celebCtrl.setValue(null);
    this.filter();
  }

  selectedTag(event: MatAutocompleteSelectedEvent) {
    this.tags.push(event.option.viewValue);
    this.tagInput.nativeElement.value = '';
    this.tagCtrl.setValue(null);
    this.filter();
  }

  setOneDay() {
    const startDate = new Date();
    startDate.setHours(0);
    startDate.setMinutes(0);
    startDate.setSeconds(0);

    this.range = {
      begin: startDate,
      end: new Date()
    } as SatDatepickerRangeValue<Date>;

    this.updatePosts();
  }

  setWeek() {
    const startDate = new Date();
    startDate.setHours(0);
    startDate.setMinutes(0);
    startDate.setSeconds(0);
    startDate.setDate(startDate.getDate() - 7);

    this.range = {
      begin: startDate,
      end: new Date()
    } as SatDatepickerRangeValue<Date>;

    this.updatePosts();
  }

  setMonth() {
    const startDate = new Date();
    startDate.setHours(0);
    startDate.setMinutes(0);
    startDate.setSeconds(0);
    startDate.setMonth(startDate.getMonth() - 1);

    this.range = {
      begin: startDate,
      end: new Date()
    } as SatDatepickerRangeValue<Date>;

    this.updatePosts();
  }

  onDateChangeEvent(event: SatDatepickerInputEvent<Date>) {
    this.range = event.value as SatDatepickerRangeValue<Date>;
    this.updatePosts();
  }

  filter() {
    // console.log(this.range.begin.getTime() + ' ' + this.range.end.getTime());
    // console.log(this.allPosts[0].timestamp);


    let tagSet = new Set(this.tags);
    // console.log(this.allPosts[0].timestamp, this.range.begin.getTime());
    this.posts = this.allPosts
      // .filter(post => post.status === 'unknown')
      .filter(post => this.celebrities.length === 0 || this.celebrities.includes(post.author))
      // .filter(post => this.range === undefined
      //   || (post.timestamp * 1000 >= this.range.begin.getTime() && post.timestamp * 1000 <= this.range.end.getTime()))
      .filter(post => this.tags.length === 0 || post.tags.filter(t => tagSet.has(t)).length > 0)
      .sort((post1, post2) =>
        post1.timestamp === post2.timestamp ? 0 : post1.timestamp > post2.timestamp ? -1 : 1);
    this.activePost = this.posts.findIndex((post => post.status === 'unknown'));
  }


  vote(isLike: boolean) {
    const post = this.posts[this.activePost];
    if (isLike) {
      this.newsApi.like(post).subscribe(x => console.log(123))
    } else {
      this.newsApi.dislike(post)
    }
    post.status = isLike ? 'liked' : 'disliked';

    this.newsApi.likedPosts().subscribe(posts => {
      this.likedPosts = posts;
    });

    this.activePost = this.activePost + 1;
  }

  _filter(items
            :
            string[], item
            :
            string
  ) {
    return items.filter(
      c => c.toLowerCase().indexOf(item.toLowerCase()) !== -1
    );
  }

  selectedStory(event: MatAutocompleteSelectedEvent) {
    this.story = event.option.viewValue;
    console.log(this.story);
    this.updatePosts();
  }

  updatePosts() {
    let story = this.story && this.stories && this.stories.includes(this.story) ? this.story : undefined;
    this.newsApi.getPosts(this.range.begin.getTime(), this.range.end.getTime(), story).subscribe(posts => {
      this.allPosts = posts["posts"];
      this.stories = posts["stories"].map(s => s["title"]);
      this.filter();
    });

  }
}
