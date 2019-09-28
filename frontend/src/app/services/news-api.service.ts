import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class NewsApiService {
  ENDPOINT = 'http://localhost:5000';

  constructor(private http: HttpClient) {
  }

  getPosts(fromTimestamp: number, count: number): Observable<PostModel[]> {
    const response = this.http.get(`${this.ENDPOINT}/posts`, {
      params: {
        timestamp: fromTimestamp.toString(),
        count: count.toString()
      }
    });
    return response as Observable<[PostModel]>;
  }

  getCelebrities(): Observable<string[]> {
    const response = this.http.get(`${this.ENDPOINT}/celeb_list`) as Observable<any[]>;
    return response.pipe(map(res => res.map(celeb => celeb["name"] as string)));
  }

  like(post: PostModel): Observable<any> {
    return this.http.post(`${this.ENDPOINT}/post_like`, {post_id: post.post_id})
  }

  dislike(post: PostModel): Observable<any> {
    return this.http.post(`${this.ENDPOINT}/post_dislike`, {post_id: post.post_id})
  }
}


export interface PostModel {
  post_id: string;
  author: string;
  status: string;
  avatar_source: string;
  author_id: string;
  content: string;
  timestamp: number;
  likes: number;
  reposts: number;
}
