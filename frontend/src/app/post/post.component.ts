import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {PostModel} from "../services/news-api.service";

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})
export class PostComponent implements OnInit {
  @Input() post: PostModel | undefined;
  @Input() active: boolean;
  @Input() visible: boolean;

  @Output() voted = new EventEmitter<boolean>();

  constructor() { }

  ngOnInit() {
  }

  vote(event: MouseEvent, isLike: boolean) {
    this.voted.emit(isLike);
    event.stopPropagation();
  }
}
