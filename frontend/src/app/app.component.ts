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
  celebCtrl = new FormControl();
  title = 'frontend';
  allPosts: PostModel[];
  posts: PostModel[];

  filteredCelebrities: Observable<string[]>;
  celebrities: string[] = [];
  allCelebrities: string[];

  separatorKeysCodes: number[] = [ENTER, COMMA];
  activePost = 0;
  range: SatDatepickerRangeValue<Date>;

  @ViewChild('celebInput', {static: false}) celebInput: ElementRef<HTMLInputElement>;
  @ViewChild('auto', {static: false}) matAutocomplete: MatAutocomplete;


  constructor(private newsApi: NewsApiService) {
    console.log(123);
    const timestamp = new Date().getTime();
    this.newsApi.getPosts(timestamp, 5).subscribe(posts => {
      this.allPosts = posts;
      this.posts = Array.from(this.allPosts);
      this.setOneDay();
    });
    this.newsApi.getCelebrities().subscribe(celebrities => {
      this.allCelebrities = celebrities;
      this.filteredCelebrities = this.celebCtrl.valueChanges.pipe(
        startWith(null),
        map(celeb => celeb ? this._filter(celeb) : this.allCelebrities.slice()))
    });

  }

  remove(celeb: string) {
    const index = this.celebrities.indexOf(celeb);

    if (index >= 0) {
      this.celebrities.splice(index, 1);
    }

    this.filter();
  }

  add(event: MatChipInputEvent) {
    if (!this.matAutocomplete.isOpen) {
      const input = event.input;
      const value = event.value;

      // Add our celeb
      if ((value || '').trim()) {
        this.celebrities.push(value.trim());
      }

      // Reset the input value
      if (input) {
        input.value = '';
      }

      this.celebCtrl.setValue(null);
    }
  }

  selected(event: MatAutocompleteSelectedEvent) {
    this.celebrities.push(event.option.viewValue);
    this.celebInput.nativeElement.value = '';
    this.celebCtrl.setValue(null);
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

    this.filter();
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

    this.filter();
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

    this.filter();
  }

  onDateChangeEvent(event: SatDatepickerInputEvent<Date>) {
    this.range = event.value as SatDatepickerRangeValue<Date>;
  }

  filter() {
    // console.log(this.range.begin.getTime() + ' ' + this.range.end.getTime());
    // console.log(this.allPosts[0].timestamp);

    this.posts = this.allPosts
      .filter(post => post.status === 'unknown')
      .filter(post => this.celebrities.length === 0 || this.celebrities.includes(post.author))
      .filter(post => this.range === undefined
        || (post.timestamp * 1000  >= this.range.begin.getTime() && post.timestamp * 1000 <= this.range.end.getTime()))
      .sort((post1, post2) =>
        post1.timestamp === post2.timestamp ? 0 : post1.timestamp > post2.timestamp ? -1 : 1);
    this.activePost = 0;
  }

  vote(isLike: boolean) {
    const post = this.posts[this.activePost];
    if (isLike) {
      this.newsApi.like(post)
    } else {
      this.newsApi.dislike(post)
    }
    post.status = isLike ? 'liked' : 'disliked';

    this.activePost = this.activePost + 1;
  }

  _filter(celeb: string) {
    return this.allCelebrities.filter(
      c => c.toLowerCase().indexOf(celeb.toLowerCase()) !== -1
    );
  }
}
