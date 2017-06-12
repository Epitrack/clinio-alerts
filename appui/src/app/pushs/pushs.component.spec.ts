import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PushsComponent } from './pushs.component';

describe('PushsComponent', () => {
  let component: PushsComponent;
  let fixture: ComponentFixture<PushsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PushsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PushsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
