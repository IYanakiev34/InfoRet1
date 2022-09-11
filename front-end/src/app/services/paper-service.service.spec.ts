import { TestBed } from '@angular/core/testing';

import { PaperServiceService } from './paper-service.service';

describe('PaperServiceService', () => {
  let service: PaperServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PaperServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
