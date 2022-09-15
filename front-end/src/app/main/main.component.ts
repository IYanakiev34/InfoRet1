import { Component, OnInit } from '@angular/core';
import { PaperServiceService } from '../services/paper-service.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit {
  papers: any = new Array<any>();
  authorName: string = '';
  sorting: string = '';
  authorId: string = '';
  totalCitations: number = 0;
  enumeration: number = 0;
  canSearchMore: boolean = false;
  linkToNext: string = '';

  constructor(private paperService: PaperServiceService) {}

  ngOnInit(): void {}

  // Get the next chunk of 100 papers
  getNext() {
    this.paperService.getNext100(this.linkToNext).subscribe((res) => {
      res = JSON.stringify(res);
      res = JSON.parse(res);

      if (res.search_metadata.status == 'Success') {
        for (var i = 0; i < res.articles.length; i++) {
          this.papers.push(res.articles[i]);
        }

        if (res.hasOwnProperty('serpapi_pagination')) {
          this.canSearchMore = true;
          this.linkToNext = res.serpapi_pagination.next;
        } else {
          this.canSearchMore = false;
        }
      } else {
        alert('Problem occured when searching for the next 100 articles');
      }
    });
  }

  // Get the original papers + will reset author if new author typed
  onSubmit($event: SubmitEvent) {
    $event.preventDefault();

    if (this.sorting == 'By Date') {
      this.sorting = 'pubdate';
    } else if (this.sorting == 'By Citations') {
      this.sorting = '';
    }

    this.paperService.getAuthorId(this.authorName).subscribe((res) => {
      res = JSON.stringify(res);
      res = JSON.parse(res);

      this.totalCitations = res.profiles[0].cited_by;
      this.authorId = res.profiles[0].author_id;

      if (res.search_metadata.status == 'Success') {
        this.paperService
          .getArticlesByAuthor(this.authorId, this.sorting)
          .subscribe((art) => {
            art = JSON.stringify(art);
            art = JSON.parse(art);

            if (art.search_metadata.status == 'Success') {
              this.papers = art.articles;

              if (art.serpapi_pagination.next != undefined) {
                this.canSearchMore = true;
                this.linkToNext = art.serpapi_pagination.next;
              } else {
                this.canSearchMore = false;
                this.linkToNext = '';
              }
            } else {
              alert('Problem occured when trying to get the articles!');
            }
          });
      } else {
        alert(
          'Problem occurred when getting the author ID probably wrong name!'
        );
      }
    });
  }
}
