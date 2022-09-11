import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PaperServiceService {
  api_url: string = environment.backend_url;

  constructor(private http: HttpClient) {}

  getArticlesByAuthor(authorId: string, sorting: string) {
    return this.http.get<any>(
      `${this.api_url}/articles?author=${authorId}&sort=${sorting}`
    );
  }

  getAuthorId(authorName: string) {
    return this.http.get<any>(`${this.api_url}/author?name=${authorName}`);
  }
}
