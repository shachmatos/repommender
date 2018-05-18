import { TestBed, inject } from '@angular/core/testing';

import { PrefService } from './pref.service';

describe('PrefService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PrefService]
    });
  });

  it('should be created', inject([PrefService], (service: PrefService) => {
    expect(service).toBeTruthy();
  }));
});
