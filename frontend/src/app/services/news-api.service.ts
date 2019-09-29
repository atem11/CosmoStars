import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class NewsApiService {
  ENDPOINT = 'http://localhost:5000';

  constructor(private http: HttpClient) {
  }

  getPosts(fromTimestamp: number, toTimestamp: number, query: string | undefined): Observable<PostModel[]> {
    const params = query ? {
      time_start: fromTimestamp.toString(),
      time_end: toTimestamp.toString(),
      query: query
    } : {
      time_start: fromTimestamp.toString(),
      time_end: toTimestamp.toString(),
    };
    const response = this.http.get(`${this.ENDPOINT}/posts`, {
      params: params
    });
    return response as Observable<PostModel[]>;
  }

  getTags(): Observable<string[]> {
    const response = this.http.get(`${this.ENDPOINT}/tags`) as Observable<any[]>;
    return response as Observable<string[]>
  }

  getCelebrities(): Observable<string[]> {
    const response = this.http.get(`${this.ENDPOINT}/celeb_list`) as Observable<any[]>;
    return response.pipe(map(res => res.map(celeb => celeb["name"] as string)));
  }

  like(post: PostModel): Observable<any> {
    return this.http.post(`${this.ENDPOINT}/post_like`, new HttpParams().set('post_id', post.post_id))
  }

  dislike(post: PostModel): Observable<any> {
    return this.http.post(`${this.ENDPOINT}/post_dislike`, new HttpParams().set('post_id', post.post_id))
  }

  likedPosts(): Observable<PostModel[]> {
    return this.http.get(`${this.ENDPOINT}/liked_posts`) as Observable<PostModel[]>
  }
}


export interface PostModel {
  post_id: string;
  author: string;
  status: string;
  avatar_source: string;
  domain: string;
  content: string;
  timestamp: number;
  likes: number;
  reposts: number;
  tags: string[];
}
