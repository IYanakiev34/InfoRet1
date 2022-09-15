import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PaperServiceService {
  api_url: string = environment.backend_url;

  constructor(private http: HttpClient) {}

  // Get original (first 100) articles by author
  getArticlesByAuthor(authorId: string, sorting: string) {
    return this.http.get<any>(
      `${this.api_url}/articles?author=${authorId}&sort=${sorting}`
    );
  }

  // Get the author id
  getAuthorId(authorName: string) {
    return this.http.get<any>(`${this.api_url}/author?name=${authorName}`);
  }

  // Get the next100 papers of a given author ( we need to have the next link)
  getNext100(url: string) {
    return this.http.get<any>(
      `${this.api_url}/next?next=${encodeURIComponent(url)}`
    );
  }
}
